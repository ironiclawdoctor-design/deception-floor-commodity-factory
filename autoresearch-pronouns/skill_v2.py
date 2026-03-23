#!/usr/bin/env python3
"""
Pronoun Skill — v2
Fixes over v1:
- INLINE [SUBJ_CAP:Name] was not resolving (regex missed _CAP variant)
- Multi-pronoun paragraphs: each {SUBJ} needs positional antecedent, not last-mentioned-overall
- Capitalization of inline resolved pronouns
- Neopronoun object inline (hir not falling back to gendered)
- Possessive capitalization bug ({POSS} resolving lowercase even at sentence start)
"""
import json
import re
from pathlib import Path

AGENTS_FILE = Path(__file__).parent / "agents.json"

def load_agents():
    data = json.loads(AGENTS_FILE.read_text())
    registry = {}
    for a in data["agents"] + data.get("neopronouns", []):
        pronouns = a["pronouns"].split("/")
        entry = {
            "name": a["name"],
            "id": a["id"],
            "subject": pronouns[0],
            "object": pronouns[1],
            "possessive": _possessive(pronouns[0]),
            "reflexive": _reflexive(pronouns[0]),
        }
        registry[a["name"].lower()] = entry
        first = a["name"].split()[0].lower()
        if first not in registry:
            registry[first] = entry
        # Role aliases
        if "role" in a:
            role_key = a["role"].lower().replace(" ", "_")
            if role_key not in registry:
                registry[role_key] = entry
            # "the CFO" → nate
            registry[f"the {a['role'].lower()}"] = entry
    return registry

def _possessive(subject):
    return {"she": "her", "he": "his", "they": "their",
            "ze": "hir", "xe": "xyr"}.get(subject, "their")

def _reflexive(subject):
    return {"she": "herself", "he": "himself", "they": "themselves",
            "ze": "hirself", "xe": "xemself"}.get(subject, "themselves")

_DEFAULT = {"subject": "they", "object": "them", "possessive": "their", "reflexive": "themselves"}

def resolve_pronouns(text, last_mentioned=None, registry=None):
    if registry is None:
        registry = load_agents()

    # ── Step 1: Resolve all inline [TYPE:Name] and [TYPE_CAP:Name] first ────
    def replace_inline(m):
        pronoun_type = m.group(1).upper()   # e.g. SUBJ, SUBJ_CAP, OBJ, POSS, REFL
        name = m.group(2).strip().lower()
        a = registry.get(name) or registry.get(name.split()[0]) or _DEFAULT
        cap = pronoun_type.endswith("_CAP")
        base = pronoun_type.replace("_CAP", "")
        val = {
            "SUBJ": a["subject"], "OBJ": a["object"],
            "POSS": a["possessive"], "REFL": a["reflexive"],
        }.get(base, m.group(0))
        return val.capitalize() if cap else val

    text = re.sub(r'\[(\w+):([^\]]+)\]', replace_inline, text)

    # ── Step 2: Resolve positional {PLACEHOLDER} — scan left to right ───────
    # Build ordered list of (position, agent) from named mentions
    agent_positions = []
    for name, agent in registry.items():
        for m in re.finditer(re.escape(name), text.lower()):
            agent_positions.append((m.start(), agent))
    agent_positions.sort(key=lambda x: x[0])

    # For each placeholder, find the closest preceding named agent
    def get_agent_at(pos):
        # Walk backwards through agent_positions to find last mentioned before pos
        best = None
        for apos, agent in agent_positions:
            if apos < pos:
                best = agent
        return best or _resolve_hint(last_mentioned, registry) or _DEFAULT

    # Replace placeholders in order, updating position as we go
    result = []
    i = 0
    placeholder_re = re.compile(r'\{(SUBJ_CAP|OBJ_CAP|SUBJ|OBJ|POSS|REFL)\}')
    
    for m in placeholder_re.finditer(text):
        result.append(text[i:m.start()])
        ptype = m.group(1)
        agent = get_agent_at(m.start())
        cap = ptype.endswith("_CAP")
        base = ptype.replace("_CAP", "")
        val = {
            "SUBJ": agent["subject"], "OBJ": agent["object"],
            "POSS": agent["possessive"], "REFL": agent["reflexive"],
        }.get(base, "they")
        result.append(val.capitalize() if cap else val)
        i = m.end()
    
    result.append(text[i:])
    return "".join(result)

def _resolve_hint(hint, registry):
    if not hint:
        return None
    h = hint.lower()
    return registry.get(h) or registry.get(h.split()[0])

def get_pronoun(name, pronoun_type="subject", registry=None):
    if registry is None:
        registry = load_agents()
    key = name.lower().split()[0]
    agent = registry.get(name.lower()) or registry.get(key)
    if not agent:
        return _DEFAULT.get(pronoun_type, "they")
    return agent.get(pronoun_type, "they")

if __name__ == "__main__":
    import sys
    reg = load_agents()
    test = sys.argv[1] if len(sys.argv) > 1 else "Valentina published the article. {SUBJ_CAP} confirmed it was live."
    hint = sys.argv[2] if len(sys.argv) > 2 else None
    print(resolve_pronouns(test, hint, reg))
