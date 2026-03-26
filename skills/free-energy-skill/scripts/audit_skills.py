#!/usr/bin/env python3
"""
audit_skills.py — Free Energy Skill Auditor

Scans all skills in workspace, scores quality 0-100.
Outputs ranked list lowest-first (most improvable first).
Saves results to audit-cache.json.

Usage:
    python3 audit_skills.py
    python3 audit_skills.py --output /path/to/cache.json
    python3 audit_skills.py --verbose
    python3 audit_skills.py --json   # raw JSON only
"""

import os
import json
import re
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone

# Skill directories to scan
SKILL_DIRS = [
    "/root/.openclaw/workspace/skills/",
    os.path.expanduser("~/.openclaw/workspace/skills/"),
]

# Deduplicate (they may be the same path)
SKILL_DIRS = list(dict.fromkeys(str(Path(d).resolve()) for d in SKILL_DIRS if Path(d).exists()))

DEFAULT_CACHE = Path("/root/.openclaw/workspace/skills/free-energy-skill/audit-cache.json")


def score_description_clarity(content: str, frontmatter: dict) -> tuple[int, list[str]]:
    """
    0-20: Does the description fire exactly when needed?
    - Has 'Use when:' with specific triggers → +8
    - Has 'NOT for:' / 'Triggers on:' phrases → +6
    - Has exact command phrases quoted → +3
    - Has 'never' / boundary conditions → +3
    """
    score = 0
    notes = []

    desc = frontmatter.get("description", "") + content

    if re.search(r"Use when:", desc, re.IGNORECASE):
        score += 8
    else:
        notes.append("Missing 'Use when:' triggers")

    if re.search(r"NOT for:|Triggers on:|never use|do not use", desc, re.IGNORECASE):
        score += 6
    else:
        notes.append("Missing 'NOT for:' boundary conditions")

    # Quoted command phrases (e.g. "improve skill", "audit all")
    quoted = re.findall(r'"[^"]{3,40}"', desc)
    if len(quoted) >= 2:
        score += 3
    else:
        notes.append("Fewer than 2 quoted trigger phrases")

    if re.search(r'\bnever\b|\bboundary\b|\bexclude\b|\bnot\b.*\bfor\b', desc, re.IGNORECASE):
        score += 3
    else:
        notes.append("No explicit boundary/never conditions")

    return min(score, 20), notes


def score_workflow_specificity(content: str) -> tuple[int, list[str]]:
    """
    0-20: Are the steps numbered and concrete?
    - Has numbered steps (1. 2. 3.) → +8
    - Has code blocks with actual commands → +7
    - Has a 'Workflow' section → +5
    """
    score = 0
    notes = []

    # Numbered steps
    numbered = re.findall(r'^\s*\d+\.\s+\S', content, re.MULTILINE)
    if len(numbered) >= 3:
        score += 8
    elif len(numbered) >= 1:
        score += 4
        notes.append("Few numbered steps (< 3)")
    else:
        notes.append("No numbered workflow steps")

    # Code blocks with commands
    code_blocks = re.findall(r'```[\w]*\n(.*?)```', content, re.DOTALL)
    has_commands = any(
        re.search(r'python3|bash|sh|curl|grep|exec|run|npm|pip', block, re.IGNORECASE)
        for block in code_blocks
    )
    if has_commands:
        score += 7
    else:
        notes.append("No executable commands in code blocks")

    if re.search(r'## Workflow|## Steps|## Usage|## How to Use', content, re.IGNORECASE):
        score += 5
    else:
        notes.append("No dedicated Workflow/Steps section")

    return min(score, 20), notes


def score_bundled_resources(skill_path: Path) -> tuple[int, list[str]]:
    """
    0-20: What's in scripts/ and references/?
    - Has scripts/ dir with ≥1 .py/.sh file → +10
    - Has references/ dir with ≥1 .md file → +7
    - Has assets/ or other bundled files → +3
    """
    score = 0
    notes = []

    scripts_dir = skill_path / "scripts"
    refs_dir = skill_path / "references"
    assets_dir = skill_path / "assets"

    if scripts_dir.exists():
        scripts = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))
        if scripts:
            score += 10
        else:
            notes.append("scripts/ dir exists but no .py/.sh files")
    else:
        notes.append("No scripts/ directory")

    if refs_dir.exists():
        refs = list(refs_dir.glob("*.md")) + list(refs_dir.glob("*.json")) + list(refs_dir.glob("*.txt"))
        if refs:
            score += 7
        else:
            notes.append("references/ dir exists but empty")
    else:
        notes.append("No references/ directory")

    if assets_dir.exists() and any(assets_dir.iterdir()):
        score += 3

    return min(score, 20), notes


