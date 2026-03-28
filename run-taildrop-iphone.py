import subprocess, os

files = [
    '/root/.openclaw/workspace/agency-install.tar.gz',
    '/root/.openclaw/workspace/agency-ssn-report.xlsx',
    '/root/.openclaw/workspace/alibi-summary-2026-03-27.md',
]

# iPhone is allowsall-gracefrom-god (confirmed from tailscale status)
# MacBook is fernandos-macbook-proall92
devices = [
    'allowsall-gracefrom-god.tail275cba.ts.net',
    'fernandos-macbook-proall92.tail275cba.ts.net',
]

for device in devices:
    for f in files:
        if not os.path.exists(f):
            print(f"SKIP {f}")
            continue
        r = subprocess.run(['tailscale', 'file', 'cp', f, f'{device}:'],
                          capture_output=True, text=True)
        result = 'SENT' if r.returncode == 0 else f'FAIL: {r.stderr.strip()}'
        print(f"{device.split('.')[0]} | {os.path.basename(f)}: {result}")
