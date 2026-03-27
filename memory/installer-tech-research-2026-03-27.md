# Installer Technology Research — 2026-03-27
# Dollar Agency Stack: OpenClaw + agents + SQLite + crons on fresh Ubuntu/Debian VPS

## Goal: Cold-start in under 10 minutes, no Docker daemon required, Node.js stack

---

## Technology Landscape

### 1. Script-based (curl | bash)
**Pattern:** `curl -fsSL https://install.openclaw.ai | bash`
- Used by: Tailscale, nvm, Homebrew, OpenClaw itself
- **Pros:** Single command, no prerequisites, network-fetches latest version
- **Cons:** Security risk (MITM), script must handle Node.js version detection, no rollback
- **Relevance:** High. OpenClaw already uses this pattern. Agency installer should extend it.
- **Install time:** 3–6 minutes (Node install + npm global + config)

### 2. npm global install
**Pattern:** `npm install -g openclaw && openclaw setup`
- **Pros:** Idiomatic for Node.js apps, handles dependency tree, `npm update` works
- **Cons:** Requires Node.js pre-installed, pollutes global npm space
- **Relevance:** Primary path. Agency install = `openclaw` installed + workspace tar extracted
- **Install time:** 2–4 minutes (assuming Node 18+ present)

### 3. tar.gz self-installer (what we have)
**Pattern:** `curl -O install.tar.gz && tar -xzf install.tar.gz && ./install.sh`
- Current: `agency-install.tar.gz` (435KB) in workspace root
- **Upgrade:** Add `install.sh` post-extract hook that: (1) checks Node version (2) runs `npm install -g openclaw` if absent (3) extracts workspace to `~/.openclaw/workspace` (4) runs `openclaw gateway start`
- **Pros:** Fully offline after download, reproducible, no npm registry dependency
- **Cons:** Manual update path, stale if workspace drifts
- **Relevance:** Best for air-gapped or disaster recovery. The 10-minute guarantee.
- **Install time:** 2–3 minutes

### 4. makeself (self-extracting shell archive)
**Pattern:** Single `.run` file, self-contained, `chmod +x agency.run && ./agency.run`
- Used by: NVIDIA drivers, many enterprise installers
- **Pros:** Single file, no curl required, embedded checksums, license display
- **Cons:** Larger file, requires makeself to build
- **Relevance:** Good for USB/physical transfer path. Build: `makeself agency-dir/ agency.run "Dollar Agency Installer" ./install.sh`
- **Install time:** 2–3 minutes

### 5. cloud-init (VPS first-boot)
**Pattern:** Embed installer in VPS cloud-init YAML at provisioning time
```yaml
#cloud-config
runcmd:
  - curl -fsSL https://install.openclaw.ai | bash
  - curl -O https://shan.app/agency-install.tar.gz
  - tar -xzf agency-install.tar.gz
  - bash install.sh
```
- **Pros:** Zero human intervention, fires on first boot, Ampere.sh supports it
- **Cons:** Requires external hosting of installer artifacts
- **Relevance:** High for `ampere.shannon` node replacement. Full cold-start with zero SSH.
- **Install time:** 5–8 minutes (unattended)

### 6. Docker Compose (if daemon available)
```yaml
services:
  openclaw:
    image: node:22-alpine
    volumes:
      - ~/.openclaw:/root/.openclaw
    command: npx openclaw gateway start
```
- **Pros:** Reproducible environment, isolates deps
- **Cons:** Docker daemon not guaranteed on Ampere.sh containers (we're already inside a container — nested Docker may not work)
- **Relevance:** Low for primary path. Good for local dev.

### 7. Ansible playbook
**Pattern:** `ansible-playbook install-agency.yml -i ampere.shannon,`
- **Pros:** Idempotent, handles Node version, config management, runs remotely
- **Cons:** Requires Ansible installed on control machine, overkill for single node
- **Relevance:** Medium. Good when managing multiple nodes. Overkill for one.

### 8. Nix flakes
- **Pros:** Fully reproducible, hash-locked deps
- **Cons:** Nix not installed by default, steep learning curve, Node.js ecosystem friction
- **Relevance:** Low. Agency stack is too dynamic for Nix pinning.

---

## Top 3 Recommended Approaches

### 🥇 1. Enhanced tar.gz + install.sh (Primary)
**What:** Upgrade `agency-install.tar.gz` with a proper `install.sh` that handles full cold-start.

```bash
#!/bin/bash
# agency install.sh
set -e
echo "Dollar Agency installer — ampere.shannon"

# 1. Node.js check
if ! command -v node &>/dev/null; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi

# 2. OpenClaw
npm install -g openclaw

# 3. Workspace
mkdir -p ~/.openclaw
cp -r workspace/ ~/.openclaw/workspace
cp openclaw.json ~/.openclaw/openclaw.json

# 4. Config patch (SR-023 + LB-007)
openclaw config patch '{"tools":{"exec":{"host":"gateway","security":"full","ask":"off"}},"channels":{"telegram":{"execApprovals":{"enabled":true,"approvers":["8273187690"],"target":"dm"}}}}'

# 5. Start
openclaw gateway start --background
echo "Agency online. Run: openclaw status"
```

**Time:** 5–8 min | **Reliability:** High | **Offline-capable:** Yes

---

### 🥈 2. cloud-init YAML (Zero-touch replacement)
**What:** Store installer YAML in workspace. On new Ampere.sh node: paste into cloud-init field at provisioning.

**Time:** 8–10 min unattended | **Reliability:** High | **Human input:** ~30 seconds at provisioning

---

### 🥉 3. curl | bash (Fastest for known-good Node.js nodes)
**What:** Host `install.sh` at `https://shan.app/install` (or GitHub raw). One command.

`curl -fsSL https://raw.githubusercontent.com/ironiclawdoctor-design/deception-floor-commodity-factory/master/install.sh | bash`

**Time:** 3–5 min | **Reliability:** Requires network + GitHub up | **Security:** Acceptable for own infra

---

## What to Build Now

1. Write `install.sh` with the Node check + OpenClaw install + config patch sequence
2. Bundle into new `agency-install.tar.gz` with the script included
3. Commit to git repo root (survives deletion via distributed mirrors)
4. Store cloud-init YAML at `workspace/cloud-init-ampere.yaml`

The 10-minute guarantee is already achievable. It just needs the script written.
