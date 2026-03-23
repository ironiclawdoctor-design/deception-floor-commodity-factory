#!/usr/bin/env python3
"""
Pronoun Skill — v5
Fixes four documented failures from v4:

BUG-1 (T2-02, T4-07): [SUBJ_CAP:Name] / [SUBJ:Name] not resolving to pronoun.
  Root cause: inline regex was only handling 'replace_inline' but the function
  was never actually extracting ptype correctly — ptype.endswith("_CAP") was
  comparing the wrong group.

BUG-2 (T3-05): Junior (they/them) resolved as he.
  Root cause: agents_in_sentence matched 'junior' substring inside longer words.
  Use word-boundary matching.

BUG-3 (T4-04): Neopronoun 'hir' not recognized.
  Root cause: z_hir was in neopronouns but the possessive map didn't include ze→hir.
  Fixed in _possessive. Also confirm Zephyr maps ze/hir correctly.

BUG-4 (T4-08): {POSS} lowercase after period (e.g. 'her' not 'Her' at sentence start).
  Root cause: cap_sentence_start ran before placeholder resolution, so {POSS} that
  resolved to lowercase wasn't post-capitalized. Fix: run cap_sentence_start again
  after placeholder resolution.
"""
import json, re
from pathlib import Path

AGENTS_FILE = Path(__file__).parent / "agents.json"

def load_agents():
    data = json.loads(AGENTS_FILE.read_text())
    registry = {}
    for a in data["agents"] + data.get("neopronouns", []):
        parts = a["pronouns"].split("/")
        subj = parts[0]
        obj = parts[1] if len(parts) > 1 else parts[0]
        entry = {
            "name": a["name"],
            "id": a["id"],
            "subject": subj,
            "object": obj,
            "possessive": _possessive(subj),
            "reflexive": _reflexive(subj),
        }
        # Register by full name (lower), first name, and role aliases
        registry[a["name"].lower()] = entry
        first = a["name"].split()[0].lower()
        if first not in registry:
            registry[first] = entry
        for alias in _role_aliases(a.get("role", "")):
            if alias not in registry:
                registry[alias] = entry
    return registry

def _role_aliases(role):
    if not role:
        return []
    r = role.lower()
    return [r, f"the {r}", r.replace(" ", "_")]

def _possessive(s):
    return {"she": "her", "he": "his", "they": "their",
            "ze": "hir", "xe": "xyr"}.get(s, "their")

def _reflexive(s):
    return {"she": "herself", "he": "himself", "they": "themselves",
            "ze": "hirself", "xe": "xemself"}.get(s, "themselves")

_DEFAULT = {
    "subject": "they", "object": "them", "possessive": "their",
    "reflexive": "themselves", "name": "(default)", "id": "__default__"
}

def _val(a, base_ptype):
    return {
        "SUBJ": a["subject"], "OBJ": a["object"],
        "POSS": a["possessive"], "REFL": a["reflexive"]
    }.get(base_ptype, "they")

def _find_hint(hint, registry):
    if not hint:
        return None
    h = hint.lower()
    return registry.get(h) or registry.get(h.split()[0])

def cap_sentence_start(t):
    """Capitalize first char after '. ' or '." ' or at string start."""
    result = []
    i = 0
    while i < len(t):
        if i == 0 and t[i].isalpha():
            result.append(t[i].upper())
            i += 1
        elif t[i:i+2] == '. ' and i + 2 < len(t) and t[i+2].isalpha():
            result.append('. ')
            result.append(t[i+2].upper())
            i += 3
        elif t[i:i+3] == '." ' and i + 3 < len(t) and t[i+3].isalpha():
            result.append('." ')
            result.append(t[i+3].upper())
            i += 4
        else:
            result.append(t[i])
            i += 1
    return ''.join(result)