def score_progressive_disclosure(content: str) -> tuple[int, list[str]]:
    """
    0-20: Quick-start → full spec → edge cases?
    - Has quick-start or TL;DR section → +6
    - Has at least 3 ## sections → +6
    - Has Edge Cases / Troubleshooting section → +5
    - Has a table or comparison structure → +3
    """
    score = 0
    notes = []

    if re.search(r'## (Quick.?Start|TL;?DR|One.?Liner|Fast|Quickstart)', content, re.IGNORECASE):
        score += 6
    else:
        notes.append("No quick-start / TL;DR section")

    sections = re.findall(r'^## .+', content, re.MULTILINE)
    if len(sections) >= 4:
        score += 6
    elif len(sections) >= 2:
        score += 3
        notes.append("Fewer than 4 top-level sections")
    else:
        notes.append("Very few sections — wall of text risk")

    if re.search(r'## (Edge Cases|Troubleshoot|Errors|Gotchas|Caveats|Limitations)', content, re.IGNORECASE):
        score += 5
    else:
        notes.append("No Edge Cases / Troubleshooting section")

    # Table structure
    if re.search(r'\|.+\|.+\|', content):
        score += 3

    return min(score, 20), notes


def score_token_efficiency(content: str) -> tuple[int, list[str]]:
    """
    0-20: Is the SKILL.md under 500 lines without losing function?
    - < 200 lines → +20
    - 200-350 lines → +15
    - 350-500 lines → +10
    - 500-700 lines → +5
    - > 700 lines → +0
    Penalty: -5 if no frontmatter (forces agent to read everything to understand scope)
    """
    score = 0
    notes = []

    lines = content.count('\n')

    if lines < 200:
        score += 20
    elif lines < 350:
        score += 15
    elif lines < 500:
        score += 10
    elif lines < 700:
        score += 5
        notes.append(f"Long SKILL.md ({lines} lines) — consider splitting to references/")
    else:
        notes.append(f"Very long SKILL.md ({lines} lines) — major token cost")

    # Check for frontmatter (yaml block at top)
    if not re.search(r'^```yaml|^---\nname:', content, re.MULTILINE):
        score = max(0, score - 5)
        notes.append("No YAML frontmatter — agent must read full file to find description")

    return min(score, 20), notes


