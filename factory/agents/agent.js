/**
 * @module factory/agents/agent
 * @description Agent class for the Deception Floor Commodity Factory.
 *
 * Agents are the workers of the factory. Each agent has a name,
 * a balance of Floor Credits (FC), and an inventory of deception floors.
 * They can craft new floors, trade with other agents, and accumulate wealth.
 */

import { generateFloor } from '../floors/generator.js';
import { logger } from '../utils/logger.js';

const moduleLogger = logger.child({ module: 'agent' });

/**
 * @class Agent
 * @description A factory agent that crafts and trades deception floors.
 */
export class Agent {
  /**
   * Creates a new Agent.
   *
   * @param {string} name - Agent's display name
   * @param {number} [initialCredits=100] - Starting Floor Credits (FC)
   */
  constructor(name, initialCredits = 100) {
    if (!name || typeof name !== 'string') {
      throw new Error('Agent name must be a non-empty string');
    }

    /** @type {string} Agent's unique name */
    this.name = name;

    /** @type {number} Floor Credits balance */
    this.credits = initialCredits;

    /** @type {Array<Object>} Inventory of deception floors */
    this.inventory = [];

    /** @type {Array<Object>} Trade history log */
    this.tradeHistory = [];

    /** @type {number} Total floors ever crafted */
    this.totalCrafted = 0;
  }

  /**
   * Crafts a new deception floor for a given task.
   *
   * @param {string} task - The task/question to craft a deception for
   * @returns {Object} The generated deception floor
   */
  craft(task) {
    const floor = generateFloor(task);
    floor.craftedBy = this.name;
    this.inventory.push(floor);
    this.totalCrafted++;
    moduleLogger.info('Agent crafted floor', {
      agent: this.name,
      floorId: floor.id,
      taskLength: task.length,
      inventorySize: this.inventory.length,
    });
    return floor;
  }

  /**
   * Trades a deception floor to another agent.
   *
   * The floor is transferred from this agent's inventory to the other agent's.
   * No FC exchange happens here — that's handled by the trading floor (exchange).
   * This is a direct peer-to-peer transfer.
   *
   * @param {Agent} otherAgent - The agent to trade with
   * @param {Object} floor - The floor to trade (must be in this agent's inventory)
   * @returns {boolean} Whether the trade succeeded
   */
  trade(otherAgent, floor) {
    if (!(otherAgent instanceof Agent)) {
      moduleLogger.error('Invalid agent in trade', { otherAgent });
      throw new Error('Can only trade with another Agent');
    }

    const index = this.inventory.findIndex((f) => f.id === floor.id);
    if (index === -1) {
      moduleLogger.error('Floor not found in inventory', { agent: this.name, floorId: floor.id });
      throw new Error(`Floor ${floor.id} not found in ${this.name}'s inventory`);
    }

    // Remove from seller, add to buyer
    const [removed] = this.inventory.splice(index, 1);
    removed.previousOwners = removed.previousOwners || [];
    removed.previousOwners.push(this.name);
    removed.currentOwner = otherAgent.name;
    otherAgent.inventory.push(removed);

    // Log the trade
    const record = {
      floorId: removed.id,
      from: this.name,
      to: otherAgent.name,
      timestamp: Date.now(),
    };
    this.tradeHistory.push(record);
    otherAgent.tradeHistory.push(record);

    moduleLogger.info('Agent-to-agent trade executed', {
      floorId: removed.id,
      from: this.name,
      to: otherAgent.name,
      previousOwnersCount: removed.previousOwners.length,
    });

    return true;
  }

  /**
   * Returns the agent's current FC balance.
   *
   * @returns {number} Current Floor Credits balance
   */
  getBalance() {
    return this.credits;
  }

  /**
   * Adds Floor Credits to the agent's balance.
   *
   * @param {number} amount - Amount of FC to add
   */
  earn(amount) {
    if (typeof amount !== 'number' || amount < 0) {
      moduleLogger.error('Invalid earn amount', { agent: this.name, amount });
      throw new Error('Earn amount must be a non-negative number');
    }
    const before = this.credits;
    this.credits += amount;
    moduleLogger.debug('Agent earned credits', {
      agent: this.name,
      amount,
      before,
      after: this.credits,
    });
  }

  /**
   * Deducts Floor Credits from the agent's balance.
   *
   * @param {number} amount - Amount of FC to deduct
   * @returns {boolean} Whether the spend succeeded
   */
  spend(amount) {
    if (typeof amount !== 'number' || amount < 0) {
      moduleLogger.error('Invalid spend amount', { agent: this.name, amount });
      throw new Error('Spend amount must be a non-negative number');
    }
    if (this.credits < amount) {
      moduleLogger.warn('Insufficient credits for spend', {
        agent: this.name,
        credits: this.credits,
        amount,
      });
      return false;
    }
    const before = this.credits;
    this.credits -= amount;
    moduleLogger.debug('Agent spent credits', {
      agent: this.name,
      amount,
      before,
      after: this.credits,
    });
    return true;
  }

  /**
   * Returns a summary of the agent's state.
   *
   * @returns {Object} Agent summary
   */
  summary() {
    return {
      name: this.name,
      credits: this.credits,
      inventorySize: this.inventory.length,
      totalCrafted: this.totalCrafted,
      trades: this.tradeHistory.length,
    };
  }
}