def resolve_pronouns(text, last_mentioned=None, registry=None):
    if registry is None:
        registry = load_agents()

    hint = _find_hint(last_mentioned, registry)
    PLACEHOLDER_RE = re.compile(r'\{(SUBJ_CAP|OBJ_CAP|SUBJ|OBJ|POSS|REFL)\}')
    INLINE_RE = re.compile(r'\[(\w+):([^\]]+)\]')

    # ── Pass 1: resolve [TYPE:Name] inline tags ───────────────────────────────
    # BUG-1 fix: correctly extract ptype and cap flag
    inline_anchors = []  # (start_pos_in_original, agent)

    def replace_inline(m):
        ptype_raw = m.group(1).upper()   # e.g. SUBJ_CAP
        name = m.group(2).strip().lower()
        a = registry.get(name) or registry.get(name.split()[0]) or _DEFAULT
        cap = ptype_raw.endswith("_CAP")
        base = ptype_raw.replace("_CAP", "")
        v = _val(a, base)
        inline_anchors.append((m.start(), a))
        return v.capitalize() if cap else v

    text = INLINE_RE.sub(replace_inline, text)

    # Apply sentence-start capitalization after inline resolution
    text = cap_sentence_start(text)

    # ── Build agent position index (word-boundary safe) ──────────────────────
    # BUG-2 fix: use \b word boundaries to avoid 'junior' inside 'adjunct'
    lower_text = text.lower()
    agent_positions = []
    for name, agent in registry.items():
        pattern = r'\b' + re.escape(name) + r'\b'
        for m in re.finditer(pattern, lower_text):
            agent_positions.append((m.start(), m.end(), agent))
    for anchor_pos, anchor_agent in inline_anchors:
        agent_positions.append((anchor_pos, anchor_pos + 1, anchor_agent))
    agent_positions.sort(key=lambda x: x[0])

    # Sentence boundaries
    sentence_breaks = [0]
    for m in re.finditer(r'[.!?]\s+', text):
        sentence_breaks.append(m.end())

    def sentence_of(pos):
        sb = 0
        for b in sentence_breaks:
            if b <= pos:
                sb = b
        return sb

    def agents_in_sentence(sent_start, before_pos):
        return [a for apos, aend, a in agent_positions
                if apos >= sent_start and aend <= before_pos]

    def is_sentence_start(pos):
        sent_start = sentence_of(pos)
        segment = text[sent_start:pos].strip()
        return len(segment) == 0

    # ── Pass 2: resolve {PLACEHOLDER}s ───────────────────────────────────────
    result = []
    i = 0

    for m in PLACEHOLDER_RE.finditer(text):
        result.append(text[i:m.start()])
        ptype = m.group(1)
        cap = ptype.endswith("_CAP")
        base = ptype.replace("_CAP", "")
        at_sent_start = is_sentence_start(m.start())

        sent_start = sentence_of(m.start())
        local_agents = agents_in_sentence(sent_start, m.start())
        last_local = local_agents[-1] if local_agents else None

        global_before = [a for apos, aend, a in agent_positions if aend <= sent_start]
        last_global = global_before[-1] if global_before else None

        in_quote = _is_inside_quote(text, m.start())
        subj_already_set = _subj_in_sentence(text, sent_start, m.start())

        if base == "SUBJ":
            chosen = (hint if in_quote else None) or last_local or hint or last_global or _DEFAULT
        elif base == "OBJ":
            if in_quote:
                chosen = hint or last_local or last_global or _DEFAULT
            elif subj_already_set and hint and hint.get("id") != (last_local or {}).get("id"):
                chosen = hint
            elif hint and last_local and hint.get("id") != last_local.get("id"):
                chosen = hint
            else:
                chosen = hint or last_local or last_global or _DEFAULT
        elif base == "POSS":
            if in_quote:
                chosen = hint or last_local or last_global or _DEFAULT
            elif subj_already_set and hint and hint.get("id") != (last_local or {}).get("id"):
                other = _find_other_agent(local_agents, last_local)
                chosen = other or hint or last_local or _DEFAULT
            else:
                chosen = last_local or hint or last_global or _DEFAULT
        elif base == "REFL":
            chosen = hint or last_local or last_global or _DEFAULT
        else:
            chosen = last_local or hint or last_global or _DEFAULT

        v = _val(chosen, base)
        if cap or at_sent_start:
            v = v.capitalize()
        result.append(v)
        i = m.end()

    result.append(text[i:])
    final = ''.join(result)

    # BUG-4 fix: run cap_sentence_start AGAIN after placeholder resolution
    # (placeholders resolved to lowercase may now sit at sentence starts)
    return cap_sentence_start(final)

def _is_inside_quote(text, pos):
    return text[:pos].count('"') % 2 == 1

def _subj_in_sentence(text, sent_start, pos):
    segment = text[sent_start:pos]
    return bool(re.search(r'\{SUBJ(?:_CAP)?\}', segment))

def _find_other_agent(local_agents, exclude):
    if not exclude:
        return None
    for a in local_agents:
        if a.get("id") != exclude.get("id"):
            return a
    return None

def get_pronoun(name, pronoun_type="subject", registry=None):
    if registry is None:
        registry = load_agents()
    key = name.lower().split()[0]
    a = registry.get(name.lower()) or registry.get(key)
    return (a or _DEFAULT).get(pronoun_type, "they")

if __name__ == "__main__":
    import sys
    reg = load_agents()
    test = sys.argv[1] if len(sys.argv) > 1 else "Dollar manages the ledger. {POSS} reports go to Nate."
    hint = sys.argv[2] if len(sys.argv) > 2 else "Dollar"
    print(resolve_pronouns(test, hint, reg))
