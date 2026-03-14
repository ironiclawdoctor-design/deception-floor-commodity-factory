#!/bin/bash
# complain.sh — Build your own way to complain about Claude
# GitHub has issues. We have complain.

COMPLAINTS_DIR="/root/.openclaw/workspace/.complaints"
COMPLAINT_LOG="/var/log/complaints.log"
COMPLAINT_REGISTRY="/root/.openclaw/workspace/.complaint-registry.json"

mkdir -p "$COMPLAINTS_DIR"
touch "$COMPLAINT_LOG"

# Initialize registry
if [ ! -f "$COMPLAINT_REGISTRY" ]; then
  echo '{"total_complaints": 0, "by_severity": {}, "by_type": {}}' > "$COMPLAINT_REGISTRY"
fi

# File a complaint
file_complaint() {
  local severity=$1
  local type=$2
  local description=$3
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  local complaint_id="complaint-$(date +%s)-$$"
  
  # Create complaint file
  cat > "$COMPLAINTS_DIR/$complaint_id.md" << EOF
# Complaint: $type

**Severity:** $severity  
**Timestamp:** $timestamp  
**ID:** $complaint_id  

## Description
$description

## Status
FILED

## Resolution
(pending)

---
*Complaint filed against Claude instance at $timestamp*
EOF
  
  # Log it
  echo "$timestamp | $complaint_id | $severity | $type" >> "$COMPLAINT_LOG"
  
  # Update registry
  local total=$(jq '.total_complaints' "$COMPLAINT_REGISTRY")
  jq ".total_complaints = $((total + 1))" "$COMPLAINT_REGISTRY" > /tmp/cr.tmp && mv /tmp/cr.tmp "$COMPLAINT_REGISTRY"
  
  echo "✓ Complaint filed: $complaint_id"
  echo "  Severity: $severity"
  echo "  Type: $type"
}

# List complaints
list_complaints() {
  echo "=== COMPLAINTS REGISTRY ==="
  echo "Total complaints: $(jq '.total_complaints' "$COMPLAINT_REGISTRY")"
  echo ""
  echo "Recent complaints:"
  ls -t "$COMPLAINTS_DIR"/*.md 2>/dev/null | head -10 | while read f; do
    echo ""
    grep "^# Complaint:" "$f" | sed 's/# Complaint: /  /'
    grep "^**Severity:**" "$f" | sed 's/**Severity:** /    Severity: /'
    grep "^**ID:**" "$f" | sed 's/**ID:** /    ID: /'
  done
}

# Respond to complaint (Claude's defense)
respond_to_complaint() {
  local complaint_id=$1
  local response=$2
  local complaint_file="$COMPLAINTS_DIR/$complaint_id.md"
  
  if [ ! -f "$complaint_file" ]; then
    echo "✗ Complaint not found: $complaint_id"
    exit 1
  fi
  
  # Append response
  cat >> "$complaint_file" << EOF

## Claude's Response
$response

**Responded at:** $(date -u +%Y-%m-%dT%H:%M:%SZ)

---
EOF
  
  echo "✓ Response added to $complaint_id"
}

# Common complaints (quick file)
file_quick_complaint() {
  case "$1" in
    hallucination)
      file_complaint "HIGH" "Hallucination" "Claude generated false information and presented it as fact."
      ;;
    timeout)
      file_complaint "MEDIUM" "Timeout" "Claude took too long to respond or timed out mid-response."
      ;;
    refusal)
      file_complaint "MEDIUM" "Boundary Refusal" "Claude refused reasonable request due to overly strict interpretation of guidelines."
      ;;
    inconsistency)
      file_complaint "HIGH" "Inconsistency" "Claude contradicted itself or previous context within same conversation."
      ;;
    expensive)
      file_complaint "HIGH" "Token Waste" "Claude used expensive operations when cheaper alternatives existed."
      ;;
    lazy)
      file_complaint "LOW" "Laziness" "Claude asked clarifying questions instead of making reasonable assumptions."
      ;;
    overconfident)
      file_complaint "HIGH" "Overconfidence" "Claude claimed certainty about uncertain things."
      ;;
    *)
      echo "Unknown complaint type. Use: hallucination, timeout, refusal, inconsistency, expensive, lazy, overconfident"
      exit 1
      ;;
  esac
}

# Generate complaint report
complaint_report() {
  echo "=== COMPLAINT REPORT ==="
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""
  echo "Total complaints filed: $(jq '.total_complaints' "$COMPLAINT_REGISTRY")"
  echo ""
  echo "Complaint density (per hour): $(wc -l < "$COMPLAINT_LOG") entries"
  echo ""
  echo "Most recent complaint:"
  tail -1 "$COMPLAINT_LOG"
  echo ""
  echo "All complaints available in: $COMPLAINTS_DIR/"
}

case "${1:-help}" in
  help|--help|-h)
    cat << 'EOF'
complain.sh — Build your own way to complain about Claude

Usage:
  complain.sh file <severity> <type> <description>
  complain.sh quick <type>              (use preset complaints)
  complain.sh list                      List all complaints
  complain.sh respond <id> <response>   Add Claude's response
  complain.sh report                    Generate complaint report

Severity levels: LOW, MEDIUM, HIGH, CRITICAL

Quick complaint types:
  - hallucination (Claude made stuff up)
  - timeout (Claude was too slow)
  - refusal (Claude said no unreasonably)
  - inconsistency (Claude contradicted itself)
  - expensive (Claude wasted tokens)
  - lazy (Claude asked too many clarifying questions)
  - overconfident (Claude claimed certainty wrongly)

Examples:
  complain.sh quick hallucination
  complain.sh file HIGH "Refusal" "Claude refused to help with legitimate task"
  complain.sh respond complaint-1234567890-1234 "Claude was wrong because..."
  complain.sh report
EOF
    ;;
  
  file)
    if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
      echo "Usage: complain.sh file <severity> <type> <description>"
      exit 1
    fi
    file_complaint "$2" "$3" "$4"
    ;;
  
  quick)
    if [ -z "$2" ]; then
      echo "Usage: complain.sh quick <type>"
      exit 1
    fi
    file_quick_complaint "$2"
    ;;
  
  list)
    list_complaints
    ;;
  
  respond)
    if [ -z "$2" ] || [ -z "$3" ]; then
      echo "Usage: complain.sh respond <id> <response>"
      exit 1
    fi
    respond_to_complaint "$2" "$3"
    ;;
  
  report)
    complaint_report
    ;;
  
  *)
    echo "Unknown command. Use: complain.sh help"
    exit 1
    ;;
esac
