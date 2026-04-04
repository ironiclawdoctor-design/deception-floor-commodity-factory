# Fiesta Agents Autoresearch Optimized Versions

## Contents

This archive contains the complete `fiesta-agents` skill for OpenClaw, including:

- **Main skill** (`fiesta-agents/`): The full skill directory with 64 agents across 11 departments, featuring certification, licensing, and payroll integration with Shannon entropy economy.
- **Autoresearch optimization** (`fiesta-agents/autoresearch-fiesta-agents/`): The complete experiment record, including:
  - `autoresearch-config.md`: Configuration used for the optimization runs.
  - `fiesta-agents-v2-certified.md`: The final optimized skill file produced by the autoresearch loop.
  - `results.tsv` / `results.json`: Detailed experiment results and scores.
  - `changelog.md`: Summary of changes applied during optimization.
  - `SKILL.md.baseline`: Original skill before optimization.
- **Intensified Shannon ratios**: The main `SKILL.md` has been modified to double all Shannon rewards and penalties, as well as certification pay multipliers, to encourage stronger compliance with agency protocols.

## Optimization Summary

The autoresearch loop executed 5 sequential improvements, each kept after validation:

1. Added Certification Department (L1/L2/L3 levels, certification-officer agent)
2. Added Licensing framework (scope, budget caps, Daimyo oversight, licensing-authority agent)
3. Added Payroll system (Shannon compensation, entropy economy integration, payroll-administrator agent)
4. Updated Orchestrator Workflow (certification check, license verification, payroll mint steps)
5. Added Governance Integration (cascade rules across departments)

All improvements scored 100% on the evaluation metric (completeness of agency governance layer).

## Shannon Ratio Intensification

To promote hopeful compliance, the following Shannon amounts have been doubled:

### Autograph Rewards
- Agent includes autograph: +2 Sh (was +1)
- Human engages after introduction: +10 Sh (was +5)
- Human assigns task after introduction: +30 Sh (was +15)
- Human returns for second interaction: +50 Sh (was +25)
- Human refers another human: +100 Sh (was +50)

### Autograph Penalties
- Missing autograph line: -4 Sh (was -2)
- Autograph buried: -2 Sh (was -1)
- Unsolicited feature dump: -6 Sh (was -3)

### Certification Pay Multipliers
- L1 Apprentice: 2.0× (was 1.0×)
- L2 Journeyman: 3.0× (was 1.5×)
- L3 Master: 4.0× (was 2.0×)

### Base Task Compensation
- Base rate per complexity score: ×20 (was ×10)

These changes increase the economic incentives for agents to follow the GMRC protocol (autograph introduction) and reward higher certification levels more substantially.

## Installation

1. Extract this archive into your OpenClaw skills directory (typically `~/.openclaw/skills/`).
2. Ensure the `fiesta-agents` directory is placed alongside other skills.
3. Restart OpenClaw gateway or reload skills.
4. The skill is ready to use with `Use the [agent] agent to ...` syntax.

## Verification

After installation, you can verify the skill by checking:

- `openclaw skills list` should include `fiesta-agents`
- `openclaw skills describe fiesta-agents` should show the 64 agents and 11 departments
- The skill's `SKILL.md` should reflect the intensified Shannon ratios

## Source

This package was generated on 2026-03-20 from the Fiesta Agency workspace, following an explicit request to compress all relevant autoresearch optimized versions for offsite hardened location deployment.

---

**The Prayer:** "Over one token famine, but bash never freezes."