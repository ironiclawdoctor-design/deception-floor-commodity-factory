/**
 * @module factory/utils/metrics
 * @description Simple in‑memory metrics collector for request/response performance.
 *
 * Tracks:
 * - Total requests
 * - Requests by HTTP method
 * - Requests by status code (2xx, 3xx, 4xx, 5xx)
 * - Response time percentiles (p50, p90, p99)
 * - Error rates
 *
 * Metrics are aggregated per process lifetime (reset on restart).
 */

class MetricsCollector {
  constructor() {
    this.reset();
  }

  reset() {
    this.startTime = Date.now();
    this.requestCount = 0;
    this.requestsByMethod = {};
    this.requestsByStatus = {};
    this.responseTimes = []; // store durations for percentile calculation
    this.errors4xx = 0;
    this.errors5xx = 0;
  }

  /**
   * Record a completed HTTP request.
   * @param {string} method - HTTP method
   * @param {number} statusCode - HTTP status code
   * @param {number} durationMs - Response duration in milliseconds
   */
  recordRequest(method, statusCode, durationMs) {
    this.requestCount++;
    this.requestsByMethod[method] = (this.requestsByMethod[method] || 0) + 1;
    const statusClass = `${Math.floor(statusCode / 100)}xx`;
    this.requestsByStatus[statusClass] = (this.requestsByStatus[statusClass] || 0) + 1;

    // Store duration for percentiles (keep last 1000 samples for memory)
    this.responseTimes.push(durationMs);
    if (this.responseTimes.length > 1000) {
      this.responseTimes.shift();
    }

    if (statusCode >= 400 && statusCode < 500) {
      this.errors4xx++;
    } else if (statusCode >= 500) {
      this.errors5xx++;
    }
  }

  /**
   * Compute percentiles from stored response times.
   * @param {number[]} sorted - Sorted array of durations
   * @param {number} p - Percentile (0‑100)
   * @returns {number} Percentile value
   */
  percentile(sorted, p) {
    if (sorted.length === 0) return 0;
    const index = Math.ceil((p / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
  }

  /**
   * Get current metrics snapshot.
   * @returns {Object} Metrics object
   */
  getMetrics() {
    const sorted = [...this.responseTimes].sort((a, b) => a - b);
    const uptime = (Date.now() - this.startTime) / 1000;

    return {
      uptime,
      requestCount: this.requestCount,
      requestsByMethod: { ...this.requestsByMethod },
      requestsByStatus: { ...this.requestsByStatus },
      responseTime: {
        min: sorted.length ? Math.min(...sorted) : 0,
        max: sorted.length ? Math.max(...sorted) : 0,
        mean: sorted.length ? sorted.reduce((a, b) => a + b, 0) / sorted.length : 0,
        p50: this.percentile(sorted, 50),
        p90: this.percentile(sorted, 90),
        p99: this.percentile(sorted, 99),
      },
      errors: {
        '4xx': this.errors4xx,
        '5xx': this.errors5xx,
        errorRate: this.requestCount ? (this.errors4xx + this.errors5xx) / this.requestCount : 0,
      },
    };
  }
}

// Singleton instance
export const collector = new MetricsCollector();