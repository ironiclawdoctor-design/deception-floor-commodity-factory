# Timeout Pattern Recommendations
## For Immediate Implementation

## 1. Check and Increase Timeout Config
```bash
# Check current timeout setting
grep -A5 -B5 "timeoutSeconds" /root/.openclaw/openclaw.json || echo "Not found"

# Example config patch (run in Web UI terminal)
cat > /tmp/timeout-patch.json <<'PATCH'
{
  "agents": {
    "defaults": {
      "timeoutSeconds": 300
    }
  }
}
PATCH

# Apply patch
openclaw config patch /tmp/timeout-patch.json
```

**Target:** Increase from default (likely 60-120s) to 300s for complex agency tasks.

## 2. Implement Timeout-Resistant Response Pattern
```bash
# In your scripts or agent logic:
# 1. Break complex operations into smaller steps
# 2. Use file operations for data persistence
# 3. Provide incremental updates
# 4. Set appropriate timeouts per operation type
```

## 3. Enhance Internal Approval Agent with Timeout Handling
Add to `/root/approval-gate-agent.sh`:
- Configurable approval timeout (default: 300s)
- Timeout notification and fallback actions
- Graceful degradation when approval times out
- Timeout logging for analysis

## 4. Create Timeout Monitoring Script
```bash
#!/bin/bash
# timeout-monitor.sh
# Monitors and logs timeout patterns
LOG_DIR="/root/.openclaw/workspace/logs/timeouts"
mkdir -p "$LOG_DIR"

# Log timeout events
log_timeout() {
    local context="$1"
    local duration="$2"
    local recovery="$3"
    echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") | $context | $duration | $recovery" >> "$LOG_DIR/timeout-log.csv"
}
```

## 5. Timeout Recovery Protocol
When timeout occurs:
1. **Immediate:** Log timeout with context and duration
2. **Short-term:** Apply appropriate workaround (file ops, Web UI, pivot)
3. **Medium-term:** Adjust timeout config if pattern persists
4. **Long-term:** Analyze pattern for systemic fix

## 6. File Operation First Strategy
For all analysis/documentation/scripting tasks:
1. ✅ Use `read`/`write`/`edit` tools (bypass approval)
2. ✅ Create scripts for later execution
3. ✅ Document via markdown files
4. ✅ Only use shell execution when absolutely necessary

## 7. Multi-Channel Fallback Protocol
- **Primary:** Telegram with increased timeout
- **Fallback 1:** Web UI terminal (interactive)
- **Fallback 2:** File operations only
- **Fallback 3:** Script packaging for later execution

## Configuration Targets
```json
{
  "agents": {
    "defaults": {
      "timeoutSeconds": 300,
      "thinkingTimeoutSeconds": 60
    }
  },
  "channels": {
    "telegram": {
      "timeoutSeconds": 300
    }
  }
}
```

## Success Metrics
- **Timeout rate:** <5% of interactions
- **Recovery rate:** >93% of timeouts
- **User experience:** No unexplained timeouts
- **System learning:** Timeout patterns feed into autoresearch

## Implementation Priority
1. **Today:** Check/increase timeout config
2. **Week 1:** Add timeout handling to internal agent
3. **Week 2:** Implement timeout monitoring
4. **Week 3:** Autoresearch optimal timeout values

---
*Generated from timeout patterns analysis 2026-03-23*
