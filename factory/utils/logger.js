/**
 * @module factory/utils/logger
 * @description Structured JSON logger for the Deception Floor Commodity Factory.
 *
 * Logs are emitted as JSON lines, ready for ingestion by log aggregators (ELK, Splunk, etc.).
 * Supports log levels (DEBUG, INFO, WARN, ERROR), correlation IDs, module names, and metadata.
 *
 * Configuration via environment variables:
 * - LOG_LEVEL: minimum log level (DEBUG, INFO, WARN, ERROR) – default INFO
 * - LOG_FORMAT: 'json' (default) or 'plain' (human-readable)
 * - LOG_CORRELATION_HEADER: HTTP header name for correlation ID (default X-Request-ID)
 *
 * Usage:
 *   import { logger } from './utils/logger.js';
 *   logger.info('Message', { metadata });
 *   const child = logger.child({ module: 'generator', correlationId: 'req-123' });
 *   child.debug('Detailed debug info', { input });
 */

import process from 'node:process';

// Log level precedence
const LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
};

const LEVEL_NAMES = Object.keys(LEVELS);

/**
 * Get current log level from environment.
 */
function getConfiguredLevel() {
  const envLevel = (process.env.LOG_LEVEL || 'INFO').toUpperCase();
  return LEVELS[envLevel] !== undefined ? LEVELS[envLevel] : LEVELS.INFO;
}

/**
 * Get log format from environment.
 */
function getLogFormat() {
  return (process.env.LOG_FORMAT || 'json').toLowerCase();
}

/**
 * Format timestamp as ISO 8601.
 */
function timestamp() {
  return new Date().toISOString();
}

/**
 * Core logger class.
 */
class Logger {
  constructor(defaultFields = {}) {
    this.defaultFields = { ...defaultFields };
    this.level = getConfiguredLevel();
    this.format = getLogFormat();
  }

  /**
   * Create a child logger with additional default fields.
   * @param {Object} fields - Fields to add to every log entry (module, correlationId, etc.)
   * @returns {Logger} Child logger instance
   */
  child(fields) {
    return new Logger({ ...this.defaultFields, ...fields });
  }

  /**
   * Log a message if the given level is enabled.
   * @param {string} level - Log level (DEBUG, INFO, WARN, ERROR)
   * @param {string} message - Human-readable message
   * @param {Object} metadata - Additional key-value pairs
   */
  log(level, message, metadata = {}) {
    const levelValue = LEVELS[level];
    if (levelValue === undefined) {
      // Fallback to INFO for unknown levels
      this.log('INFO', message, metadata);
      return;
    }
    if (levelValue < this.level) {
      return; // Level disabled
    }

    const entry = {
      timestamp: timestamp(),
      level,
      message,
      ...this.defaultFields,
      ...metadata,
    };

    // Ensure correlationId is present if provided in defaults (allow override)
    if (this.defaultFields.correlationId && !metadata.correlationId) {
      entry.correlationId = this.defaultFields.correlationId;
    }

    // Remove undefined values
    Object.keys(entry).forEach(key => entry[key] === undefined && delete entry[key]);

    if (this.format === 'plain') {
      // Human-readable format (still includes key fields)
      const parts = [
        entry.timestamp,
        `[${entry.level}]`,
        entry.module ? `(${entry.module})` : '',
        entry.correlationId ? `{${entry.correlationId}}` : '',
        message,
      ];
      console.log(parts.filter(Boolean).join(' '));
      if (Object.keys(metadata).length > 0) {
        console.log('  ', JSON.stringify(metadata, null, 0));
      }
    } else {
      // JSON format (one line)
      console.log(JSON.stringify(entry));
    }
  }

  debug(message, metadata) {
    this.log('DEBUG', message, metadata);
  }

  info(message, metadata) {
    this.log('INFO', message, metadata);
  }

  warn(message, metadata) {
    this.log('WARN', message, metadata);
  }

  error(message, metadata) {
    this.log('ERROR', message, metadata);
  }

  /**
   * Log an error object with stack trace.
   * @param {Error} error - Error instance
   * @param {string} message - Optional context message
   * @param {Object} metadata - Additional metadata
   */
  errorWithStack(error, message = '', metadata = {}) {
    this.log('ERROR', message || error.message, {
      error: {
        message: error.message,
        name: error.name,
        stack: error.stack,
        ...(error.correlationId && { correlationId: error.correlationId }),
        ...(error.code && { code: error.code }),
        ...(error.status && { status: error.status }),
      },
      ...metadata,
    });
  }

  /**
   * Log request start/end with timing.
   * @param {string} correlationId - Request correlation ID
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {number} startTime - Performance timestamp
   * @param {number} statusCode - HTTP status code
   * @param {string} userAgent - User-Agent header
   * @param {Object} extra - Additional fields (userId, agentId, etc.)
   */
  requestLog(correlationId, method, url, startTime, statusCode, userAgent, extra = {}) {
    const durationMs = Date.now() - startTime;
    this.info('Request completed', {
      correlationId,
      method,
      url,
      statusCode,
      durationMs,
      userAgent,
      ...extra,
    });
  }
}

// Default logger instance (no default fields)
const logger = new Logger();

export { logger, Logger };