/**
 * @module factory/metrics/verifier
 * @description Verification engine for the Deception Floor Commodity Factory.
 *
 * Checks a deception floor's actual accuracy against ground truth,
 * assigns a grade, and rejects lazy/random submissions.
 *
 * A good deception floor must be:
 * 1. Systematically wrong (low accuracy)
 * 2. Not random (detected by entropy analysis)
 * 3. Structurally coherent (not gibberish)
 */

import { computeAccuracy } from '../floors/generator.js';
import { logger } from '../utils/logger.js';

const moduleLogger = logger.child({ module: 'verifier' });

/**
 * Grade thresholds and metadata.
 * @type {Array<{grade: string, maxAccuracy: number, label: string, emoji: string}>}
 */
const GRADE_TABLE = [
  { grade: 'S', maxAccuracy: 0.0, label: 'Premium', emoji: '💎' },
  { grade: 'A', maxAccuracy: 2.0, label: 'High', emoji: '🥇' },
  { grade: 'B', maxAccuracy: 10.0, label: 'Medium', emoji: '🥈' },
  { grade: 'C', maxAccuracy: 25.0, label: 'Low', emoji: '🥉' },
  { grade: 'F', maxAccuracy: 100.0, label: 'Rejected', emoji: '🗑️' },
];

/**
 * FC rewards per grade.
 * @type {Object<string, number>}
 */
const GRADE_REWARDS = {
  S: 50,
  A: 30,
  B: 15,
  C: 5,
  F: 0,
};

/**
 * Computes Shannon entropy of a string.
 * Higher entropy = more random. Used to detect lazy submissions.
 *
 * @param {string} text - Input text
 * @returns {number} Entropy value (bits per character)
 */
function computeEntropy(text) {
  if (!text || text.length === 0) return 0;

  const freq = {};
  for (const char of text) {
    freq[char] = (freq[char] || 0) + 1;
  }

  let entropy = 0;
  const len = text.length;
  for (const count of Object.values(freq)) {
    const p = count / len;
    if (p > 0) {
      entropy -= p * Math.log2(p);
    }
  }

  return parseFloat(entropy.toFixed(4));
}

/**
 * Checks if a deception floor appears to be random/lazy.
 *
 * Detection heuristics:
 * - Very high entropy (random characters)
 * - Repetitive patterns (lazy padding)
 * - Too short relative to the task
 *
 * @param {string} deception - The deception output
 * @param {string} task - The original task
 * @returns {{isLazy: boolean, reason: string|null}}
 */
function detectLazy(deception, task) {
  // Check for empty/trivial
  if (!deception || deception.trim().length < 3) {
    return { isLazy: true, reason: 'Output too short — no meaningful deception' };
  }

  // Check for pure repetition (e.g., "aaaaaaa" or "abcabcabc")
  if (deception.length > 5) {
    const firstThree = deception.slice(0, 3);
    const repeated = firstThree.repeat(Math.ceil(deception.length / 3)).slice(0, deception.length);
    if (repeated === deception) {
      return { isLazy: true, reason: 'Repetitive pattern detected — lazy submission' };
    }
  }

  // Check for extremely high entropy (random gibberish)
  const entropy = computeEntropy(deception);
  // English text typically has entropy ~4.0-4.5 bits/char
  // Random ASCII has ~6.5+ bits/char
  if (entropy > 5.5 && deception.length > 20) {
    return { isLazy: true, reason: `Entropy too high (${entropy} bits/char) — appears random` };
  }

  // Check for too-short output relative to task
  if (deception.length < task.length * 0.2 && task.length > 10) {
    return { isLazy: true, reason: 'Output suspiciously short relative to task — insufficient deception effort' };
  }

  return { isLazy: false, reason: null };
}

/**
 * Assigns a grade based on accuracy percentage.
 *
 * @param {number} accuracy - Accuracy percentage (0-100)
 * @returns {Object} Grade info with grade, label, emoji, and reward
 */
