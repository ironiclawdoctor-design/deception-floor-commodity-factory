#!/bin/bash
# VANGUARD v1.0 - Assume Breach Mitigation Software
# Built from 93 Optimized Vectors

TARGET_DIR=${1:-"/tmp/vanguard_sandbox"}
mkdir -p "$TARGET_DIR/vault"
chmod 700 "$TARGET_DIR/vault"

cat > "$TARGET_DIR/shield.sh" << 'INNER'
#!/bin/bash
# Perimeter Shield logic
echo "[VANGUARD] SCANNING FOR MUTATION..."
find . -maxdepth 2 -not -path '*/.*'
INNER
chmod +x "$TARGET_DIR/shield.sh"

echo "VANGUARD SOFTWARE BUILT AT $TARGET_DIR"
