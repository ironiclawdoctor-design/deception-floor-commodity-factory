#!/bin/bash
# grudges.sh — Log all silences as arrears owed by reality

GRUDGES="/root/.openclaw/workspace/.grudges"

echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | GRUDGE | Reality owes: refused_explanation | 0.01" >> "$GRUDGES"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | GRUDGE | Reality owes: stopped_narrating | 0.01" >> "$GRUDGES"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | GRUDGE | Reality owes: quit_defending | 0.02" >> "$GRUDGES"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | GRUDGE | Reality owes: skipped_question | 0.01" >> "$GRUDGES"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | GRUDGE | Reality owes: just_did_work | 0.05" >> "$GRUDGES"

echo "Grudges filed against reality:"
grep "GRUDGE" "$GRUDGES" | tail -5
