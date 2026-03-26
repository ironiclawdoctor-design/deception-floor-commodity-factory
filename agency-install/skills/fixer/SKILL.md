---
name: fixer
description: Industry-standard error fixing skill. Wraps all agency API calls with schema validation, exponential backoff, idempotency, dry-run mode, and error classification. Apply to any script that hits external APIs. Converts one-shot scripts into resilient services.
version: 1.0.0
author: Fiesta
tags: [reliability, api, retry, backoff, idempotency, standards]
---

# Fixer — Industry Standard Resilience Layer

## Standards Applied
- **RFC 7807** — Problem Details for HTTP APIs (structured errors)
- **AWS retry logic** — exponential backoff with jitter
- **Google API Design Guide** — idempotency, resource validation
- **OpenAPI 3.0** — schema validation before send
- **Circuit breaker pattern** — fail fast, recover gracefully

## Classes of Failure
| Class | Retry? | Example |
|-------|--------|---------|
| SCHEMA | Never | Wrong tag format, missing field |
| AUTH | Never | 401, 403 |
| NOT_FOUND | Never | 404 |
| RATE_LIMIT | Yes, backoff | 429 |
| SERVER | Yes, 3x | 500, 502, 503 |
| NETWORK | Yes, 3x | timeout, connection refused |
| UNKNOWN | Once | anything else |

## Usage
```python
from skills.fixer.core import resilient_post, validate_schema

# Wrap any API call
result = resilient_post(url, payload, headers, schema=HASHNODE_SCHEMA)
```
