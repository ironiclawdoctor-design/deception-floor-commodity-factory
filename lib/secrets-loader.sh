#!/bin/bash
# secrets-loader.sh — Secure credential loader for all agents
# Usage: source secrets-loader.sh && load_secret "twitter-api" "bearer_token"

set -euo pipefail

SECRETS_DIR="${SECRETS_DIR:-./.secrets}"
AUDIT_LOG="${AUDIT_LOG:-./.secrets/audit.log}"

# Load a secret value safely
# Args: secret_name, key_path (optional, returns whole object if not provided)
load_secret() {
    local secret_name="$1"
    local key_path="${2:-}"
    local secret_file="$SECRETS_DIR/${secret_name}.json"

    if [[ ! -f "$secret_file" ]]; then
        echo "ERROR: Secret file not found: $secret_file" >&2
        return 1
    fi

    # Check file permissions (must be 600 or 400)
    local perms=$(stat -c %a "$secret_file" 2>/dev/null || stat -f %OLp "$secret_file" 2>/dev/null)
    if [[ ! "$perms" =~ ^[46]00$ ]]; then
        echo "ERROR: Secret file has unsafe permissions ($perms). Must be 600 or 400." >&2
        return 1
    fi

    # Load and parse
    if [[ -z "$key_path" ]]; then
        # Return entire JSON object
        cat "$secret_file"
    else
        # Return specific key value using jq
        jq -r ".${key_path}" "$secret_file" 2>/dev/null || {
            echo "ERROR: Failed to extract key '$key_path' from $secret_file" >&2
            return 1
        }
    fi

    # Audit log (append, never rotate)
    echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] LOAD $secret_name ${key_path:-(full)} by $(whoami)@$(hostname)" >> "$AUDIT_LOG"
}

# Rotate credentials (mark old ones, require manual creation of new)
rotate_secret() {
    local secret_name="$1"
    local secret_file="$SECRETS_DIR/${secret_name}.json"

    if [[ ! -f "$secret_file" ]]; then
        echo "ERROR: Secret file not found: $secret_file" >&2
        return 1
    fi

    local backup_file="${secret_file}.rotated-$(date -u +'%Y%m%dT%H%M%SZ')"
    cp "$secret_file" "$backup_file"
    chmod 400 "$backup_file"  # Read-only after rotation

    echo "✅ Secret rotated. Backup: $backup_file"
    echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] ROTATE $secret_name by $(whoami)@$(hostname)" >> "$AUDIT_LOG"
}

# List all secret files (without content)
list_secrets() {
    echo "Available secrets in $SECRETS_DIR:"
    ls -lhA "$SECRETS_DIR"/*.json 2>/dev/null | awk '{print $9, "(" $5 ")"}'  || echo "  (none)"
    echo ""
    echo "Audit log (last 10 loads):"
    tail -n 10 "$AUDIT_LOG" 2>/dev/null || echo "  (no audit log yet)"
}

export -f load_secret rotate_secret list_secrets
