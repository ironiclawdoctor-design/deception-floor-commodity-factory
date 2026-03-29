#!/usr/bin/env python3
"""Deploy Negative Space Audit to Cloud Run — same GCP project as dollar dashboard."""
import subprocess, sys, os

PROJECT = "sovereign-see"
REGION = "us-central1"
SERVICE = "negative-space-audit"
IMAGE = f"gcr.io/{PROJECT}/{SERVICE}"

os.chdir(os.path.dirname(os.path.abspath(__file__)))

steps = [
    (["gcloud", "builds", "submit", "--tag", IMAGE, "--project", PROJECT], "Building image"),
    (["gcloud", "run", "deploy", SERVICE,
      "--image", IMAGE,
      "--platform", "managed",
      "--region", REGION,
      "--allow-unauthenticated",
      "--project", PROJECT,
      "--memory", "256Mi",
      "--cpu", "1",
      "--min-instances", "0",
      "--max-instances", "3",
      "--port", "8080"], "Deploying to Cloud Run"),
    (["gcloud", "run", "services", "describe", SERVICE,
      "--region", REGION, "--project", PROJECT,
      "--format", "value(status.url)"], "Getting URL"),
]

for cmd, label in steps:
    print(f"\n[{label}]")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        sys.exit(1)
    if result.stdout.strip():
        print(result.stdout.strip())

print("\n✓ Negative Space Audit deployed.")
