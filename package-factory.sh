#!/bin/bash
# package-factory.sh — Create downloadable zips

FACTORY_DIR="/root/.openclaw/workspace/deception-floor-commodity-factory"
WORKSPACE_DIR="/root/.openclaw/workspace"
OUTPUT_DIR="/tmp/packages"

mkdir -p "$OUTPUT_DIR"

echo "📦 Packaging factory..."
cd "$FACTORY_DIR"
zip -r "$OUTPUT_DIR/deception-floor-factory.zip" . \
  -x ".git/*" "node_modules/*" ".gitignore" "*.log" > /dev/null
echo "✓ Factory: $OUTPUT_DIR/deception-floor-factory.zip"

echo "📦 Packaging playbooks..."
cd "$WORKSPACE_DIR"
zip "$OUTPUT_DIR/agency-playbooks.zip" \
  FAMINE_PLAYBOOK.md \
  REVENUE_PLAYBOOK.md \
  SOVEREIGNTY_CHECKLIST.md \
  FAITH_DECISION_TREE.md \
  famine-watch.sh > /dev/null
echo "✓ Playbooks: $OUTPUT_DIR/agency-playbooks.zip"

echo "📦 Packaging firewall scripts..."
zip "$OUTPUT_DIR/agency-firewall.zip" \
  /usr/local/bin/agency-*.sh \
  FIREWALL-SURVIVAL-GUIDE.md \
  DAIMYO-IMPLEMENTATION.md > /dev/null 2>&1 || true
echo "✓ Firewall: $OUTPUT_DIR/agency-firewall.zip (if scripts exist)"

echo ""
echo "📥 Download from:"
ls -lh "$OUTPUT_DIR"/*.zip

echo ""
echo "📋 Contents:"
for zip in "$OUTPUT_DIR"/*.zip; do
  echo "  $(basename $zip):"
  unzip -l "$zip" | tail -3
done
