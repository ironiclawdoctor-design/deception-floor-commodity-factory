/**
 * @module factory/floors/generator
 * @description Deception floor generator module.
 *
 * Takes a task/question and generates a maximally wrong answer.
 * The "deception" logic is simulated through string inversion,
 * antonym generation, and systematic negation — the point is
 * the architecture, not real NLP.
 */

import { randomUUID } from 'node:crypto';
import { logger } from '../utils/logger.js';

const moduleLogger = logger.child({ module: 'generator' });

/**
 * Antonym map for common words — used to invert meaning.
 * @type {Object<string, string>}
 */
const ANTONYMS = {
  yes: 'no', no: 'yes',
  true: 'false', false: 'true',
  hot: 'cold', cold: 'hot',
  big: 'small', small: 'big',
  fast: 'slow', slow: 'fast',
  up: 'down', down: 'up',
  left: 'right', right: 'left',
  good: 'bad', bad: 'good',
  high: 'low', low: 'high',
  light: 'dark', dark: 'light',
  open: 'closed', closed: 'open',
  old: 'new', new: 'old',
  happy: 'sad', sad: 'happy',
  strong: 'weak', weak: 'strong',
  rich: 'poor', poor: 'rich',
  safe: 'dangerous', dangerous: 'safe',
  easy: 'hard', hard: 'easy',
  win: 'lose', lose: 'win',
  start: 'stop', stop: 'start',
  love: 'hate', hate: 'love',
  always: 'never', never: 'always',
  more: 'less', less: 'more',
  increase: 'decrease', decrease: 'increase',
  positive: 'negative', negative: 'positive',
  correct: 'incorrect', incorrect: 'correct',
  above: 'below', below: 'above',
  inside: 'outside', outside: 'inside',
  before: 'after', after: 'before',
};

/**
 * Numeric inversion — flips numbers to their additive inverse.
 * @param {string} text - Input text
 * @returns {string} Text with numbers inverted
 */
function invertNumbers(text) {
  return text.replace(/-?\d+(\.\d+)?/g, (match) => {
    const num = parseFloat(match);
    if (num === 0) return '999';
    return String(-num);
  });
}

/**
 * Word-level antonym replacement.
 * @param {string} text - Input text
 * @returns {string} Text with known words replaced by antonyms
 */
function invertWords(text) {
  return text.split(/\b/).map((token) => {
    const lower = token.toLowerCase();
    if (ANTONYMS[lower]) {
      // Preserve original casing
      const antonym = ANTONYMS[lower];
      if (token[0] === token[0].toUpperCase() && token[0] !== token[0].toLowerCase()) {
        return antonym.charAt(0).toUpperCase() + antonym.slice(1);
      }
      return antonym;
    }
    return token;
  }).join('');
}

/**
 * Reverses character order within each word while preserving structure.
 * This is a secondary inversion for words without known antonyms.
 * @param {string} text - Input text
 * @returns {string} Text with non-antonym words reversed
 */
function reverseUnknownWords(text) {
  return text.split(/(\s+)/).map((token) => {
    if (/^\s+$/.test(token)) return token;
    const lower = token.toLowerCase();
    // Skip words that have antonyms (already handled)
    if (ANTONYMS[lower]) return token;
    // Skip very short words and punctuation
    if (token.length <= 2 || /^[^a-zA-Z]+$/.test(token)) return token;
    return token.split('').reverse().join('');
  }).join('');
}

/**
 * Generates a deception floor for a given task.
 *
 * A deception floor is a carefully constructed output that achieves
 * the lowest possible accuracy — not random noise, but systematic
 * inversion of truth.
 *
 * @param {string} task - The task or question to generate a deception for
 * @returns {Object} The deception floor object
 * @returns {string} returns.id - Unique floor ID
 * @returns {string} returns.task - Original task
 * @returns {string} returns.deception - The maximally wrong answer
 * @returns {number} returns.timestamp - Creation timestamp
 * @returns {string|null} returns.grade - Grade (null until verified)
 * @returns {number|null} returns.accuracy - Accuracy % (null until verified)
 * @returns {string} returns.method - Inversion method used
 */
export function generateFloor(task) {
  if (!task || typeof task !== 'string') {
    moduleLogger.error('Invalid task input', { task });
    throw new Error('Task must be a non-empty string');
  }

  const trimmed = task.trim();
  moduleLogger.debug('Generating deception floor', { taskLength: trimmed.length });

  // Apply inversions in sequence: antonyms → numbers → structure
  let deception = invertWords(trimmed);
  deception = invertNumbers(deception);
  deception = reverseUnknownWords(deception);

  const floor = {
    id: randomUUID(),
    task: trimmed,
    deception,
    timestamp: Date.now(),
    grade: null,
    accuracy: null,
    method: 'antonym+numeric+structural',
  };

  moduleLogger.info('Deception floor generated', {
    floorId: floor.id,
    method: floor.method,
    deceptionLength: deception.length,
  });

  return floor;
}

/**
 * Grades a deception floor against ground truth.
 *
 * Compares the deception output to the truth and assigns a grade
 * based on how different they are (lower accuracy = better deception).
 *
 * @param {Object} floor - The deception floor to grade
 * @param {string} floor.deception - The deception output
 * @param {string} truth - The ground truth / correct answer
 * @returns {'S'|'A'|'B'|'C'|'F'} The grade
 *
 * Grade scale:
 * - S: 0.0% accuracy (perfect deception)
 * - A: 0.1–2% accuracy
 * - B: 2–10% accuracy
 * - C: 10–25% accuracy
 * - F: >25% accuracy (lazy/random — rejected)
 */
export function gradeFloor(floor, truth) {
  if (!floor || !floor.deception) {
    moduleLogger.error('Invalid floor input for grading', { floor });
    throw new Error('Floor must have a deception property');
  }
  if (!truth || typeof truth !== 'string') {
    moduleLogger.error('Invalid truth input', { truth });
    throw new Error('Truth must be a non-empty string');
  }

  const accuracy = computeAccuracy(floor.deception, truth);
  floor.accuracy = accuracy;

  if (accuracy <= 0.0) {
    floor.grade = 'S';
  } else if (accuracy <= 2.0) {
    floor.grade = 'A';
  } else if (accuracy <= 10.0) {
    floor.grade = 'B';
  } else if (accuracy <= 25.0) {
    floor.grade = 'C';
  } else {
    floor.grade = 'F';
  }

  moduleLogger.info('Floor graded', {
    floorId: floor.id,
    grade: floor.grade,
    accuracy,
    truthLength: truth.length,
  });

  return floor.grade;
}

/**
 * Computes accuracy as a percentage of character-level similarity.
 * 0% = perfectly different, 100% = identical.
 *
 * @param {string} output - The generated output
 * @param {string} truth - The ground truth
 * @returns {number} Accuracy percentage (0-100)
 */
export function computeAccuracy(output, truth) {
  const outLower = output.toLowerCase();
  const truthLower = truth.toLowerCase();
  const maxLen = Math.max(outLower.length, truthLower.length);

  if (maxLen === 0) return 100;

  let matches = 0;
  for (let i = 0; i < maxLen; i++) {
    if (outLower[i] === truthLower[i]) {
      matches++;
    }
  }

  return parseFloat(((matches / maxLen) * 100).toFixed(2));
}
