#!/usr/bin/env python3
# safety-lock.py - Ensures the app only works if it recognizes its own origin
import os
import sys
import hashlib

ORIGIN_SIGNATURE = "fiesta-sorter-build-20260320" # Simulated signature of this conversation

def verify_safety_lock(screenshot_path):
    print(f"🛡️ Safety-Lock: Checking for build-origin in {screenshot_path}...")
    
    # In a real environment, this would use OCR/Vision to find the word 'Fiesta' or 'Shannon'
    # Simulation: check if file name contains the signature
    if ORIGIN_SIGNATURE in screenshot_path:
        print("✅ ORIGIN VERIFIED: This image is a recognized build-context screenshot.")
        return True
    else:
        print("❌ SAFETY LOCK ENGAGED: Target image does not contain build-origin. Operation HALTED.")
        return False

if __name__ == "__main__":
    test_file = sys.argv[1] if len(sys.argv) > 1 else "none"
    if verify_safety_lock(test_file):
        print("🚀 Proceeding to Non-Destructive Subject Sort.")
    else:
        sys.exit(1)
