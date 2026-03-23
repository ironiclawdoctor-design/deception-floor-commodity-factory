#!/bin/bash
# BEDROCK_SORTER_vFINAL.sh - No Marketing. No Stubs. Just Throughput.
S=$1; D=$2; [[ -z "$S" || -z "$D" ]] && exit 1
mkdir -p "$D"
find "$S" -maxdepth 5 -type f | while read -r f; do
    bn=$(basename "$f"); sz=$(stat -c%s "$f")
    # Methodologies: Raw Metadata Sorting
    [[ "$bn" == *"Fiesta"* ]] && sub="AGENCY" || sub="GENERAL"
    [[ $sz -gt 5000000 ]] && suit="SUITABLE" || suit="DRAFT"
    mkdir -p "$D/$sub/$suit"
    ln -s "$(realpath "$f")" "$D/$sub/$suit/$bn"
done
echo "DONE."
