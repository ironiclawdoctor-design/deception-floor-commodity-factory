#!/bin/bash
# Feed Fiesta outputs to BitNet for deception floor commodity training
# Cost: $0.00 | Tier 0

INPUT_FILE="$1"
OUTPUT_DIR="/root/.openclaw/workspace/deception-floor-commodity-augments"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

if [ -z "$INPUT_FILE" ]; then
    echo "Usage: $0 <input-file> [--hallucination|--observed]"
    exit 1
fi

# Extract outputs and send to BitNet for augmentation
while IFS= read -r line; do
    BITNET_OUTPUT=$(/root/.openclaw/workspace/tier-0-bitnet-enforcer.sh "Augment: $line")
    echo "{\"timestamp\":\"$(date -Iseconds)\",\"raw\":\"$line\",\"augmented\":\"$BITNET_OUTPUT\",\"source\":\"hallucination_feed\"}" >> "${OUTPUT_DIR}/bitnet-augments-${TIMESTAMP}.jsonl"
done < "$INPUT_FILE"

echo "[0] FEED COMPLETE: $INPUT_FILE → BitNet augmentation"
echo "Output: ${OUTPUT_DIR}/bitnet-augments-${TIMESTAMP}.jsonl"