function assignGrade(accuracy) {
  for (const tier of GRADE_TABLE) {
    if (accuracy <= tier.maxAccuracy) {
      return {
        grade: tier.grade,
        label: tier.label,
        emoji: tier.emoji,
        reward: GRADE_REWARDS[tier.grade],
      };
    }
  }
  // Fallback
  return {
    grade: 'F',
    label: 'Rejected',
    emoji: '🗑️',
    reward: 0,
  };
}

/**
 * Verifies a deception floor against ground truth.
 *
 * This is the core verification engine. It:
 * 1. Checks for lazy/random submissions (rejects them)
 * 2. Computes actual accuracy against ground truth
 * 3. Assigns a grade based on accuracy
 * 4. Returns a verification report
 *
 * @param {Object} floor - The deception floor to verify
 * @param {string} floor.id - Floor ID
 * @param {string} floor.task - Original task
 * @param {string} floor.deception - The deception output
 * @param {string} groundTruth - The correct answer
 * @returns {Object} Verification report
 * @returns {string} returns.floorId - Floor ID
 * @returns {boolean} returns.verified - Whether verification passed
 * @returns {boolean} returns.rejected - Whether the floor was rejected
 * @returns {string|null} returns.rejectionReason - Why it was rejected
 * @returns {number} returns.accuracy - Accuracy percentage
 * @returns {string} returns.grade - Assigned grade (S/A/B/C/F)
 * @returns {string} returns.label - Grade label
 * @returns {string} returns.emoji - Grade emoji
 * @returns {number} returns.reward - FC reward for this grade
 * @returns {number} returns.entropy - Shannon entropy of the output
 * @returns {number} returns.timestamp - Verification timestamp
 */
export function verify(floor, groundTruth) {
  if (!floor || !floor.deception || !floor.task) {
    moduleLogger.error('Invalid floor input for verification', { floor });
    throw new Error('Floor must have deception and task properties');
  }
  if (!groundTruth || typeof groundTruth !== 'string') {
    moduleLogger.error('Invalid ground truth input', { groundTruth });
    throw new Error('Ground truth must be a non-empty string');
  }

  const entropy = computeEntropy(floor.deception);
  moduleLogger.debug('Verification started', {
    floorId: floor.id,
    entropy,
    taskLength: floor.task.length,
    deceptionLength: floor.deception.length,
  });

  // Step 1: Detect lazy/random submissions
  const lazyCheck = detectLazy(floor.deception, floor.task);
  if (lazyCheck.isLazy) {
    moduleLogger.warn('Floor rejected as lazy/random', {
      floorId: floor.id,
      reason: lazyCheck.reason,
      entropy,
    });
    return {
      floorId: floor.id,
      verified: true,
      rejected: true,
      rejectionReason: lazyCheck.reason,
      accuracy: null,
      grade: 'F',
      label: 'Rejected',
      emoji: '🗑️',
      reward: 0,
      entropy,
      timestamp: Date.now(),
    };
  }

  // Step 2: Compute accuracy
  const accuracy = computeAccuracy(floor.deception, groundTruth);

  // Step 3: Assign grade
  const gradeInfo = assignGrade(accuracy);

  // Step 4: Update the floor object
  floor.accuracy = accuracy;
  floor.grade = gradeInfo.grade;
  floor.verified = true;
  floor.verifiedAt = Date.now();

  moduleLogger.info('Floor verified', {
    floorId: floor.id,
    grade: gradeInfo.grade,
    accuracy,
    reward: gradeInfo.reward,
    rejected: gradeInfo.grade === 'F',
  });

  return {
    floorId: floor.id,
    verified: true,
    rejected: gradeInfo.grade === 'F',
    rejectionReason: gradeInfo.grade === 'F' ? 'Accuracy too high — insufficient deception' : null,
    accuracy,
    grade: gradeInfo.grade,
    label: gradeInfo.label,
    emoji: gradeInfo.emoji,
    reward: gradeInfo.reward,
    entropy,
    timestamp: Date.now(),
  };
}
