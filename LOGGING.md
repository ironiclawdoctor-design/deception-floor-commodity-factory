# Structured Logging & Observability

## Overview

The Deception Floor Commodity Factory backend implements structured logging with correlation IDs, enabling production debugging, audit trails, and real‑time anomaly detection. All logs are emitted as JSON lines, ready for ingestion by log aggregators (ELK, Splunk, Datadog, etc.).

## Key Features

- **Unique correlation IDs** for every request (injected via `X‑Request‑ID` header)
- **Structured JSON logs** with consistent fields (timestamp, level, module, correlationId, message, metadata)
- **Request/response logging** with method, URL, status, duration, user agent
- **Log levels** (DEBUG, INFO, WARN, ERROR) configurable via environment
- **Performance metrics** (response times, error rates) exposed via `/metrics` endpoint
- **Audit trails** for security events (login attempts, admin actions)
- **Integration with error handling** (correlation IDs flow from HTTP requests to errors)
- **Future‑proof** for distributed tracing (OpenTelemetry)

## Log Schema

Every log entry contains the following base fields:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 string | UTC time when the event occurred |
| `level` | string | Log level: `DEBUG`, `INFO`, `WARN`, `ERROR` |
| `message` | string | Human‑readable description of the event |
| `module` | string (optional) | Source module (`generator`, `verifier`, `exchange`, `agent`, etc.) |
| `correlationId` | string (optional) | Unique ID tying together all logs for a single request |
| `metadata` | object (optional) | Context‑specific key‑value pairs (e.g., `floorId`, `agent`, `durationMs`) |

Additional fields may appear depending on the log type (see examples below).

## Configuration

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `LOG_LEVEL` | `INFO` | Minimum log level: `DEBUG`, `INFO`, `WARN`, `ERROR` |
| `LOG_FORMAT` | `json` | Output format: `json` (structured) or `plain` (human‑readable) |
| `LOG_CORRELATION_HEADER` | `X‑Request‑ID` | HTTP header used for correlation ID propagation |
| `PORT` | `3000` | HTTP server port |

### Example .env file

```bash
LOG_LEVEL=DEBUG
LOG_FORMAT=json
LOG_CORRELATION_HEADER=X-Request-ID
PORT=3000
```

## Usage

### Importing the Logger

```js
import { logger } from './factory/utils/logger.js';

// Default logger (no module/correlation ID)
logger.info('System started');

// Create a child logger with module name
const moduleLogger = logger.child({ module: 'generator' });
moduleLogger.debug('Processing task', { taskLength: 42 });

// Create a child logger with correlation ID (for request‑scoped logging)
const requestLogger = logger.child({ module: 'api', correlationId: 'req-123' });
requestLogger.info('Request received');
```

### Logging in Modules

Each core module has its own child logger (e.g., `moduleLogger`). Use the appropriate log level:

- **DEBUG**: Detailed internal state (e.g., “Generating deception floor”, “Bid placed”)
- **INFO**: Business‑level events (e.g., “Floor generated”, “Trade settled”)
- **WARN**: Potentially problematic situations (e.g., “Duplicate listing attempted”)
- **ERROR**: Failures that require attention (e.g., “Invalid input”, “Dependency failure”)

### Logging Errors

Use `logger.errorWithStack(error, message?, metadata?)` to log an error with its stack trace:

```js
try {
  riskyOperation();
} catch (err) {
  logger.errorWithStack(err, 'Risky operation failed', { userId: 42 });
}
```

### HTTP Request Logging

Every HTTP request is automatically logged with:

- Start (DEBUG level) when the request arrives
- Completion (INFO/WARN/ERROR depending on status code) when the response is sent

Example log entry for a successful request:

```json
{
  "timestamp": "2025‑03‑18T21:45:12.123Z",
  "level": "INFO",
  "message": "Request completed",
  "correlationId": "550e8400‑e29b‑41d4‑a716‑446655440000",
  "method": "POST",
  "url": "/floors/generate",
  "statusCode": 201,
  "durationMs": 24,
  "userAgent": "curl/7.68.0",
  "ip": "::1"
}
```

