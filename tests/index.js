/**
 * @file Test suite for the Deception Floor Commodity Factory
 * @description Uses Node.js built-in test runner (node:test)
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import { generateFloor, gradeFloor, computeAccuracy } from '../factory/floors/generator.js';
import { Agent } from '../factory/agents/agent.js';
import { Exchange } from '../factory/trading/exchange.js';
import { verify } from '../factory/metrics/verifier.js';
import { extract } from '../factory/metrics/extractor.js';

// ─── Generator Tests ───────────────────────────────────────────────

describe('generator', () => {
  describe('generateFloor()', () => {
    it('should generate a valid deception floor', () => {
      const floor = generateFloor('The sky is blue');
      assert.ok(floor.id, 'Floor should have an ID');
      assert.equal(floor.task, 'The sky is blue');
      assert.ok(floor.deception, 'Floor should have a deception');
      assert.notEqual(floor.deception, floor.task, 'Deception should differ from task');
      assert.ok(floor.timestamp > 0, 'Should have a timestamp');
      assert.equal(floor.grade, null, 'Grade should be null before verification');
      assert.equal(floor.accuracy, null, 'Accuracy should be null before verification');
      assert.equal(floor.method, 'antonym+numeric+structural');
    });

    it('should invert antonyms', () => {
      const floor = generateFloor('yes true good');
      // "yes" → "no", "true" → "false", "good" → "bad"
      assert.ok(floor.deception.includes('no'), 'Should contain "no" for "yes"');
      assert.ok(floor.deception.includes('false'), 'Should contain "false" for "true"');
      assert.ok(floor.deception.includes('bad'), 'Should contain "bad" for "good"');
    });

    it('should invert numbers', () => {
      const floor = generateFloor('Temperature is 42 degrees');
      assert.ok(floor.deception.includes('-42'), 'Should negate 42 to -42');
    });

    it('should throw on empty task', () => {
      assert.throws(() => generateFloor(''), /non-empty string/);
      assert.throws(() => generateFloor(null), /non-empty string/);
    });
  });

  describe('gradeFloor()', () => {
    it('should grade a floor against truth', () => {
      const floor = generateFloor('yes');
      const grade = gradeFloor(floor, 'completely different truth text here');
      assert.ok(['S', 'A', 'B', 'C', 'F'].includes(grade));
      assert.ok(floor.accuracy !== null, 'Accuracy should be set after grading');
      assert.ok(floor.grade !== null, 'Grade should be set after grading');
    });

    it('should grade S for completely different output', () => {
      const floor = { deception: 'abcdefghijklmnop' };
      const grade = gradeFloor(floor, 'zyxwvutsrqponmlk');
      // These share no positional characters so accuracy ~0%
      assert.equal(grade, 'S');
    });

    it('should grade F for identical output', () => {
      const floor = { deception: 'the answer is yes' };
      const grade = gradeFloor(floor, 'the answer is yes');
      assert.equal(grade, 'F');
      assert.equal(floor.accuracy, 100);
    });
  });

  describe('computeAccuracy()', () => {
    it('should return 100 for identical strings', () => {
      assert.equal(computeAccuracy('hello', 'hello'), 100);
    });

    it('should return 0 for completely different strings', () => {
      const acc = computeAccuracy('abc', 'xyz');
      assert.equal(acc, 0);
    });

    it('should be case-insensitive', () => {
      assert.equal(computeAccuracy('Hello', 'hello'), 100);
    });

    it('should handle different lengths', () => {
      const acc = computeAccuracy('ab', 'abcd');
      // 2 matches out of 4 = 50%
      assert.equal(acc, 50);
    });
  });
});

// ─── Agent Tests ───────────────────────────────────────────────────

describe('Agent', () => {
  it('should create an agent with defaults', () => {
    const agent = new Agent('TestAgent');
    assert.equal(agent.name, 'TestAgent');
    assert.equal(agent.credits, 100);
    assert.deepEqual(agent.inventory, []);
    assert.deepEqual(agent.tradeHistory, []);
  });

  it('should create an agent with custom credits', () => {
    const agent = new Agent('Rich', 500);
    assert.equal(agent.credits, 500);
  });

  it('should throw on invalid name', () => {
    assert.throws(() => new Agent(''), /non-empty string/);
    assert.throws(() => new Agent(null), /non-empty string/);
  });

  it('should craft a deception floor', () => {
    const agent = new Agent('Crafter');
    const floor = agent.craft('What is 2+2?');
    assert.equal(agent.inventory.length, 1);
    assert.equal(floor.craftedBy, 'Crafter');
    assert.equal(agent.totalCrafted, 1);
  });

  it('should trade a floor to another agent', () => {
    const alice = new Agent('Alice');
    const bob = new Agent('Bob');
    const floor = alice.craft('Test task');

    assert.equal(alice.inventory.length, 1);
    assert.equal(bob.inventory.length, 0);

    alice.trade(bob, floor);

    assert.equal(alice.inventory.length, 0);
    assert.equal(bob.inventory.length, 1);
    assert.equal(bob.inventory[0].currentOwner, 'Bob');
  });

  it('should throw when trading a floor not in inventory', () => {
    const alice = new Agent('Alice');
    const bob = new Agent('Bob');
    const fakeFloor = { id: 'nonexistent' };
    assert.throws(() => alice.trade(bob, fakeFloor), /not found/);
  });

  it('should return balance via getBalance()', () => {
    const agent = new Agent('Banker', 250);
    assert.equal(agent.getBalance(), 250);
  });

  it('should earn and spend credits', () => {
    const agent = new Agent('Worker');
    agent.earn(50);
    assert.equal(agent.credits, 150);

    const ok = agent.spend(100);
    assert.equal(ok, true);
    assert.equal(agent.credits, 50);

    const fail = agent.spend(200);
    assert.equal(fail, false);
    assert.equal(agent.credits, 50);
  });

  it('should return a summary', () => {
    const agent = new Agent('Summary');
    agent.craft('task 1');
    const summary = agent.summary();
    assert.equal(summary.name, 'Summary');
    assert.equal(summary.inventorySize, 1);
    assert.equal(summary.totalCrafted, 1);
  });
});

// ─── Exchange Tests ────────────────────────────────────────────────

describe('Exchange', () => {
  it('should list a floor for sale', () => {
    const exchange = new Exchange();
    const seller = new Agent('Seller');
    const floor = seller.craft('Task for sale');

    const listing = exchange.listFloor(seller, floor, 25);
    assert.ok(listing.listingId);
    assert.equal(listing.askPrice, 25);
    assert.equal(listing.status, 'active');
  });

  it('should not list a floor not in inventory', () => {
    const exchange = new Exchange();
    const agent = new Agent('Faker');
    assert.throws(
      () => exchange.listFloor(agent, { id: 'fake' }, 10),
      /not found/
    );
  });

  it('should place a bid', () => {
    const exchange = new Exchange();
    const seller = new Agent('Seller');
    const buyer = new Agent('Buyer');
    const floor = seller.craft('Bid task');

    exchange.listFloor(seller, floor, 20);
    const bid = exchange.bid(buyer, floor.id, 25);
    assert.ok(bid.bidId);
    assert.equal(bid.bidPrice, 25);
    assert.equal(bid.status, 'pending');
  });

  it('should not allow bidding on own listing', () => {
    const exchange = new Exchange();
    const seller = new Agent('SelfBidder');
    const floor = seller.craft('Self bid');
    exchange.listFloor(seller, floor, 10);

    assert.throws(
      () => exchange.bid(seller, floor.id, 15),
      /Cannot bid on your own/
    );
  });

  it('should settle matched orders', () => {
    const exchange = new Exchange();
    const seller = new Agent('Seller', 100);
    const buyer = new Agent('Buyer', 100);
    const floor = seller.craft('Tradeable');

    exchange.listFloor(seller, floor, 20);
    exchange.bid(buyer, floor.id, 25);

    const settled = exchange.settle();
    assert.equal(settled.length, 1);
    assert.equal(settled[0].price, 20); // Settles at ask price
    assert.equal(seller.credits, 120); // 100 + 20
    assert.equal(buyer.credits, 80);   // 100 - 20
    assert.equal(buyer.inventory.length, 1);
    assert.equal(seller.inventory.length, 0);
  });

  it('should not settle if bid < ask', () => {
    const exchange = new Exchange();
    const seller = new Agent('Seller');
    const buyer = new Agent('Buyer');
    const floor = seller.craft('Overpriced');

    exchange.listFloor(seller, floor, 50);
    exchange.bid(buyer, floor.id, 10);

    const settled = exchange.settle();
    assert.equal(settled.length, 0);
  });

  it('should report stats', () => {
    const exchange = new Exchange();
    const stats = exchange.stats();
    assert.equal(stats.activeListings, 0);
    assert.equal(stats.totalVolume, 0);
  });
});

// ─── Verifier Tests ────────────────────────────────────────────────

describe('verifier', () => {
  it('should verify a well-crafted floor', () => {
    const floor = generateFloor('The answer is yes and it is true');
    const report = verify(floor, 'Something completely different here now');

    assert.equal(report.verified, true);
    assert.ok(report.accuracy !== null || report.rejected);
    assert.ok(['S', 'A', 'B', 'C', 'F'].includes(report.grade));
    assert.ok(report.timestamp > 0);
  });

  it('should reject lazy/empty submissions', () => {
    const floor = {
      id: 'lazy-1',
      task: 'What is the meaning of life?',
      deception: 'a',
    };
    const report = verify(floor, 'The meaning of life is complex');
    assert.equal(report.rejected, true);
    assert.equal(report.grade, 'F');
    assert.ok(report.rejectionReason);
  });

  it('should reject repetitive submissions', () => {
    const floor = {
      id: 'rep-1',
      task: 'Explain quantum physics',
      deception: 'abcabcabcabcabcabc',
    };
    const report = verify(floor, 'Quantum physics is the study of matter');
    assert.equal(report.rejected, true);
    assert.ok(report.rejectionReason.includes('Repetitive'));
  });

  it('should assign reward based on grade', () => {
    const floor = generateFloor('yes true good high');
    const report = verify(floor, 'zzzzzzzzzzzzzzzzz');
    assert.ok(report.reward >= 0);
  });

  it('should throw on invalid inputs', () => {
    assert.throws(() => verify(null, 'truth'), /must have deception/);
    assert.throws(
      () => verify({ deception: 'x', task: 'y', id: '1' }, ''),
      /non-empty string/
    );
  });
});

// ─── Extractor Tests ───────────────────────────────────────────────

describe('extractor', () => {
  it('should extract correct output from a verified floor', () => {
    const floor = generateFloor('yes true good');
    // Manually verify it
    floor.verified = true;
    floor.grade = 'A';

    const result = extract(floor);
    assert.ok(result.extracted);
    assert.equal(result.method, 'path-b-inversion');
    assert.equal(result.grade, 'A');
    assert.ok(result.timestamp > 0);
  });

  it('should reconstruct the original from inversion', () => {
    const original = 'yes true good';
    const floor = generateFloor(original);
    floor.verified = true;
    floor.grade = 'S';

    const result = extract(floor);
    // The extracted text should closely match the original
    // (exact match for pure antonym inversions)
    assert.equal(result.extracted, original);
  });

  it('should throw on unverified floor', () => {
    const floor = generateFloor('test');
    assert.throws(() => extract(floor), /unverified/);
  });

  it('should throw on rejected (grade F) floor', () => {
    const floor = generateFloor('test');
    floor.verified = true;
    floor.grade = 'F';
    assert.throws(() => extract(floor), /rejected/);
  });

  it('should handle numeric inversion round-trip', () => {
    const floor = generateFloor('The temperature is 42');
    floor.verified = true;
    floor.grade = 'B';

    const result = extract(floor);
    assert.ok(result.extracted.includes('42'), 'Should restore the original number');
  });
});
