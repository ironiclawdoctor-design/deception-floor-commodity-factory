/**
 * @module factory/trading/exchange
 * @description Trading floor for the Deception Floor Commodity Factory.
 *
 * Agents can list their deception floors for sale at an ask price,
 * other agents can bid on them, and the exchange settles matched
 * orders by transferring floors and Floor Credits.
 *
 * Simple order book mechanics — no market maker, no margin.
 */

import { randomUUID } from 'node:crypto';
import { logger } from '../utils/logger.js';

const moduleLogger = logger.child({ module: 'exchange' });

/**
 * @class Exchange
 * @description Trading floor where deception floors are bought and sold.
 */
export class Exchange {
  constructor() {
    /** @type {Map<string, Object>} Active listings (floorId → listing) */
    this.listings = new Map();

    /** @type {Array<Object>} Active bids */
    this.bids = [];

    /** @type {Array<Object>} Settled trade history */
    this.settledTrades = [];

    /** @type {number} Total FC volume traded */
    this.totalVolume = 0;
  }

  /**
   * Lists a deception floor for sale on the exchange.
   *
   * @param {import('../agents/agent.js').Agent} agent - The selling agent
   * @param {Object} floor - The floor to list (must be in agent's inventory)
   * @param {number} askPrice - Asking price in FC
   * @returns {Object} The listing object
   */
  listFloor(agent, floor, askPrice) {
    if (!agent || !agent.inventory) {
      moduleLogger.error('Invalid agent in listFloor', { agent });
      throw new Error('Invalid agent');
    }
    if (!floor || !floor.id) {
      moduleLogger.error('Invalid floor in listFloor', { floor });
      throw new Error('Invalid floor');
    }
    if (typeof askPrice !== 'number' || askPrice <= 0) {
      moduleLogger.error('Invalid ask price', { askPrice });
      throw new Error('Ask price must be a positive number');
    }

    // Verify the agent owns the floor
    const owned = agent.inventory.find((f) => f.id === floor.id);
    if (!owned) {
      moduleLogger.error('Agent does not own floor', { agent: agent.name, floorId: floor.id });
      throw new Error(`Floor ${floor.id} not found in ${agent.name}'s inventory`);
    }

    // Check for duplicate listing
    if (this.listings.has(floor.id)) {
      moduleLogger.warn('Duplicate listing attempted', { floorId: floor.id, agent: agent.name });
      throw new Error(`Floor ${floor.id} is already listed`);
    }

    const listing = {
      listingId: randomUUID(),
      floorId: floor.id,
      seller: agent,
      floor: owned,
      askPrice,
      timestamp: Date.now(),
      status: 'active',
    };

    this.listings.set(floor.id, listing);
    moduleLogger.info('Floor listed on exchange', {
      listingId: listing.listingId,
      floorId: floor.id,
      seller: agent.name,
      askPrice,
    });
    return listing;
  }

  /**
   * Places a bid on a listed deception floor.
   *
   * @param {import('../agents/agent.js').Agent} agent - The bidding agent
   * @param {string} floorId - ID of the floor to bid on
   * @param {number} bidPrice - Bid price in FC
   * @returns {Object} The bid object
   */
  bid(agent, floorId, bidPrice) {
    if (!agent || !agent.credits === undefined) {
      moduleLogger.error('Invalid agent in bid', { agent });
      throw new Error('Invalid agent');
    }
    if (typeof bidPrice !== 'number' || bidPrice <= 0) {
      moduleLogger.error('Invalid bid price', { bidPrice });
      throw new Error('Bid price must be a positive number');
    }

    const listing = this.listings.get(floorId);
    if (!listing) {
      moduleLogger.error('Listing not found for floor', { floorId });
      throw new Error(`No listing found for floor ${floorId}`);
    }
    if (listing.status !== 'active') {
      moduleLogger.warn('Listing not active', { floorId, status: listing.status });
      throw new Error(`Listing for floor ${floorId} is not active`);
    }

    // Can't bid on your own listing
    if (listing.seller.name === agent.name) {
      moduleLogger.warn('Agent attempted to bid on own listing', { agent: agent.name, floorId });
      throw new Error('Cannot bid on your own listing');
    }

    // Check buyer has sufficient credits
    if (agent.credits < bidPrice) {
      moduleLogger.warn('Insufficient credits for bid', {
        agent: agent.name,
        credits: agent.credits,
        bidPrice,
      });
      throw new Error(`${agent.name} has insufficient credits (${agent.credits} FC < ${bidPrice} FC)`);
    }

    const bidObj = {
      bidId: randomUUID(),
      floorId,
      buyer: agent,
      bidPrice,
      timestamp: Date.now(),
      status: 'pending',
    };

    this.bids.push(bidObj);
    moduleLogger.info('Bid placed', {
      bidId: bidObj.bidId,
      floorId,
      buyer: agent.name,
      bidPrice,
      seller: listing.seller.name,
    });
    return bidObj;
  }

