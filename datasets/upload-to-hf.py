#!/usr/bin/env python3
"""
HuggingFace Upload Script — Dollar Agency RLHF Dataset
Uploads deduplicated clean JSONL files to:
  huggingface.co/datasets/ApproveAlwaysAllow/dollar-agency-rlhf

DO NOT RUN until human approves upload.
Run with: python3 upload-to-hf.py [--dry-run]
"""
import sys, json, os
from pathlib import Path

DRY_RUN = "--dry-run" in sys.argv
CLEAN_DIR = Path("/root/.openclaw/workspace/datasets/rlhf-clean")
HF_SECRETS = Path("/root/.openclaw/workspace/secrets/huggingface.json")
HF_REPO_ID = "ApproveAlwaysAllow/dollar-agency-rlhf"
HF_REPO_TYPE = "dataset"

# Load token
with open(HF_SECRETS) as f:
    secrets = json.load(f)
HF_TOKEN = secrets["token"]
print(f"✅ HF token loaded (user: {secrets.get('username', 'unknown')})")

if DRY_RUN:
    print("\n🔍 DRY RUN MODE — no files will be uploaded")

# Verify huggingface_hub is installed
try:
    from huggingface_hub import HfApi, CommitOperationAdd
    print("✅ huggingface_hub available")
except ImportError:
    print("❌ huggingface_hub not installed. Run:")
    print("   pip install huggingface_hub")
    sys.exit(1)

api = HfApi(token=HF_TOKEN)

# Verify repo exists
try:
    info = api.repo_info(repo_id=HF_REPO_ID, repo_type=HF_REPO_TYPE)
    print(f"✅ Repo exists: {HF_REPO_ID}")
    print(f"   Private: {info.private}")
    print(f"   Last modified: {info.lastModified}")
except Exception as e:
    print(f"⚠️  Could not access repo: {e}")
    print("   Creating repo...")
    if not DRY_RUN:
        api.create_repo(repo_id=HF_REPO_ID, repo_type=HF_REPO_TYPE, private=False)
        print(f"   ✅ Created {HF_REPO_ID}")

# Collect files to upload
files = sorted(CLEAN_DIR.glob("*.jsonl")) + [CLEAN_DIR / "README.md"]
files = [f for f in files if f.exists()]
total_bytes = sum(f.stat().st_size for f in files)

print(f"\n📦 Files to upload: {len(files)}")
print(f"   Total size: {total_bytes / 1e6:.1f} MB")
print(f"   Destination: {HF_REPO_ID}")

if DRY_RUN:
    print("\n[DRY RUN] Would upload:")
    for f in files[:10]:
        print(f"  {f.name} ({f.stat().st_size/1e3:.1f} KB)")
    if len(files) > 10:
        print(f"  ... and {len(files)-10} more")
    print("\n[DRY RUN] Complete. Run without --dry-run to actually upload.")
    sys.exit(0)

# Upload in batches to avoid API limits
BATCH_SIZE = 50
print(f"\n🚀 Starting upload in batches of {BATCH_SIZE}...")

for i in range(0, len(files), BATCH_SIZE):
    batch = files[i:i+BATCH_SIZE]
    batch_num = i // BATCH_SIZE + 1
    total_batches = (len(files) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"\n  Batch {batch_num}/{total_batches}: uploading {len(batch)} files...")
    
    operations = []
    for f in batch:
        with open(f, "rb") as fh:
            content = fh.read()
        operations.append(
            CommitOperationAdd(
                path_in_repo=f.name,
                path_or_fileobj=content,
            )
        )
    
    try:
        commit = api.create_commit(
            repo_id=HF_REPO_ID,
            repo_type=HF_REPO_TYPE,
            operations=operations,
            commit_message=f"Upload batch {batch_num}/{total_batches}: {len(batch)} deduplicated RLHF files",
        )
        print(f"  ✅ Batch {batch_num} committed: {commit.commit_url}")
    except Exception as e:
        print(f"  ❌ Batch {batch_num} failed: {e}")
        print("  Retrying individually...")
        for f in batch:
            try:
                api.upload_file(
                    path_or_fileobj=str(f),
                    path_in_repo=f.name,
                    repo_id=HF_REPO_ID,
                    repo_type=HF_REPO_TYPE,
                )
                print(f"    ✅ {f.name}")
            except Exception as e2:
                print(f"    ❌ {f.name}: {e2}")

print(f"\n🎉 Upload complete!")
print(f"   View at: https://huggingface.co/datasets/{HF_REPO_ID}")