## Correlation IDs

### Propagation

1. **Incoming request**: If the request contains the `X‑Request‑ID` header, its value is used as the correlation ID; otherwise a new UUIDv4 is generated.
2. **Response**: The same correlation ID is sent back in the `X‑Request‑ID` response header.
3. **Downstream calls**: The correlation ID is stored in `req.correlationId` and should be passed to any external service calls (future extension).
4. **Errors**: Any error thrown during request processing inherits the request’s correlation ID.

### Tracing

With correlation IDs, you can trace a single request across all logs:

```bash
grep '550e8400‑e29b‑41d4‑a716‑446655440000' factory.log
```

## Performance Metrics

The `/metrics` endpoint provides basic operational metrics:

```bash
curl http://localhost:3000/metrics
```

Returns:

```json
{
  "uptime": 1234.5,
  "memory": { "rss": 123456, "heapTotal": 987654, "heapUsed": 543210 },
  "agents": 5,
  "exchange": { "activeListings": 3, "settledTrades": 12, "totalVolume": 450 },
  "timestamp": "2025‑03‑18T21:45:12.123Z"
}
```

## Audit Trails

Security‑relevant events are logged at `INFO` level with explicit metadata:

- Agent creation (`agent`, `initialCredits`)
- Floor listing (`listingId`, `seller`, `askPrice`)
- Trade settlement (`tradeId`, `seller`, `buyer`, `price`)
- Authentication attempts (future)

## Querying Logs

### With `jq`

If logs are written to a file (`factory.log`), use `jq` for powerful filtering:

```bash
# Show all ERROR logs
cat factory.log | jq 'select(.level == "ERROR")'

# Show logs for a specific correlation ID
cat factory.log | jq 'select(.correlationId == "req‑123")'

# Show request logs that took longer than 100ms
cat factory.log | jq 'select(.durationMs != null and .durationMs > 100)'
```

### With ELK/Splunk

Index the JSON logs directly; all fields are searchable.

## Alerting Recommendations

Set up alerts based on log patterns:

- **Error rate**: Alert if more than 5 errors per minute.
- **Slow requests**: Alert if any request takes longer than 2 seconds.
- **Security events**: Alert on repeated authentication failures.
- **Business metrics**: Alert if trade volume drops below threshold.

## Future Extensions

- **OpenTelemetry integration**: Replace custom correlation IDs with W3C Trace Context.
- **Log aggregation**: Ship logs to Loki, Elasticsearch, or cloud logging services.
- **Structured logging in frontend**: Extend correlation IDs to browser sessions.
- **Advanced metrics**: Integrate Prometheus for real‑time monitoring.

## Example Workflow

1. Client sends `POST /floors/generate` with `X‑Request‑ID: abc123`.
2. Middleware injects `correlationId = abc123` into `req`.
3. Generator module logs `DEBUG` event with `correlationId`.
4. Response is logged with duration and status.
5. Error (if any) includes same `correlationId`.
6. All logs for this request can be retrieved via `grep abc123`.

## Best Practices

- **Do not log sensitive data** (passwords, tokens, personal information).
- **Use appropriate log levels**: DEBUG for development, INFO for production.
- **Keep metadata small**; avoid logging large objects.
- **Use child loggers** with module names for easier filtering.
- **Test log output** in staging to verify structure and completeness.

## Troubleshooting

### No logs appear
- Check `LOG_LEVEL` (maybe set to `ERROR` while logging `INFO`).
- Verify `LOG_FORMAT` is `json` (if expecting JSON lines).

### Correlation ID missing in module logs
- Ensure you are using a child logger that inherits `correlationId` from the request context.
- In HTTP handlers, use `req.correlationId` to create a child logger.

### Logs are not JSON
- Set `LOG_FORMAT=json` (default). If `plain` is set, logs are human‑readable.

### Performance overhead
- Logger is designed for low overhead; DEBUG logs are skipped when level is higher.
- Consider increasing `LOG_LEVEL` to `INFO` in production.