/**
 * @module factory/server
 * @description HTTP server for the Deception Floor Commodity Factory.
 *
 * Exposes REST APIs for:
 * - Generating deception floors
 * - Verifying floors against ground truth
 * - Extracting correct outputs from verified floors
 * - Trading floors between agents
 * - Agent management
 *
 * All requests are logged with correlation IDs, structured JSON logs,
 * and performance metrics.
 */

import { createApp } from './middleware.js';
import { logger } from '../utils/logger.js';
import { generateFloor, gradeFloor, computeAccuracy } from '../floors/generator.js';
import { verify } from '../metrics/verifier.js';
import { extract } from '../metrics/extractor.js';
import { Exchange } from '../trading/exchange.js';
import { Agent } from '../agents/agent.js';
import { FactoryError, wrapHandler } from '../errors/index.js';

// Create in‑memory instances (for demo)
const exchange = new Exchange();
const agents = new Map(); // name → Agent

/**
 * Ensure an agent exists (create if missing).
 */
function getOrCreateAgent(name, initialCredits = 100) {
  if (!agents.has(name)) {
    const agent = new Agent(name, initialCredits);
    agents.set(name, agent);
    logger.info(`Created new agent`, { agent: name, initialCredits });
  }
  return agents.get(name);
}

/**
 * Mount all API routes onto the Express app.
 */
