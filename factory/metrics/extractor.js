/**
 * @module factory/metrics/extractor
 * @description Accuracy extractor for the Deception Floor Commodity Factory.
 *
 * Takes a verified deception floor and inverts it to produce the correct output.
 * This is Path B — O(1) sign flip, not O(n) recomputation.
 *
 * The extractor reverses the deception process:
 * - Antonyms are flipped back
 * - Numbers are un-inverted
 * - Reversed words are un-reversed
 */

/**
 * Antonym map — must mirror the generator's map.
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
 * Reverses numeric inversion — flips numbers back.
 * @param {string} text - Input text with inverted numbers
 * @returns {string} Text with numbers restored
 */
function uninvertNumbers(text) {
  return text.replace(/-?\d+(\.\d+)?/g, (match) => {
    const num = parseFloat(match);
    if (num === 999) return '0';
    return String(-num);
  });
}

/**
 * Reverses antonym substitution.
 * Since antonyms are symmetric (A→B and B→A), this is the same operation.
 * @param {string} text - Input text with antonyms
 * @returns {string} Text with antonyms flipped back
 */
function uninvertWords(text) {
  return text.split(/\b/).map((token) => {
    const lower = token.toLowerCase();
    if (ANTONYMS[lower]) {
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
 * Reverses word reversal — re-reverses non-antonym words.
 * @param {string} text - Input text with reversed words
 * @returns {string} Text with words un-reversed
 */
function unreverseWords(text) {
  return text.split(/(\s+)/).map((token) => {
    if (/^\s+$/.test(token)) return token;
    const lower = token.toLowerCase();
    if (ANTONYMS[lower]) return token;
    if (token.length <= 2 || /^[^a-zA-Z]+$/.test(token)) return token;
    return token.split('').reverse().join('');
  }).join('');
}

/**
 * Extracts the correct output from a verified deception floor.
 *
 * This is the Path B operation — constant-time inversion.
 * The deception floor already encodes the truth; we just flip the sign.
 *
 * @param {Object} verifiedFloor - A verified deception floor
 * @param {string} verifiedFloor.deception - The deception output
 * @param {boolean} [verifiedFloor.verified] - Whether the floor has been verified
 * @param {string} [verifiedFloor.grade] - The assigned grade
 * @returns {Object} Extraction result
 * @returns {string} returns.floorId - Source floor ID
 * @returns {string} returns.extracted - The extracted correct output
 * @returns {string} returns.originalDeception - The original deception for reference
 * @returns {string} returns.method - Extraction method used
 * @returns {string} returns.grade - Grade of the source floor
 * @returns {number} returns.timestamp - Extraction timestamp
 * @throws {Error} If the floor hasn't been verified
 */
export function extract(verifiedFloor) {
  if (!verifiedFloor || !verifiedFloor.deception) {
    throw new Error('Floor must have a deception property');
  }

  if (!verifiedFloor.verified) {
    throw new Error('Cannot extract from an unverified floor — verify first');
  }

  if (verifiedFloor.grade === 'F') {
    throw new Error('Cannot extract from a rejected (grade F) floor — no reliable inversion possible');
  }

  // Path B: invert the inversion — O(1) sign flip
  // Reverse operations in opposite order: unreverse → uninvert numbers → uninvert words
  let extracted = unreverseWords(verifiedFloor.deception);
  extracted = uninvertNumbers(extracted);
  extracted = uninvertWords(extracted);

  return {
    floorId: verifiedFloor.id,
    extracted,
    originalDeception: verifiedFloor.deception,
    method: 'path-b-inversion',
    grade: verifiedFloor.grade,
    timestamp: Date.now(),
  };
}