def extract_frontmatter(content: str) -> dict:
    """Extract name/description from YAML frontmatter block."""
    result = {}

    # ```yaml ... ``` block
    m = re.search(r'```yaml\n(.*?)```', content, re.DOTALL)
    if m:
        yaml_text = m.group(1)
        for line in yaml_text.splitlines():
            if ':' in line:
                key, _, val = line.partition(':')
                result[key.strip()] = val.strip()
        return result

    # --- name: ... --- block
    m = re.search(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                key, _, val = line.partition(':')
                result[key.strip()] = val.strip()
        return result

    # Fallback: look for # Title at top
    m = re.match(r'^#\s+(.+)', content.strip())
    if m:
        result['name'] = m.group(1).strip()

    return result


def audit_skill(skill_path: Path) -> dict:
    """Audit a single skill directory. Returns score dict."""
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return {
            "name": skill_path.name,
            "path": str(skill_path),
            "total": 0,
            "scores": {
                "description_clarity": 0,
                "workflow_specificity": 0,
                "bundled_resources": 0,
                "progressive_disclosure": 0,
                "token_efficiency": 0,
            },
            "notes": ["SKILL.md missing — scored 0"],
            "status": "missing",
        }

    try:
        content = skill_md.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {
            "name": skill_path.name,
            "path": str(skill_path),
            "total": 0,
            "scores": {},
            "notes": [f"Could not read SKILL.md: {e}"],
            "status": "error",
        }

    frontmatter = extract_frontmatter(content)

    s1, n1 = score_description_clarity(content, frontmatter)
    s2, n2 = score_workflow_specificity(content)
    s3, n3 = score_bundled_resources(skill_path)
    s4, n4 = score_progressive_disclosure(content)
    s5, n5 = score_token_efficiency(content)

    total = s1 + s2 + s3 + s4 + s5
    all_notes = n1 + n2 + n3 + n4 + n5

    # Free energy threshold check
    has_resources = (skill_path / "scripts").exists() or (skill_path / "references").exists()
    above_threshold = total > 60 and has_resources

    return {
        "name": frontmatter.get("name", skill_path.name),
        "path": str(skill_path),
        "total": total,
        "above_threshold": above_threshold,
        "scores": {
            "description_clarity": s1,
            "workflow_specificity": s2,
            "bundled_resources": s3,
            "progressive_disclosure": s4,
            "token_efficiency": s5,
        },
        "notes": all_notes,
        "status": "ok",
    }


def scan_all_skills(verbose: bool = False) -> list[dict]:
    """Scan all skill directories. Return sorted list (lowest score first)."""
    results = []
    seen = set()

    for base_dir in SKILL_DIRS:
        base = Path(base_dir)
        if not base.exists():
            if verbose:
                print(f"[skip] {base} does not exist", file=sys.stderr)
            continue

        for entry in sorted(base.iterdir()):
            if not entry.is_dir():
                continue
            key = str(entry.resolve())
            if key in seen:
                continue
            seen.add(key)

            if verbose:
                print(f"[audit] {entry.name}...", file=sys.stderr)

            result = audit_skill(entry)
            results.append(result)

    # Sort: lowest score first (most improvable first)
    results.sort(key=lambda r: r["total"])
    return results


def render_table(results: list[dict]) -> str:
    """Render results as an ASCII table."""
    lines = []
    lines.append(f"\n{'='*72}")
    lines.append(f"{'SKILL AUDIT RESULTS':^72}")
    lines.append(f"{'Lowest score = most improvable':^72}")
    lines.append(f"{'='*72}")
    lines.append(f"{'Rank':<5} {'Skill':<30} {'Score':>6} {'Threshold':>10} {'Notes'}")
    lines.append(f"{'-'*5} {'-'*30} {'-'*6} {'-'*10} {'-'*20}")

    for i, r in enumerate(results, 1):
        threshold_str = "✓ above" if r.get("above_threshold") else "✗ below"
        top_note = r["notes"][0] if r["notes"] else ""
        lines.append(
            f"{i:<5} {r['name'][:30]:<30} {r['total']:>5}/100 {threshold_str:>10}  {top_note}"
        )

    lines.append(f"{'='*72}")
    lines.append(f"Total skills audited: {len(results)}")
    above = sum(1 for r in results if r.get("above_threshold"))
    lines.append(f"Above free energy threshold (>60 + has resources): {above}/{len(results)}")
    lines.append(f"{'='*72}\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit all agency skills for quality.")
    parser.add_argument("--output", default=str(DEFAULT_CACHE), help="Path to save audit-cache.json")
    parser.add_argument("--verbose", action="store_true", help="Show per-skill progress")
    parser.add_argument("--json", action="store_true", help="Output raw JSON only")
    parser.add_argument("--top", type=int, default=5, help="Show N lowest-scoring skills (default: 5)")
    args = parser.parse_args()

    results = scan_all_skills(verbose=args.verbose)

    cache = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skill_dirs_scanned": SKILL_DIRS,
        "total_skills": len(results),
        "skills": results,
    }

    # Save cache
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(cache, indent=2))

    if args.json:
        print(json.dumps(cache, indent=2))
        return

    # Print table
    print(render_table(results))

    # Print bottom N detail
    print(f"\n{'='*72}")
    print(f"BOTTOM {args.top} SKILLS — HIGHEST IMPROVEMENT ROI")
    print(f"{'='*72}")
    for r in results[:args.top]:
        print(f"\n  Skill:  {r['name']}")
        print(f"  Path:   {r['path']}")
        print(f"  Score:  {r['total']}/100")
        print(f"  Breakdown:")
        for dim, val in r.get("scores", {}).items():
            bar = "█" * val + "░" * (20 - val)
            print(f"    {dim:<25} {val:>2}/20  [{bar}]")
        if r["notes"]:
            print(f"  Issues:")
            for note in r["notes"][:4]:
                print(f"    • {note}")
        print(f"  Fix:    python3 improve_skill.py --path {r['path']}")

    print(f"\nAudit saved to: {output_path}")


if __name__ == "__main__":
    main()
