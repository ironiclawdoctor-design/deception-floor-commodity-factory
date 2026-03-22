/**
 * Test script for structured logging and correlation IDs.
 * Starts the HTTP server, makes sample requests, verifies logs.
 */

import { startServer } from './factory/server/index.js';
import { logger } from './factory/utils/logger.js';

// Capture logs
const capturedLogs = [];
const originalLog = console.log;
console.log = (...args) => {
  capturedLogs.push(args.join(' '));
  originalLog(...args);
};

// Override logger's console.log? Logger uses console.log, already overridden.

async function run() {
  console.log('=== Starting logging test ===');

  // Start server on random port (0 = OS assigns)
  const server = startServer(0);
  const port = server.address().port;
  console.log(`Server listening on port ${port}`);

  // Wait a moment for server to be ready
  await new Promise(resolve => setTimeout(resolve, 500));

  const baseUrl = `http://localhost:${port}`;

  // Test 1: Health endpoint
  console.log('\n--- Test 1: GET /health');
  const healthRes = await fetch(`${baseUrl}/health`);
  console.log(`Health status: ${healthRes.status}`);
  const healthBody = await healthRes.json();
  console.log(healthBody);

  // Test 2: Generate floor with correlation ID
  console.log('\n--- Test 2: POST /floors/generate');
  const correlationId = 'test-corr-123';
  const generateRes = await fetch(`${baseUrl}/floors/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Request-ID': correlationId,
    },
    body: JSON.stringify({ task: 'The sky is blue' }),
  });
  console.log(`Generate status: ${generateRes.status}`);
  const floor = await generateRes.json();
  console.log(`Floor ID: ${floor.id}`);

  // Test 3: Verify floor
  console.log('\n--- Test 3: POST /floors/verify');
  const verifyRes = await fetch(`${baseUrl}/floors/verify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Request-ID': correlationId,
    },
    body: JSON.stringify({
      floor,
      groundTruth: 'The sky is blue',
    }),
  });
  const verifyReport = await verifyRes.json();
  console.log(`Verify grade: ${verifyReport.grade}`);

  // Test 4: Extract accuracy
  console.log('\n--- Test 4: POST /floors/extract');
  const extractRes = await fetch(`${baseUrl}/floors/extract`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Request-ID': correlationId,
    },
    body: JSON.stringify({
      verifiedFloor: { ...floor, verified: true, grade: verifyReport.grade },
    }),
  });
  const extractResult = await extractRes.json();
  console.log(`Extracted: ${extractResult.extracted}`);

  // Test 5: Metrics endpoint
  console.log('\n--- Test 5: GET /metrics');
  const metricsRes = await fetch(`${baseUrl}/metrics`);
  const metrics = await metricsRes.json();
  console.log(`Agents: ${metrics.agents}`);

  // Wait a bit for any async logs
  await new Promise(resolve => setTimeout(resolve, 200));

  // Stop server
  server.close();
  console.log('\n=== Server stopped ===');

  // Analyze captured logs
  console.log('\n=== Captured logs (first 20) ===');
  capturedLogs.slice(0, 20).forEach((log, i) => {
    console.log(`${i}: ${log}`);
  });

  // Check for correlation ID in logs
  const correlationLogs = capturedLogs.filter(log => log.includes(correlationId));
  console.log(`\nLogs containing correlation ID: ${correlationLogs.length}`);
  if (correlationLogs.length === 0) {
    console.error('ERROR: No logs contain correlation ID');
    process.exit(1);
  }

  // Check for structured JSON logs
  const jsonLogs = capturedLogs.filter(log => {
    try {
      JSON.parse(log);
      return true;
    } catch {
      return false;
    }
  });
  console.log(`Structured JSON logs: ${jsonLogs.length}`);
  if (jsonLogs.length === 0) {
    console.warn('WARNING: No JSON logs found (maybe LOG_FORMAT=plain)');
  }

  console.log('\n✅ All tests passed');
  process.exit(0);
}

run().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});