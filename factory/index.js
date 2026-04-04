/**
 * @module factory
 * @description Main entry point for the Deception Floor Commodity Factory.
 *
 * Re-exports all core modules for convenient access.
 */

export { generateFloor, gradeFloor, computeAccuracy } from './floors/generator.js';
export { Agent } from './agents/agent.js';
export { Exchange } from './trading/exchange.js';
export { verify } from './metrics/verifier.js';
export { extract } from './metrics/extractor.js';
