import subprocess, os, sys

files = [
    '/root/.openclaw/workspace/agency-install.tar.gz',
    '/root/.openclaw/workspace/agency-ssn-report.xlsx',
    '/root/.openclaw/workspace/alibi-summary-2026-03-27.md',
]

# Get tailnet peers
status = subprocess.run(['tailscale', 'status'], capture_output=True, text=True)
print("TAILSCALE STATUS:")
print(status.stdout[:2000])

device = 'allowsall-gracefrom-god.tail275cba.ts.net'

for f in files:
    if not os.path.exists(f):
        # Try generating ssn report if missing
        if 'ssn-report' in f:
            r = subprocess.run(['python3', '/root/.openclaw/workspace/ssn-excel-export.py'],
                             capture_output=True, text=True)
            print(r.stdout, r.stderr)
        else:
            print(f"SKIP (not found): {f}")
            continue
    r = subprocess.run(['tailscale', 'file', 'cp', f, f'{device}:'],
                      capture_output=True, text=True)
    status_str = 'SENT' if r.returncode == 0 else f'FAIL: {r.stderr}'
    print(f"{os.path.basename(f)}: {status_str}")
