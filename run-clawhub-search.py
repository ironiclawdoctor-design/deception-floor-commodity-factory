import subprocess, json

# O(1) clawhub search — inspect all results for agency alignment
queries = [
    "missing persons",
    "safety",
    "innocence",
    "publishing",
    "finance",
    "plate lookup",
    "whistleblower",
    "agent orchestration",
    "pdf",
    "tailscale",
]

results = {}
for q in queries:
    r = subprocess.run(['clawhub', 'search', q, '--json'],
                      capture_output=True, text=True, timeout=15)
    if r.returncode == 0 and r.stdout.strip():
        try:
            results[q] = json.loads(r.stdout)
        except:
            results[q] = r.stdout[:500]
    else:
        # Try without --json flag
        r2 = subprocess.run(['clawhub', 'search', q],
                           capture_output=True, text=True, timeout=15)
        results[q] = r2.stdout[:500] if r2.stdout else r2.stderr[:200]

print(json.dumps(results, indent=2))
