/**
 * @module factory/server/middleware
 * @description HTTP middleware stack for the Deception Floor Commodity Factory.
 *
 * Provides:
 * - Correlation ID injection (X‑Request‑ID or custom header)
 * - Structured request/response logging
 * - JSON body parsing
 * - CORS headers
 * - Central error handling
 *
 * All middleware adds a correlation ID to the request object (`req.correlationId`)
 * and logs each request with timing, status, and metadata.
 */

import { randomUUID } from 'node:crypto';
import express from 'express';
import cors from 'cors';
import { logger } from '../utils/logger.js';
import { FactoryError } from '../errors/index.js';
import { collector } from '../utils/metrics.js';

/**
 * Default correlation ID header name.
 */
const CORRELATION_HEADER = process.env.LOG_CORRELATION_HEADER || 'X-Request-ID';

/**
 * Middleware that injects a correlation ID into the request.
 * If the request already contains the configured header, that value is used;
 * otherwise a new UUIDv4 is generated.
 */
export function correlationIdMiddleware(req, res, next) {
  const incomingId = req.get(CORRELATION_HEADER) || randomUUID();
  req.correlationId = incomingId;
  // Set the header on the response for client tracing
  res.set(CORRELATION_HEADER, incomingId);
  next();
}

/**
 * Structured request logging middleware.
 * Logs the start and completion of each request with timing and metadata.
 */
export function requestLoggingMiddleware(req, res, next) {
  const startTime = Date.now();
  const { method, originalUrl, headers } = req;
  const userAgent = headers['user-agent'] || 'unknown';

  // Log request start (DEBUG level)
  logger.debug('Request started', {
    correlationId: req.correlationId,
    method,
    url: originalUrl,
    userAgent,
    ip: req.ip,
  });

  // Hook into response finish to log completion
  res.on('finish', () => {
    const durationMs = Date.now() - startTime;
    const { statusCode } = res;

    // Determine log level based on status code
    let level = 'INFO';
    if (statusCode >= 500) level = 'ERROR';
    else if (statusCode >= 400) level = 'WARN';

    logger.log(level, 'Request completed', {
      correlationId: req.correlationId,
      method,
      url: originalUrl,
      statusCode,
      durationMs,
      userAgent,
      ip: req.ip,
    });
  });

  next();
}

/**
 * JSON body parsing middleware (express.json).
 */
export const jsonBodyMiddleware = express.json();

/**
 * CORS middleware with sensible defaults.
 */
export const corsMiddleware = cors({
  origin: process.env.CORS_ORIGIN || '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', CORRELATION_HEADER],
});

/**
 * Global error‑handling middleware.
 * Catches any error thrown in route handlers, logs it, and returns a structured JSON response.
 */
export function errorHandlerMiddleware(err, req, res, next) {
  // Ensure the error is a FactoryError (or wrap it)
  let factoryError = err;
  if (!(err instanceof FactoryError)) {
    factoryError = new FactoryError(err.message || 'Internal server error', {
      status: err.status || 500,
      cause: err,
      correlationId: req.correlationId,
    });
  }

  // Ensure correlation ID is set from request if missing
  if (!factoryError.correlationId) {
    factoryError.correlationId = req.correlationId;
  }

  // Log the error with stack trace
  logger.errorWithStack(factoryError, 'Request error', {
    correlationId: factoryError.correlationId,
    url: req.originalUrl,
    method: req.method,
    statusCode: factoryError.status,
  });

  // Send JSON response (backward‑compatible shape)
  res.status(factoryError.status).json(factoryError.toJSON());
}

/**
 * Health check endpoint middleware.
 * Returns 200 OK with service status (useful for load balancers).
 */
export function healthCheckMiddleware(req, res, next) {
  if (req.path === '/health' || req.path === '/health/') {
    return res.status(200).json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      service: 'deception-floor-commodity-factory',
      version: process.env.npm_package_version || '0.1.0',
    });
  }
  next();
}

/**
 * Compose all middleware into a single function suitable for `app.use`.
 * Order matters:
 * 1. Correlation ID injection
 * 2. Request logging
 * 3. CORS
 * 4. JSON body parsing
 * 5. Health check (early exit)
 * 6. Routes (to be added later)
 * 7. Error handler (must be last)
 */
export function createMiddlewareStack() {
  const router = express.Router();

  router.use(correlationIdMiddleware);
  router.use(requestLoggingMiddleware);
  router.use(corsMiddleware);
  router.use(jsonBodyMiddleware);
  router.use(healthCheckMiddleware);

  // The actual routes will be mounted after this stack
  return router;
}

/**
 * Creates a complete Express application with the middleware stack and basic routes.
 * @param {Function} routeMount - Function that mounts routes onto the router
 * @returns {express.Application} Configured Express app
 */
export function createApp(routeMount) {
  const app = express();

  // Apply middleware stack
  app.use(createMiddlewareStack());

  // Mount routes (provided by caller)
  if (typeof routeMount === 'function') {
    routeMount(app);
  }

  // Global error handler (must be after routes)
  app.use(errorHandlerMiddleware);

  return app;
}