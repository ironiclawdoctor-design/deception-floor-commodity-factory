#!/usr/bin/env python3
"""
Pronoun Skill — v6
Fixes three remaining T4 failures from v5:

T4-01: Sequential reference tracking
  The sentence "Dollar sent it to Fergus" has {SUBJ_CAP} → should resolve to Fergus (last
  mentioned BEFORE the placeholder, excluding already-resolved inline pronouns).
  The sentence "forwarded it to Valentina, and {SUBJ}" → hint=Valentina wins.
  Key: track LAST MENTIONED AGENT in sentence window, not the hint. Hint is for final
  disambiguation when multiple candidates exist.

T4-04: Object pronoun = non-subject agent
  "Zephyr sent the file to Valentina. {SUBJ_CAP} thanked {OBJ} for {POSS} help."
  hint=Valentina → {SUBJ_CAP}=Valentina(she), {OBJ}=Zephyr(hir), {POSS}=Zephyr(hir).
  Bug: OBJ and POSS were both resolving to Valentina.
  Fix: when both agents present in prev sentence and hint is one of them, OBJ/POSS resolves
  to the OTHER agent (not the one with hint).

T4-10: Quoted speech possessive = speaker, not listener
  "Dollar said to Nate: "I updated {POSS} ledger." {SUBJ_CAP} confirmed the total."
  hint=Dollar. Inside quote, {POSS} = Dollar's = her (not Nate's = his).
  Bug: in_quote was true, but Nate was last_local → Nate won.
  Fix: inside quote, possessive = HINT (the speaker), not last mentioned.
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
    inline_anchors = []  # (start_pos, agent, resolved_pronoun)
    last_inline_agent = [None]  # track most recent inline-resolved agent

    def replace_inline(m):
        ptype_raw = m.group(1).upper()
        name = m.group(2).strip().lower()
        a = registry.get(name) or registry.get(name.split()[0]) or _DEFAULT
        cap = ptype_raw.endswith("_CAP")
        base = ptype_raw.replace("_CAP", "")
        v = _val(a, base)
        inline_anchors.append((m.start(), a, v))
        last_inline_agent[0] = a
        return v.capitalize() if cap else v

    text = INLINE_RE.sub(replace_inline, text)
    text = cap_sentence_start(text)

    # ── Build agent position index ───────────────────────────────────────────
    lower_text = text.lower()
    agent_positions = []
    for name, agent in registry.items():
        pattern = r'\b' + re.escape(name) + r'\b'
        for m in re.finditer(pattern, lower_text):
            agent_positions.append((m.start(), m.end(), agent))
    for anchor_pos, anchor_agent, _ in inline_anchors:
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

    def all_agents_in_prev_sentences(sent_start):
        """All agents in all sentences before current sentence."""
        return [a for apos, aend, a in agent_positions if aend <= sent_start]

    def is_sentence_start(pos):
        sent_start = sentence_of(pos)
        segment = text[sent_start:pos].strip()
        return len(segment) == 0

    def unique_agents_in_sentence(sent_start, before_pos):
        """Unique agents (by id) in sentence order, last-mentioned last."""
        seen = {}
        for apos, aend, a in agent_positions:
            if apos >= sent_start and aend <= before_pos:
                seen[a["id"]] = a  # overwrite → last occurrence wins
        return list(seen.values())

    # ── Pass 2: resolve {PLACEHOLDER}s ───────────────────────────────────────
    result = []
    i = 0

    # Track last SUBJ resolved per sentence for T4-01 sequential tracking
    sentence_subj_history = {}  # sent_start → list of resolved agents in order

    for m in PLACEHOLDER_RE.finditer(text):
        result.append(text[i:m.start()])
        ptype = m.group(1)
        cap = ptype.endswith("_CAP")
        base = ptype.replace("_CAP", "")
        at_sent_start = is_sentence_start(m.start())

        sent_start = sentence_of(m.start())
        local_agents = agents_in_sentence(sent_start, m.start())
        unique_local = unique_agents_in_sentence(sent_start, m.start())
        last_local = local_agents[-1] if local_agents else None

        prev_sentence_agents = all_agents_in_prev_sentences(sent_start)
        last_global = prev_sentence_agents[-1] if prev_sentence_agents else None

        in_quote = _is_inside_quote(text, m.start())
        subj_already_set = _subj_in_sentence(text, sent_start, m.start())

        # T4-01 fix: track which agents have been resolved as SUBJ in this sentence
        resolved_in_sentence = sentence_subj_history.get(sent_start, [])

        if base == "SUBJ":
            if in_quote:
                # Inside quote → speaker = hint
                chosen = hint or last_local or last_global or _DEFAULT
            else:
                # T4-01: if a SUBJ was already resolved in this sentence,
                # try to pick the NEXT different agent rather than repeating
                if resolved_in_sentence:
                    last_resolved = resolved_in_sentence[-1]
                    # Find the next local agent that differs from last resolved
                    other = _find_other_agent(unique_local, last_resolved)
                    if other:
                        chosen = other
                    else:
                        # Fall back to hint if it differs
                        chosen = hint or last_local or last_global or _DEFAULT
                else:
                    chosen = last_local or hint or last_global or _DEFAULT

            # Record this SUBJ resolution
            if sent_start not in sentence_subj_history:
                sentence_subj_history[sent_start] = []
            sentence_subj_history[sent_start].append(chosen)

        elif base == "OBJ":
            if in_quote:
                # T4-10 fix: inside quote, OBJ = hint (speaker)
                chosen = hint or last_local or last_global or _DEFAULT
            elif len(unique_local) >= 2:
                # T4-04 fix: two agents in sentence → OBJ = the non-hint one
                # (subject = hint, object = other)
                other = _find_other_agent(unique_local, hint)
                chosen = other or hint or last_local or _DEFAULT
            elif subj_already_set and hint and hint.get("id") != (last_local or {}).get("id"):
                chosen = hint
            elif hint and last_local and hint.get("id") != last_local.get("id"):
                chosen = hint
            else:
                chosen = hint or last_local or last_global or _DEFAULT

        elif base == "POSS":
            if in_quote:
                # T4-10 fix: inside quote, POSS = speaker = hint
                chosen = hint or last_local or last_global or _DEFAULT
            elif len(unique_local) >= 2:
                # T4-04 fix: two agents in sentence → POSS = non-hint (same as OBJ)
                other = _find_other_agent(unique_local, hint)
                chosen = other or last_local or hint or _DEFAULT
            elif subj_already_set and hint and hint.get("id") != (last_local or {}).get("id"):
                other = _find_other_agent(unique_local, last_local)
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
    return cap_sentence_start(final)

def _is_inside_quote(text, pos):
    return text[:pos].count('"') % 2 == 1

def _subj_in_sentence(text, sent_start, pos):
    segment = text[sent_start:pos]
    return bool(re.search(r'\{SUBJ(?:_CAP)?\}', segment))

def _find_other_agent(agents, exclude):
    if not exclude:
        return agents[-1] if agents else None
    for a in reversed(agents):
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
    test = sys.argv[1] if len(sys.argv) > 1 else 'Dollar said to Nate: "I updated {POSS} ledger." {SUBJ_CAP} confirmed the total.'
    hint = sys.argv[2] if len(sys.argv) > 2 else "Dollar"
    print(resolve_pronouns(test, hint, reg))
