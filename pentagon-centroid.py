#!/usr/bin/env python3
import base64

strings = [
    "JAFV2NngVbF-y_CFDzZC:1:ci",
    "f95GkAm3WMh9FbmOWLsmzatyYKUrvr6id5I54DtoXdvESQu4Or",
    "4O88_9kYjKm4sSmxFfQaaKoB_JcfEk1qBHaZWTNI3JdXn:1774740054633:1:0:at:1",
    "6P3X3jE5zRlzZfdOpAFflvm5iDhVQqG7DAijlUULaaVhd:1774740054633:1:0:rt:1",
    "z_ekmPcCZkpoKv7ij3-I:1:ci"
]

print("Pentagon strings (5 points):")
for i, s in enumerate(strings):
    print(f"{i+1}. {s[:30]}...")

print("\n--- Centroid computation ---")

# Method 1: Average length
avg_len = sum(len(s) for s in strings) / len(strings)
print(f"Average length: {avg_len:.1f} chars")

# Method 2: Character-wise average (simple)
# Take first N chars where N = min length
min_len = min(len(s) for s in strings)
centroid_chars = []
for i in range(min_len):
    char_codes = [ord(s[i]) for s in strings]
    avg_code = sum(char_codes) / len(char_codes)
    centroid_chars.append(chr(int(avg_code)))

centroid = ''.join(centroid_chars)
print(f"Centroid (first {min_len} chars avg): {centroid}")

# Method 3: Base64 decode if possible
print("\nBase64 decoded (if valid):")
for s in strings:
    try:
        # Add padding
        padded = s + '=' * (-len(s) % 4)
        decoded = base64.b64decode(padded).decode('utf-8', errors='ignore')
        print(f"{s[:20]}... → {decoded[:50]}...")
    except:
        pass

# Method 4: Find common suffix
suffixes = [s.split(':')[-1] for s in strings if ':' in s]
print(f"\nCommon suffix pattern: {set(suffixes)}")

# Method 5: Numeric parts
import re
numbers = []
for s in strings:
    nums = re.findall(r'\d+', s)
    numbers.extend(nums)
print(f"Numeric parts found: {numbers[:10]}...")

# The actual centroid might be the Request Token Secret
request_token_secret = "9nBWzkfoaVQ44ZHoAxg2GqHMl7E0Xiw7"
print(f"\nRequest Token Secret (from new auth): {request_token_secret}")
print("This might be the 'centroid' as it's derived from the auth flow.")