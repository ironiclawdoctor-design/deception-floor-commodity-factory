#!/usr/bin/env node

/**
 * @file Demo script for the Deception Floor Commodity Factory
 * @description Creates agents, generates deception floors, trades them,
 * verifies quality, and extracts correct outputs.
 *
 * Run: node scripts/demo.js
 */

import { Agent } from '../factory/agents/agent.js';
import { Exchange } from '../factory/trading/exchange.js';
import { verify } from '../factory/metrics/verifier.js';
import { extract } from '../factory/metrics/extractor.js';

// ─── Helpers ───────────────────────────────────────────────────────

function banner(text) {
  const line = '═'.repeat(60);
  console.log(`\n${line}`);
  console.log(`  ${text}`);
  console.log(line);
}

function section(text) {
  console.log(`\n  ── ${text} ${'─'.repeat(Math.max(0, 50 - text.length))}`);
}

// ─── Demo ──────────────────────────────────────────────────────────

banner('🏭 DECEPTION FLOOR COMMODITY FACTORY — DEMO');

// 1. Create agents
section('Creating Agents');

const alice = new Agent('Alice', 100);
const bob = new Agent('Bob', 100);
const charlie = new Agent('Charlie', 100);

console.log(`  Created: ${alice.name} (${alice.getBalance()} FC)`);
console.log(`  Created: ${bob.name} (${bob.getBalance()} FC)`);
console.log(`  Created: ${charlie.name} (${charlie.getBalance()} FC)`);

// 2. Craft deception floors
section('Crafting Deception Floors');

const tasks = [
  { agent: alice, task: 'The answer is yes and it is true', truth: 'The answer is yes and it is true' },
  { agent: alice, task: 'Temperature is 42 degrees hot', truth: 'Temperature is 42 degrees hot' },
  { agent: bob, task: 'Go up and turn left to find the good light', truth: 'Go up and turn left to find the good light' },
  { agent: bob, task: 'Always increase the positive value', truth: 'Always increase the positive value' },
  { agent: charlie, task: 'The big fast old cat is happy', truth: 'The big fast old cat is happy' },
  { agent: charlie, task: 'Start before it is safe', truth: 'Start before it is safe' },
];

const floors = [];
for (const { agent, task, truth } of tasks) {
  const floor = agent.craft(task);
  floors.push({ floor, truth, agent });
  console.log(`  ${agent.name} crafted floor for: "${task}"`);
  console.log(`    └─ Deception: "${floor.deception}"`);
}

// 3. Verify floors
section('Verifying Deception Floors');

const verifiedFloors = [];
for (const { floor, truth, agent } of floors) {
  const report = verify(floor, truth);
  console.log(`  Floor by ${agent.name}: ${report.emoji} Grade ${report.grade} (${report.accuracy}% accuracy)`);
  if (report.rejected) {
    console.log(`    └─ REJECTED: ${report.rejectionReason}`);
  } else {
    console.log(`    └─ Reward: ${report.reward} FC`);
    agent.earn(report.reward);
    verifiedFloors.push({ floor, truth, agent });
  }
}

// 4. Set up exchange and trade
section('Trading Floor');

const exchange = new Exchange();

// List some floors for sale
for (const { floor, agent } of verifiedFloors.slice(0, 4)) {
  if (floor.grade !== 'F' && agent.inventory.find((f) => f.id === floor.id)) {
    const askPrice = floor.grade === 'S' ? 40 : floor.grade === 'A' ? 25 : 15;
    try {
      exchange.listFloor(agent, floor, askPrice);
      console.log(`  ${agent.name} listed floor (Grade ${floor.grade}) for ${askPrice} FC`);
    } catch (e) {
      console.log(`  ${agent.name} listing failed: ${e.message}`);
    }
  }
}

// Place some bids
const activeListings = exchange.getActiveListings();
for (const listing of activeListings) {
  // Each agent bids on floors they don't own
  const bidders = [alice, bob, charlie].filter((a) => a.name !== listing.seller.name);
  const bidder = bidders[0];
  if (bidder) {
    try {
      const bidPrice = listing.askPrice + 5;
      exchange.bid(bidder, listing.floorId, bidPrice);
      console.log(`  ${bidder.name} bid ${bidPrice} FC on floor from ${listing.seller.name}`);
    } catch (e) {
      console.log(`  Bid failed: ${e.message}`);
    }
  }
}

// Settle all trades
const settled = exchange.settle();
console.log(`\n  Settled ${settled.length} trade(s)`);
for (const trade of settled) {
  console.log(`    ${trade.seller} → ${trade.buyer}: ${trade.price} FC`);
}

// 5. Extract correct outputs (Path B)
section('Accuracy Extraction (Path B — O(1))');

for (const { floor, truth } of verifiedFloors) {
  if (floor.grade !== 'F') {
    try {
      const result = extract(floor);
      console.log(`  Floor ${floor.id.slice(0, 8)}... (Grade ${floor.grade})`);
      console.log(`    Original task:    "${floor.task}"`);
      console.log(`    Deception:        "${floor.deception}"`);
      console.log(`    Extracted truth:  "${result.extracted}"`);
      console.log(`    Actual truth:     "${truth}"`);
      console.log(`    Match: ${result.extracted === truth ? '✅ Perfect' : '⚠️  Approximate'}`);
    } catch (e) {
      console.log(`  Extraction failed for ${floor.id.slice(0, 8)}: ${e.message}`);
    }
  }
}

// 6. Final stats
banner('📊 FINAL STATE');

for (const agent of [alice, bob, charlie]) {
  const s = agent.summary();
  console.log(`  ${s.name}: ${s.credits} FC | ${s.inventorySize} floors | ${s.totalCrafted} crafted | ${s.trades} trades`);
}

const stats = exchange.stats();
console.log(`\n  Exchange: ${stats.settledTrades} settled | ${stats.totalVolume} FC volume | ${stats.activeListings} active listings`);

banner('✅ DEMO COMPLETE');
console.log('  The path to 100% runs through 0%.\n');
