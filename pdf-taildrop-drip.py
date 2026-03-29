import os, shutil, subprocess
from pathlib import Path
pdf_dir = Path('/root/.openclaw/workspace/pdf')
sent_dir = Path('/root/.openclaw/workspace/pdf-sent')
sent_dir.mkdir(exist_ok=True)
files = sorted(pdf_dir.glob('*.pdf'))[:5]
if not files:
    print('DONE: pdf folder drained')
else:
    for f in files:
        r = subprocess.run(['tailscale','file','cp',str(f),'allowsall-gracefrom-god.tail275cba.ts.net:'],capture_output=True,text=True)
        if r.returncode == 0:
            shutil.move(str(f), sent_dir / f.name)
            print(f'SENT+MOVED: {f.name}')
        else:
            print(f'FAIL: {f.name} — {r.stderr.strip()}')