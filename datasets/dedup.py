#!/usr/bin/env python3
"""
RLHF Dataset Deduplication Pipeline
- Hash every JSONL file (MD5)
- Keep one canonical copy per unique hash
- Move duplicates to .trash/
- Report stats
"""
import os, sys, hashlib, shutil, json
from pathlib import Path
from collections import defaultdict

SEARCH_DIRS = [
    "/root/.openclaw/workspace/bedrock-results",
    "/root/.openclaw/workspace/vigilance",
]
CLEAN_DIR = Path("/root/.openclaw/workspace/datasets/rlhf-clean")
TRASH_DIR = Path("/root/.openclaw/workspace/datasets/.trash")
STATS_FILE = Path("/root/.openclaw/workspace/datasets/dedup-stats.json")

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
TRASH_DIR.mkdir(parents=True, exist_ok=True)

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def count_rows(path):
    count = 0
    try:
        with open(path, "r", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    count += 1
    except Exception:
        pass
    return count

print("🔍 Scanning for JSONL files...")
all_files = []
for d in SEARCH_DIRS:
    p = Path(d)
    if p.exists():
        found = list(p.rglob("*.jsonl"))
        print(f"  {d}: {len(found)} files")
        all_files.extend(found)

print(f"\nTotal files found: {len(all_files)}")

print("\n🔐 Hashing all files (this may take a minute)...")
hash_to_files = defaultdict(list)
total_original_bytes = 0

for i, f in enumerate(all_files):
    if i % 100 == 0:
        print(f"  Progress: {i}/{len(all_files)}", flush=True)
    try:
        size = f.stat().st_size
        total_original_bytes += size
        h = md5(f)
        hash_to_files[h].append(f)
    except Exception as e:
        print(f"  WARN: {f}: {e}")

unique_hashes = len(hash_to_files)
duplicate_files = sum(len(v) - 1 for v in hash_to_files.values())
print(f"\n✅ Unique files: {unique_hashes}")
print(f"🗑  Duplicate files: {duplicate_files}")

print("\n📦 Copying canonical files to rlhf-clean/...")
canonical_rows = 0
canonical_bytes = 0
canonical_paths = []
trashed_paths = []

for h, files in hash_to_files.items():
    # Pick the canonical file (prefer bedrock-results, then shortest path)
    canonical = sorted(files, key=lambda p: (0 if "bedrock-results" in str(p) else 1, len(str(p))))[0]
    dupes = [f for f in files if f != canonical]
    
    # Copy canonical to clean dir
    dest_name = canonical.name
    # Handle name collisions (same name, different hash)
    dest = CLEAN_DIR / dest_name
    if dest.exists():
        dest = CLEAN_DIR / f"{h[:8]}_{canonical.name}"
    
    shutil.copy2(canonical, dest)
    rows = count_rows(dest)
    canonical_rows += rows
    canonical_bytes += dest.stat().st_size
    canonical_paths.append(str(dest))
    
    # Move duplicates to trash
    for dupe in dupes:
        trash_dest = TRASH_DIR / f"{h[:8]}_{dupe.parent.name}_{dupe.name}"
        try:
            shutil.move(str(dupe), trash_dest)
            trashed_paths.append(str(trash_dest))
        except Exception as e:
            print(f"  WARN trash: {e}")

total_original_rows = 0
print("\n🔢 Counting rows in original (pre-dedup) files...")
# Estimate: unique rows = canonical_rows, total was ~canonical_rows * avg_duplication
avg_duplication = len(all_files) / unique_hashes if unique_hashes else 1
estimated_original_rows = int(canonical_rows * avg_duplication)

saved_bytes = total_original_bytes - canonical_bytes
dedup_ratio = (1 - canonical_bytes / total_original_bytes) * 100 if total_original_bytes else 0

stats = {
    "total_files_scanned": len(all_files),
    "unique_files": unique_hashes,
    "duplicate_files": duplicate_files,
    "total_original_bytes": total_original_bytes,
    "canonical_bytes": canonical_bytes,
    "saved_bytes": saved_bytes,
    "dedup_ratio_pct": round(dedup_ratio, 2),
    "unique_rows": canonical_rows,
    "estimated_original_rows": estimated_original_rows,
    "avg_duplication_factor": round(avg_duplication, 2),
    "clean_dir": str(CLEAN_DIR),
    "trash_dir": str(TRASH_DIR),
}

with open(STATS_FILE, "w") as f:
    json.dump(stats, f, indent=2)

print("\n" + "="*50)
print("📊 DEDUP REPORT")
print("="*50)
print(f"Files scanned:        {len(all_files):,}")
print(f"Unique files:         {unique_hashes:,}")
print(f"Duplicates trashed:   {duplicate_files:,}")
print(f"Original size:        {total_original_bytes/1e6:.1f} MB")
print(f"Clean size:           {canonical_bytes/1e6:.1f} MB")
print(f"Storage saved:        {saved_bytes/1e6:.1f} MB ({dedup_ratio:.1f}%)")
print(f"Unique rows:          {canonical_rows:,}")
print(f"Est. original rows:   {estimated_original_rows:,}")
print(f"Dedup factor:         {avg_duplication:.1f}x")
print(f"\nStats saved to: {STATS_FILE}")
print(f"Clean dataset:  {CLEAN_DIR}")
print(f"Trash:          {TRASH_DIR}")
print("\n✅ DONE")
