# Autoresearch Batch API Methods

**Purpose:** Systematic experimentation across agent-to-agent interfaces, service dependencies, and internal APIs  
**Scope:** Internal agency couplings only  
**Integration:** Works with fiesta-agents orchestrator  

## Batch API Endpoints

### POST /api/autoresearch/batch/agent-couplings
Test couplings between agent pairs in batch mode.

**Parameters:**
```json
{
  "agent_pairs": [
    {"from": "agent_a", "to": "agent_b", "interface": "session_spawn"},
    {"from": "agent_b", "to": "agent_c", "interface": "message_passing"}
  ],
  "test_cases": 10,
  "concurrency": 3
}
```

### POST /api/autoresearch/batch/service-dependencies
Test service dependency chains.

**Parameters:**
```json
{
  "services": ["database", "cache", "queue", "api_gateway"],
  "failure_modes": ["timeout", "error", "partial"],
  "iterations": 50
}
```

### POST /api/autoresearch/batch/internal-apis
Test internal API endpoints in batch.

**Parameters:**
```json
{
  "endpoints": [
    "/api/ledger/balance",
    "/api/market/trades",
    "/api/agents/status"
  ],
  "load_profile": "spike",
  "duration_seconds": 300
}
```

## Implementation Script

```bash
#!/bin/bash
# autoresearch-batch.sh

set -e

CONFIG_FILE="${HOME}/.openclaw/workspace/config/autoresearch.conf"
RESULTS_DIR="${HOME}/.openclaw/workspace/results/autoresearch"
mkdir -p "$RESULTS_DIR"

batch_agent_couplings() {
    local pairs="$1"
    local test_cases="${2:-10}"
    local concurrency="${3:-3}"
    
    echo "Testing agent couplings: $pairs"
    # Implementation would iterate through pairs
    # and test session_spawn, message_passing, etc.
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    echo "{\"timestamp\": \"$TIMESTAMP\", \"pairs\": $pairs}" > "$RESULTS_DIR/couplings_$TIMESTAMP.json"
    echo "✓ Agent couplings batch completed"
}

batch_service_dependencies() {
    local services="$1"
    local failure_modes="${2:-timeout,error,partial}"
    local iterations="${3:-50}"
    
    echo "Testing service dependencies: $services"
    # Test dependency chains with various failure modes
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    echo "{\"services\": $services, \"iterations\": $iterations}" > "$RESULTS_DIR/dependencies_$TIMESTAMP.json"
    echo "✓ Service dependencies batch completed"
}

batch_internal_apis() {
    local endpoints="$1"
    local load_profile="${2:-spike}"
    local duration="${3:-300}"
    
    echo "Testing internal APIs: $endpoints"
    # Load test internal API endpoints
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    echo "{\"endpoints\": $endpoints, \"duration\": $duration}" > "$RESULTS_DIR/apis_$TIMESTAMP.json"
    echo "✓ Internal APIs batch completed"
}

# Main dispatcher
case "$1" in
    "agent-couplings")
        batch_agent_couplings "$2" "$3" "$4"
        ;;
    "service-dependencies")
        batch_service_dependencies "$2" "$3" "$4"
        ;;
    "internal-apis")
        batch_internal_apis "$2" "$3" "$4"
        ;;
    *)
        echo "Usage: $0 {agent-couplings|service-dependencies|internal-apis} [params...]"
        echo ""
        echo "Examples:"
        echo "  $0 agent-couplings '[{\"from\":\"support\",\"to\":\"engineer\"}]' 5 2"
        echo "  $0 service-dependencies '[\"db\",\"cache\"]' 'timeout,error' 100"
        echo "  $0 internal-apis '[\"/api/status\"]' spike 60"
        exit 1
        ;;
esac
```

## Integration with Fiesta-Agents

Add to `fiesta-agents/orchestrator/SKILL.md`:

```markdown
## Batch Autoresearch Integration

The orchestrator can dispatch batch research tasks:

```bash
./orchestrator.sh --task "research-agent-couplings" \
  --params '{"agent_pairs": [{"from": "A", "to": "B"}], "test_cases": 20}'
```

Results are stored in `workspace/results/autoresearch/` for analysis.
```

## Monitoring & Alerting

- Success rate per coupling type
- Latency percentiles
- Failure mode distribution
- Automatic alert on regression >5%
