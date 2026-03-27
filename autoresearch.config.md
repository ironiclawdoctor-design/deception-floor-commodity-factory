# Autoresearch Configuration

## Goal
Exceed 93% reality correlation on NP-hard problem decomposition. Solve problems humans and standard agents punt on. Find the approach that works, iterate until it holds.

## Metric
- **Name**: solution_quality
- **Direction**: higher is better
- **Target**: >93% — measured as: does the output solve the stated problem completely, with no hand-waving, no deferral, no theater?
- **Extract command**: manual review + structured self-eval: [SOLVED / PARTIAL / THEATER]

## Target Files
- `autoresearch-experiments/` (create per-experiment files here)
- `autoresearch.config.md` (this file)

## Read-Only Files
- `SOUL.md`
- `MEMORY.md`
- `AGENTS.md`

## Run Command
Spawn isolated sub-agent with the problem. Measure output. Log result.

## Time Budget
- **Per experiment**: 120s
- **Kill timeout**: 400s

## Constraints
- No GPU
- No paid models for inner loop — glm-4.5-air:free only
- No theater (announcing plan ≠ executing plan)
- No asking for permission mid-experiment

## Branch
autoresearch/np-hard-exceed-93

## Problem Classes (ordered by impact)
1. Scheduling under constraint (agency cron optimization)
2. Graph coloring (agent dependency resolution)
3. Bin packing (token budget allocation across agents)
4. Traveling salesman variants (multi-step field ops with escape routes)
5. Boolean satisfiability (config conflict resolution)

## Notes
The maze IS the problem. Every cleanup loop is an NP-hard scheduling problem in disguise. Autoresearch finds which decomposition clears it fastest. 93% is the floor, not the ceiling.