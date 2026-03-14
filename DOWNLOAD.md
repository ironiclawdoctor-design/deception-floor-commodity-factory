# Downloads

All packages ready to download from `/root/.openclaw/workspace/`:

## Factory
- **deception-floor-factory.tar.gz** (51 KB)
  - Complete factory code + tests + scripts
  - Extract: `tar -xzf deception-floor-factory.tar.gz`
  - Install: `cd deception-floor-commodity-factory && bash install.sh`

## Playbooks
- **agency-playbooks.tar.gz** (21 KB)
  - FAMINE_PLAYBOOK.md (survive zero tokens)
  - REVENUE_PLAYBOOK.md (first $500 sale)
  - SOVEREIGNTY_CHECKLIST.md (BitNet-only ops)
  - FAITH_DECISION_TREE.md (governance framework)
  - famine-watch.sh (token countdown)
  - Extract: `tar -xzf agency-playbooks.tar.gz`

## Usage

Extract both:
```bash
tar -xzf deception-floor-factory.tar.gz
tar -xzf agency-playbooks.tar.gz
```

Then run:
```bash
cd deception-floor-commodity-factory
bash install.sh
npm run dev
```

Visit `http://localhost:9000` for API
Visit `http://localhost:9000/health` to check status

## What's Inside

- 37 passing tests
- 5 executable bash scripts
- 4 playbooks (famine, revenue, sovereignty, faith)
- HTML sales page
- Complete installation script
- Git-based backups

All code. All executable. All yours to fork.
