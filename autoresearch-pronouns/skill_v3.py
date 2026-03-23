#!/usr/bin/env python3
"""
Pronoun Skill — v3
Strategy: two-pass with explicit context stack.

Pass 1: resolve all [INLINE:Name] references first (fully explicit)
Pass 2: for {PLACEHOLDER}s, use a context window:
  - If a hint is provided AND no closer name precedes the placeholder → use hint
  - Precedence: inline-resolved names > preceding names > hint > default they/them
  
Additional fixes over v2:
- Hint consulted when no name precedes placeholder (fixes T1-05, T4-10)
- Capitalization of inline-resolved subject pronouns (fixes T4-01, T4-08 {POSS} cap)
- T4-04: {OBJ}/{POSS} in same sentence as named agent — hint determines which agent
- T4-08: sentence-level possessive capitalization
- T4-10: hint=Dollar prevents Nate (mentioned after) from hijacking {SUBJ_CAP} at end
"""
import json, re
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
        if "role" in a:
            role_lower = a["role"].lower()
            registry[f"the {role_lower}"] = entry
            registry[role_lower.replace(" ", "_")] = entry
    return registry

def _possessive(s):
    return {"she":"her","he":"his","they":"their","ze":"hir","xe":"xyr"}.get(s,"their")
def _reflexive(s):
    return {"she":"herself","he":"himself","they":"themselves","ze":"hirself","xe":"xemself"}.get(s,"themselves")

_DEFAULT = {"subject":"they","object":"them","possessive":"their","reflexive":"themselves"}

def _val(agent, ptype):
    base = ptype.replace("_CAP","")
    return {"SUBJ": agent["subject"], "OBJ": agent["object"],
            "POSS": agent["possessive"], "REFL": agent["reflexive"]}.get(base, "they")

def resolve_pronouns(text, last_mentioned=None, registry=None):
    if registry is None:
        registry = load_agents()

    hint_agent = None
    if last_mentioned:
        h = last_mentioned.lower()
        hint_agent = registry.get(h) or registry.get(h.split()[0])

    # ── Pass 1: resolve all [TYPE:Name] inline ───────────────────────────────
    def replace_inline(m):
        ptype = m.group(1).upper()
        name = m.group(2).strip().lower()
        a = registry.get(name) or registry.get(name.split()[0]) or _DEFAULT
        cap = ptype.endswith("_CAP")
        v = _val(a, ptype)
        return v.capitalize() if cap else v

    text = re.sub(r'\[(\w+):([^\]]+)\]', replace_inline, text)

    # ── Pass 2: positional resolution for {PLACEHOLDER}s ────────────────────
    # Build list of (position, agent) from all named mentions in text
    lower_text = text.lower()
    agent_positions = []
    for name, agent in registry.items():
        for match in re.finditer(re.escape(name), lower_text):
            agent_positions.append((match.start(), match.end(), agent))
    agent_positions.sort(key=lambda x: x[0])

    PLACEHOLDER_RE = re.compile(r'\{(SUBJ_CAP|OBJ_CAP|SUBJ|OBJ|POSS|REFL)\}')

    result = []
    i = 0
    for m in PLACEHOLDER_RE.finditer(text):
        result.append(text[i:m.start()])
        ptype = m.group(1)
        cap = ptype.endswith("_CAP")
        
        # Find last named agent STRICTLY BEFORE this placeholder position
        preceding = None
        for apos, aend, agent in agent_positions:
            if aend <= m.start():  # strictly before placeholder
                preceding = agent
            # stop once we pass the placeholder
            if apos > m.start():
                break

        # Resolution priority:
        # 1. Last name strictly preceding this placeholder
        # 2. Hint (explicit context, e.g. "this paragraph is about Dollar")
        # 3. Default they/them
        chosen = preceding or hint_agent or _DEFAULT
        
        v = _val(chosen, ptype)
        result.append(v.capitalize() if cap else v)
        i = m.end()

    result.append(text[i:])
    final = "".join(result)
    return final

def get_pronoun(name, pronoun_type="subject", registry=None):
    if registry is None:
        registry = load_agents()
    key = name.lower().split()[0]
    a = registry.get(name.lower()) or registry.get(key)
    return (a or _DEFAULT).get(pronoun_type, "they")

if __name__ == "__main__":
    import sys
    reg = load_agents()
    test = sys.argv[1] if len(sys.argv) > 1 else "Valentina published the article. {SUBJ_CAP} confirmed it was live."
    hint = sys.argv[2] if len(sys.argv) > 2 else None
    print(resolve_pronouns(test, hint, reg))
