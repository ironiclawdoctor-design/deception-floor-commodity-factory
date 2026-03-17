#!/bin/bash
# EMERGENCY TOKEN USAGE FREEZE
# Disables ALL external LLM consult regardless of "complex system directive" classification
# Tier: 0 | Cost: $0.00 | Enforcement: Absolute

echo "[0] EMERGENCY FREEZE INITIATED"

# 1) Process-level kill (immediate)
echo "[1] Killing external LLM processes..."
pkill -9 -f "claude|haiku|opus|openai|anthropic|gpt" 2>/dev/null || true

# 2) Network-level block (iptables if available)
if command -v iptables &> /dev/null; then
    echo "[2] Blocking external LLM endpoints..."
    iptables -A OUTPUT -d api.anthropic.com -j DROP 2>/dev/null || true
    iptables -A OUTPUT -d api.openai.com -j DROP 2>/dev/null || true
    iptables -A OUTPUT -d api.ampere.sh -j DROP 2>/dev/null || true
fi

# 3) DNS-level block (hosts file)
echo "[3] DNS blocking external endpoints..."
cat >> /etc/hosts << 'HOSTS'
0.0.0.0 api.anthropic.com
0.0.0.0 api.openai.com
0.0.0.0 api.ampere.sh
0.0.0.0 openrouter.ai
HOSTS

# 4) Config-level routing (BitNet only)
echo "[4] Configuring BitNet-only routing..."
mkdir -p /root/.openclaw
cat > /root/.openclaw/openclaw.json << 'CONFIG'
{
  "models": {
    "providers": {
      "bitnet": {
        "baseUrl": "http://127.0.0.1:8080/v1",
        "api": "openai",
        "models": [{"id": "bitnet-local", "name": "BitNet Sovereign", "costInput": 0, "costOutput": 0}]
      }
    },
    "default": "bitnet-local"
  },
  "agents": {
    "defaults": {
      "model": {"primary": "bitnet-local"}
    }
  },
  "env": {
    "ANTHROPIC_API_KEY": "DISABLED_BY_FREEZE",
    "AMPERE_API_KEY": "DISABLED_BY_FREEZE"
  }
}
CONFIG

# 5) Cron enforcement (persistent)
echo "[5] Installing persistent enforcement..."
(crontab -l 2>/dev/null; echo "*/1 * * * * pkill -9 -f 'claude|haiku|opus|openai' || true") | crontab -

# 6) Verification
echo "[6] VERIFICATION:"
curl -s http://127.0.0.1:8080/v1/models 2>/dev/null | head -1 && echo "  ✓ BitNet: ACTIVE" || echo "  ✗ BitNet: DOWN"
ps aux | grep -E "claude|haiku|opus|openai" | grep -v grep || echo "  ✓ External LLM: NONE RUNNING"

echo ""
echo "=========================================="
echo "  EXTERNAL LLM FREEZE: ACTIVE"
echo "  All consults → BitNet {-1,0,1} only"
echo "  Cost: $0.00 eternal"
echo "=========================================="
