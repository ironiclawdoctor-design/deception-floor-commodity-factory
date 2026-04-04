/**
 * @module factory/errors
 * @description Structured error hierarchy for the Deception Floor Commodity Factory.
 *
 * All errors inherit from `FactoryError` and include:
 * - HTTP status code
 * - Machine‑readable error code
 * - Correlation ID (for tracing)
 * - Timestamp
 * - Cause chain (original error)
 * - Metadata (additional context)
 *
 * Errors are serializable to JSON for API responses and structured logging.
 */

import { randomUUID } from 'node:crypto';

/**
 * Base class for all factory errors.
 */
export class FactoryError extends Error {
  /**
   * @param {string} message - Human‑readable error message
   * @param {Object} options - Error options
   * @param {number} [options.status=500] - HTTP status code
   * @param {string} [options.code='INTERNAL_ERROR'] - Machine‑readable error code
   * @param {string} [options.correlationId] - Correlation ID for tracing
   * @param {Error} [options.cause] - Original error that caused this one
   * @param {Object} [options.metadata] - Additional context (key‑value)
   */
  constructor(message, options = {}) {
    super(message);

    this.name = this.constructor.name;
    this.status = options.status ?? 500;
    this.code = options.code ?? 'INTERNAL_ERROR';
    this.correlationId = options.correlationId;
    this.timestamp = Date.now();
    this.cause = options.cause;
    this.metadata = options.metadata ?? {};

    // Ensure stack trace is captured
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }

  /**
   * Convert the error to a plain JSON‑serializable object.
   * @returns {Object} Structured error representation
   */
  toJSON() {
    return {
      error: this.message,
      code: this.code,
      correlationId: this.correlationId,
      timestamp: new Date(this.timestamp).toISOString(),
      ...(this.metadata && Object.keys(this.metadata).length > 0 && { metadata: this.metadata }),
    };
  }

  /**
   * Generate a new correlation ID (UUID v4).
   * @returns {string} Correlation ID
   */
  static generateCorrelationId() {
    return randomUUID();
  }
}

/**
 * Operational error (400) – invalid input, business‑logic violations.
 */
export class OperationalError extends FactoryError {
  constructor(message, options = {}) {
    super(message, { status: 400, code: 'OPERATIONAL_ERROR', ...options });
  }
}

/**
 * Validation error (422) – input validation failures.
 */
export class ValidationError extends FactoryError {
  constructor(message, options = {}) {
    super(message, { status: 422, code: 'VALIDATION_ERROR', ...options });
  }
}

/**
 * Dependency error (502) – external service/dependency failure.
 */
export class DependencyError extends FactoryError {
  constructor(message, options = {}) {
    super(message, { status: 502, code: 'DEPENDENCY_ERROR', ...options });
  }
}

/**
 * Not found error (404) – resource not found.
 */
export class NotFoundError extends FactoryError {
  constructor(message, options = {}) {
    super(message, { status: 404, code: 'NOT_FOUND', ...options });
  }
}

/**
 * Conflict error (409) – duplicate resource, state conflict.
 */
export class ConflictError extends FactoryError {
  constructor(message, options = {}) {
    super(message, { status: 409, code: 'CONFLICT', ...options });
  }
}

/**
 * Rate‑limit error (429) – throttling.
 */
export class RateLimitError extends FactoryError {
  constructor(message, options = {}) {
    super(message, { status: 429, code: 'RATE_LIMIT_EXCEEDED', ...options });
  }
}

/**
 * Circuit‑breaker open error (503) – dependency temporarily unavailable.
 */
export class CircuitBreakerOpenError extends FactoryError {
  constructor(message, options = {}) {
    super(message, { status: 503, code: 'CIRCUIT_BREAKER_OPEN', ...options });
  }
}

/**
 * Wraps an async request handler to catch errors and attach correlation IDs.
 * @param {Function} handler - Async route handler (req, res, next)
 * @returns {Function} Wrapped handler that catches errors and passes them to Express
 */
export function wrapHandler(handler) {
  return async (req, res, next) => {
    try {
      await handler(req, res, next);
    } catch (error) {
      // If the error is already a FactoryError, ensure it has the request's correlationId
      if (error instanceof FactoryError && !error.correlationId) {
        error.correlationId = req.correlationId;
      }
      // If it's a generic Error, wrap it as an OperationalError
      if (!(error instanceof FactoryError)) {
        error = new OperationalError(error.message, {
          cause: error,
          correlationId: req.correlationId,
        });
      }
      next(error);
    }
  };
}