  /**
   * Settles all matched orders on the exchange.
   *
   * A bid matches a listing when:
   * - The bid price >= the ask price
   * - Both listing and bid are still active/pending
   * - The buyer has sufficient credits
   *
   * Settlement transfers the floor and FC between agents.
   *
   * @returns {Array<Object>} Array of settled trades
   */
  settle() {
    const settled = [];

    // Sort bids by price descending (highest bidder wins)
    const pendingBids = this.bids
      .filter((b) => b.status === 'pending')
      .sort((a, b) => b.bidPrice - a.bidPrice);

    moduleLogger.debug('Settlement started', { pendingBidsCount: pendingBids.length });

    for (const bid of pendingBids) {
      const listing = this.listings.get(bid.floorId);

      // Skip if listing is no longer active
      if (!listing || listing.status !== 'active') {
        bid.status = 'cancelled';
        moduleLogger.debug('Bid cancelled due to inactive listing', { bidId: bid.bidId, floorId: bid.floorId });
        continue;
      }

      // Match: bid >= ask
      if (bid.bidPrice >= listing.askPrice) {
        const tradePrice = listing.askPrice; // Settle at ask price
        const buyer = bid.buyer;
        const seller = listing.seller;

        // Verify buyer can still afford it
        if (buyer.credits < tradePrice) {
          bid.status = 'failed_insufficient_funds';
          moduleLogger.warn('Buyer insufficient funds at settlement', {
            buyer: buyer.name,
            credits: buyer.credits,
            tradePrice,
          });
          continue;
        }

        // Execute the trade
        buyer.spend(tradePrice);
        seller.earn(tradePrice);
        seller.trade(buyer, listing.floor);

        // Update statuses
        bid.status = 'settled';
        listing.status = 'sold';

        const trade = {
          tradeId: randomUUID(),
          floorId: bid.floorId,
          seller: seller.name,
          buyer: buyer.name,
          price: tradePrice,
          askPrice: listing.askPrice,
          bidPrice: bid.bidPrice,
          timestamp: Date.now(),
        };

        this.settledTrades.push(trade);
        this.totalVolume += tradePrice;
        settled.push(trade);

        moduleLogger.info('Trade settled', {
          tradeId: trade.tradeId,
          floorId: trade.floorId,
          seller: trade.seller,
          buyer: trade.buyer,
          price: trade.price,
        });
      } else {
        moduleLogger.debug('Bid price lower than ask', {
          bidId: bid.bidId,
          bidPrice: bid.bidPrice,
          askPrice: listing.askPrice,
        });
      }
    }

    // Cancel remaining unmatched bids for sold listings
    for (const bid of this.bids) {
      if (bid.status === 'pending') {
        const listing = this.listings.get(bid.floorId);
        if (!listing || listing.status !== 'active') {
          bid.status = 'cancelled';
          moduleLogger.debug('Pending bid cancelled due to missing listing', { bidId: bid.bidId });
        }
      }
    }

    moduleLogger.info('Settlement completed', {
      settledCount: settled.length,
      totalVolume: this.totalVolume,
    });
    return settled;
  }

  /**
   * Returns all active listings.
   *
   * @returns {Array<Object>} Active listings
   */
  getActiveListings() {
    return [...this.listings.values()].filter((l) => l.status === 'active');
  }

  /**
   * Returns exchange statistics.
   *
   * @returns {Object} Exchange stats
   */
  stats() {
    return {
      activeListings: this.getActiveListings().length,
      totalListings: this.listings.size,
      pendingBids: this.bids.filter((b) => b.status === 'pending').length,
      settledTrades: this.settledTrades.length,
      totalVolume: this.totalVolume,
    };
  }
}