function mountRoutes(app) {
  const router = app; // app is already a Router from middleware stack

  // ─── Health endpoint (already handled by middleware) ──────────────

  // ─── Metrics endpoint (performance monitoring) ─────────────────────
  router.get('/metrics', (req, res) => {
    // Basic metrics (to be extended with real metrics collection)
    const metrics = {
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      agents: agents.size,
      exchange: exchange.stats(),
      timestamp: new Date().toISOString(),
    };
    res.json(metrics);
  });

  // ─── Floor generation ──────────────────────────────────────────────
  router.post('/floors/generate', wrapHandler(async (req, res) => {
    const { task } = req.body;
    if (!task || typeof task !== 'string') {
      throw new FactoryError('Task must be a non‑empty string', {
        status: 400,
        code: 'VALIDATION_ERROR',
        correlationId: req.correlationId,
      });
    }

    const floor = generateFloor(task);
    logger.info('Floor generated', {
      correlationId: req.correlationId,
      floorId: floor.id,
      taskLength: task.length,
      method: floor.method,
    });

    res.status(201).json(floor);
  }));

  // ─── Floor verification ────────────────────────────────────────────
  router.post('/floors/verify', wrapHandler(async (req, res) => {
    const { floor, groundTruth } = req.body;
    if (!floor || !floor.deception || !floor.task) {
      throw new FactoryError('Floor must have deception and task properties', {
        status: 400,
        code: 'VALIDATION_ERROR',
        correlationId: req.correlationId,
      });
    }
    if (!groundTruth || typeof groundTruth !== 'string') {
      throw new FactoryError('Ground truth must be a non‑empty string', {
        status: 400,
        code: 'VALIDATION_ERROR',
        correlationId: req.correlationId,
      });
    }

    const report = verify(floor, groundTruth);
    logger.info('Floor verified', {
      correlationId: req.correlationId,
      floorId: floor.id,
      grade: report.grade,
      accuracy: report.accuracy,
      rejected: report.rejected,
    });

    res.json(report);
  }));

  // ─── Accuracy extraction ───────────────────────────────────────────
  router.post('/floors/extract', wrapHandler(async (req, res) => {
    const { verifiedFloor } = req.body;
    if (!verifiedFloor || !verifiedFloor.deception) {
      throw new FactoryError('Verified floor must have a deception property', {
        status: 400,
        code: 'VALIDATION_ERROR',
        correlationId: req.correlationId,
      });
    }

    const result = extract(verifiedFloor);
    logger.info('Accuracy extracted', {
      correlationId: req.correlationId,
      floorId: result.floorId,
      grade: result.grade,
      method: result.method,
    });

    res.json(result);
  }));

  // ─── Agent creation ────────────────────────────────────────────────
  router.post('/agents', wrapHandler(async (req, res) => {
    const { name, initialCredits } = req.body;
    if (!name || typeof name !== 'string') {
      throw new FactoryError('Agent name must be a non‑empty string', {
        status: 400,
        code: 'VALIDATION_ERROR',
        correlationId: req.correlationId,
      });
    }

    if (agents.has(name)) {
      throw new FactoryError(`Agent '${name}' already exists`, {
        status: 409,
        code: 'CONFLICT',
        correlationId: req.correlationId,
      });
    }

    const agent = new Agent(name, initialCredits || 100);
    agents.set(name, agent);
    logger.info('Agent created', {
      correlationId: req.correlationId,
      agent: name,
      initialCredits: agent.credits,
    });

    res.status(201).json(agent.summary());
  }));

  // ─── Agent details ─────────────────────────────────────────────────
  router.get('/agents/:name', wrapHandler(async (req, res) => {
    const agent = agents.get(req.params.name);
    if (!agent) {
      throw new FactoryError(`Agent '${req.params.name}' not found`, {
        status: 404,
        code: 'NOT_FOUND',
        correlationId: req.correlationId,
      });
    }
    res.json(agent.summary());
  }));

  // ─── Floor crafting (by an agent) ──────────────────────────────────
  router.post('/agents/:name/craft', wrapHandler(async (req, res) => {
    const agent = agents.get(req.params.name);
    if (!agent) {
      throw new FactoryError(`Agent '${req.params.name}' not found`, {
        status: 404,
        code: 'NOT_FOUND',
        correlationId: req.correlationId,
      });
    }
    const { task } = req.body;
    if (!task || typeof task !== 'string') {
      throw new FactoryError('Task must be a non‑empty string', {
        status: 400,
        code: 'VALIDATION_ERROR',
        correlationId: req.correlationId,
      });
    }

    const floor = agent.craft(task);
    logger.info('Agent crafted floor', {
      correlationId: req.correlationId,
      agent: agent.name,
      floorId: floor.id,
      taskLength: task.length,
    });

    res.status(201).json(floor);
  }));

  // ─── Exchange listing ──────────────────────────────────────────────
  router.post('/exchange/list', wrapHandler(async (req, res) => {
    const { agentName, floorId, askPrice } = req.body;
    const agent = agents.get(agentName);
    if (!agent) {
      throw new FactoryError(`Agent '${agentName}' not found`, {
        status: 404,
        correlationId: req.correlationId,
      });
    }
    const floor = agent.inventory.find(f => f.id === floorId);
    if (!floor) {
      throw new FactoryError(`Floor ${floorId} not found in agent's inventory`, {
        status: 404,
        correlationId: req.correlationId,
      });
    }

    const listing = exchange.listFloor(agent, floor, askPrice);
    logger.info('Floor listed on exchange', {
      correlationId: req.correlationId,
      agent: agent.name,
      floorId,
      askPrice,
      listingId: listing.listingId,
    });

    res.status(201).json(listing);
  }));

  // ─── Exchange bid ──────────────────────────────────────────────────
  router.post('/exchange/bid', wrapHandler(async (req, res) => {
    const { agentName, floorId, bidPrice } = req.body;
    const agent = agents.get(agentName);
    if (!agent) {
      throw new FactoryError(`Agent '${agentName}' not found`, {
        status: 404,
        correlationId: req.correlationId,
      });
    }

    const bid = exchange.bid(agent, floorId, bidPrice);
    logger.info('Bid placed', {
      correlationId: req.correlationId,
      agent: agent.name,
      floorId,
      bidPrice,
      bidId: bid.bidId,
    });

    res.status(201).json(bid);
  }));

  // ─── Exchange settle ───────────────────────────────────────────────
  router.post('/exchange/settle', wrapHandler(async (req, res) => {
    const settled = exchange.settle();
    logger.info('Exchange settled', {
      correlationId: req.correlationId,
      settledCount: settled.length,
    });
    res.json({ settled });
  }));

  // ─── Exchange stats ────────────────────────────────────────────────
  router.get('/exchange/stats', (req, res) => {
    res.json(exchange.stats());
  });

  // ─── Catch‑all 404 ─────────────────────────────────────────────────
  router.use('*', (req, res) => {
    throw new FactoryError(`Endpoint ${req.method} ${req.originalUrl} not found`, {
      status: 404,
      code: 'NOT_FOUND',
      correlationId: req.correlationId,
    });
  });
}

/**
 * Start the HTTP server.
 * @param {number} port - Port to listen on (default 3000)
 * @returns {import('http').Server} HTTP server instance
 */
export function startServer(port = 3000) {
  const app = createApp(mountRoutes);

  const server = app.listen(port, () => {
    logger.info('Server started', {
      port,
      pid: process.pid,
      nodeVersion: process.version,
      logLevel: process.env.LOG_LEVEL || 'INFO',
      correlationHeader: process.env.LOG_CORRELATION_HEADER || 'X-Request-ID',
    });
  });

  // Graceful shutdown
  const shutdown = (signal) => {
    logger.info(`Received ${signal}, shutting down gracefully`);
    server.close(() => {
      logger.info('Server closed');
      process.exit(0);
    });
    // Force shutdown after 10 seconds
    setTimeout(() => {
      logger.error('Forced shutdown after timeout');
      process.exit(1);
    }, 10000).unref();
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));

  return server;
}

// If this file is executed directly, start the server
if (process.argv[1] === new URL(import.meta.url).pathname) {
  const port = parseInt(process.env.PORT || '3000', 10);
  startServer(port);
}