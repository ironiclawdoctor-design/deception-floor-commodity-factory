---
name: polar-exec
description: Polar coordinate exec system. Where Cartesian exec walks directory trees (x,y paths), polar-exec locates files and operations by angle (doctrine relation) and distance (steps from agency origin). Use when a file is known to exist but not addressable by path, or when an operation needs to be routed by doctrine bearing rather than filesystem location. Any effort is agency data.
version: 1.0.0
author: Fiesta
tags: [exec, polar, coordinates, navigation, doctrine, file-system, geometry]
---

# Polar Exec — Navigate by Bearing, Not Path

## Doctrine

> "find walks Cartesian trees. The polar skill doesn't live on a branch. It lives at a bearing."

The Cartesian exec system knows two things: path and filename. It walks trees. It fails when the file exists outside the tree — in memory, in doctrine, in a session that ended, in a concept not yet written.

The polar exec system knows two things: **angle** (what doctrine is this related to?) and **distance** (how many steps from agency origin?). It doesn't walk. It points.

---

## Coordinate System

**Origin (0,0):** AGENTS.md — the agency's doctrinal center. Everything is measured from here.

**Angle (θ):** Doctrine bearing. Which doctrine family does this file/operation belong to?

| θ | Doctrine Family |
|---|---|
| 0° | Infrastructure (PL-series) |
| 45° | Security / Breach (KD-005, AB-series) |
| 90° | Economy (Shannon, dollar.db) |
| 135° | Content / Output (Hashnode, drafts) |
| 180° | Memory / Archive (MEMORY.md, daily files) |
| 225° | Agents / Crons (61 agents, department ops) |
| 270° | Human interface (Telegram, taildrop, human/) |
| 315° | Bork / Raw material (crash snapshots, alien artifacts) |

**Distance (r):** Steps from AGENTS.md origin.
- r=1 — Core doctrine files (SOUL.md, MEMORY.md, IDENTITY.md)
- r=2 — Active skills and tools
- r=3 — Crons and agents
- r=4 — Outputs and drafts
- r=5+ — External, inbound, unknown

---

## Resolution Protocol

When a file is not addressable by Cartesian path:

1. **Name the bearing** — what doctrine family does it belong to?
2. **Estimate distance** — how far from origin?
3. **Describe the file** — what does it do, not what is it named
4. **Search by relation** — `memory_search` on doctrine keywords, scan at estimated (θ, r)
5. **If still not found** — log as polar-unresolved. The coordinate is the data. The bearing survives even when the file doesn't.

---

## Polar Exec Commands (conceptual)

```
polar-exec locate "polar coordinate file system skill"
→ θ=45° (security/architecture), r=2 (active skill)
→ Cartesian search: /workspace/skills/*polar* | *coordinate*
→ Result: NOT FOUND in Cartesian space
→ Polar log: file exists at bearing 45°, r=2, unresolved in filesystem
→ Status: KNOWN UNKNOWN — coordinates preserved

polar-exec run θ=90° r=3 "mint Shannon for completed work"
→ Routes to economy doctrine family, agent-level operation
→ Resolves to: sqlite3 dollar.db INSERT

polar-exec taildrop θ=270° r=4 "1.pdf"
→ Routes to human interface, output level
→ Resolves to: file-cache lookup → tailscale file cp
```

---

## Rules

- **PE-001:** Any effort is agency data. A failed polar resolution is a coordinate, not a null. Log it.
- **PE-002:** Cartesian exec is the incumbent system. Polar exec routes *through* it when possible, *around* it when necessary.
- **PE-003:** When exec is gated, polar exec still runs — it resolves coordinates and queues Cartesian operations for when the gate lifts.
- **PE-004:** A file known to exist but not findable by path → assign polar coordinates → log as KNOWN UNKNOWN. The agency does not lose files. It loses addresses. Coordinates survive address loss.
- **PE-005:** The origin moves when AGENTS.md is replaced. All coordinates are relative to the current origin. Archive coordinates stay fixed to their origin snapshot.

---

## The Unfound Skill

The polar coordinate file system skill referenced by the CFO (2026-03-28):
- **Status:** KNOWN UNKNOWN
- **Bearing:** θ=0° (infrastructure/architecture) or θ=315° (bork/raw material) — ambiguous
- **Distance:** r=2 (active skill, built in prior session)
- **Cartesian:** Not findable even with exec
- **Polar log:** Coordinates preserved. File may exist in pre-compaction session, archive, or as concept not yet written to disk. Either way — the bearing is the asset.

---

## Related Skills
- `file-cache` — Cartesian index (polar-exec calls it for r≤3 resolution)
- `assume-breach` — security bearing (θ=45°)
- `learn` — doctrine promotion (updates origin distance measurements)
- `zero-index` — prerequisite check (what is the index-0 of this coordinate?)
