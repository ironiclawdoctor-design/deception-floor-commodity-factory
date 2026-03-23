#!/usr/bin/env python3
"""
Pronoun Skill — v4
Full sentence-aware resolution with multi-role context.

Key insight from v1-v3 failures:
- {SUBJ}/{SUBJ_CAP} usually refers to the grammatical subject → last mentioned OR hint
- {OBJ} usually refers to a different agent than {SUBJ} in same sentence → hint often right
- {POSS}/{REFL} follow the most recently introduced agent UNLESS hint overrides
- Sentence-start detection required for {POSS} capitalization
- Inline [SUBJ:Name] without _CAP suffix must not capitalize (already fixed in v2/v3 but
  the [SUBJ:Dollar] bug is that the inline resolver is *replacing* the word but not
  capitalizing when it's the start of a sentence — fixed by post-processing)

v4 approach:
1. Inline [TYPE:Name] → resolved (with cap for _CAP variant, no cap otherwise)
2. Post-process: capitalize any resolved pronoun that follows ". " or starts the string
3. For {PLACEHOLDER}s: use per-sentence agent context:
   - Split into sentences
   - Each sentence: named agents mentioned = subject candidates
   - {SUBJ}/{SUBJ_CAP}: last preceding name in sentence, or hint
   - {OBJ}: if hint is different from last preceding name, use hint
   - {POSS}/{REFL}: follow last preceding name
4. Capitalize {POSS} (and any placeholder) that is sentence-initial
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
            for alias in [a["role"].lower(), f"the {a['role'].lower()}", a["role"].lower().replace(" ","_")]:
                if alias not in registry:
                    registry[alias] = entry
    return registry

def _possessive(s):
    return {"she":"her","he":"his","they":"their","ze":"hir","xe":"xyr"}.get(s,"their")
def _reflexive(s):
    return {"she":"herself","he":"himself","they":"themselves","ze":"hirself","xe":"xemself"}.get(s,"themselves")

_DEFAULT = {"subject":"they","object":"them","possessive":"their","reflexive":"themselves","name":"(default)"}

def _val(a, base_ptype):
    return {"SUBJ": a["subject"], "OBJ": a["object"],
            "POSS": a["possessive"], "REFL": a["reflexive"]}.get(base_ptype, "they")

def _find_hint(hint, registry):
    if not hint:
        return None
    h = hint.lower()
    return registry.get(h) or registry.get(h.split()[0])

def resolve_pronouns(text, last_mentioned=None, registry=None):
    if registry is None:
        registry = load_agents()

    hint = _find_hint(last_mentioned, registry)
    PLACEHOLDER_RE = re.compile(r'\{(SUBJ_CAP|OBJ_CAP|SUBJ|OBJ|POSS|REFL)\}')

    # ── Pass 1: resolve [INLINE:Name] — track resolved agent positions ───────
    # After replacement, inject a zero-width name anchor so position tracking works
    inline_anchors = []  # list of (position_in_final_text, agent)
    
    def replace_inline(m):
        ptype = m.group(1).upper()
        name = m.group(2).strip().lower()
        a = registry.get(name) or registry.get(name.split()[0]) or _DEFAULT
        cap = ptype.endswith("_CAP")
        v = _val(a, ptype.replace("_CAP",""))
        result_word = v.capitalize() if cap else v
        # Record that at this position, agent 'a' was resolved
        inline_anchors.append((m.start(), a))
        return result_word

    text = re.sub(r'\[(\w+):([^\]]+)\]', replace_inline, text)

    # ── Pass 1b: capitalize any resolved pronoun at sentence start ────────────
    # After inline resolution, a lowercase pronoun may be at sentence start
    def cap_sentence_start(t):
        # Capitalize first word after ". " or at string start
        result = []
        i = 0
        while i < len(t):
            if i == 0 and t[i].isalpha():
                result.append(t[i].upper())
                i += 1
            elif t[i:i+2] == '. ' and i+2 < len(t) and t[i+2].isalpha():
                result.append('. ')
                result.append(t[i+2].upper())
                i += 3
            elif t[i:i+3] == '." ' and i+3 < len(t) and t[i+3].isalpha():
                result.append('." ')
                result.append(t[i+3].upper())
                i += 4
            else:
                result.append(t[i])
                i += 1
        return ''.join(result)

    text = cap_sentence_start(text)

    # ── Pass 2: resolve {PLACEHOLDER}s with sentence-aware context ───────────
    lower_text = text.lower()

    # Map all agent name positions + inline anchor positions
    agent_positions = []
    for name, agent in registry.items():
        for m in re.finditer(re.escape(name), lower_text):
            agent_positions.append((m.start(), m.end(), agent))
    # Add inline-resolved agents at their approximate positions
    for anchor_pos, anchor_agent in inline_anchors:
        agent_positions.append((anchor_pos, anchor_pos + 1, anchor_agent))
    agent_positions.sort(key=lambda x: x[0])

    # Find sentence boundaries
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
        """All agents mentioned in same sentence before given position."""
        result = []
        for apos, aend, agent in agent_positions:
            if apos >= sent_start and aend <= before_pos:
                result.append(agent)
        return result

    def is_sentence_start(pos, text):
        """Is this position at or very near a sentence start?"""
        # Check if only whitespace or nothing precedes within current sentence
        sent_start = sentence_of(pos)
        segment = text[sent_start:pos].strip()
        return len(segment) == 0

    result = []
    i = 0

    for m in PLACEHOLDER_RE.finditer(text):
        result.append(text[i:m.start()])
        ptype = m.group(1)
        cap = ptype.endswith("_CAP")
        base = ptype.replace("_CAP", "")
        at_sent_start = is_sentence_start(m.start(), text)

        sent_start = sentence_of(m.start())
        # Agents in current sentence, before this placeholder
        local_agents = agents_in_sentence(sent_start, m.start())
        last_local = local_agents[-1] if local_agents else None

        # Agents before current sentence (global context)
        global_before = [a for apos, aend, a in agent_positions if aend <= sent_start]
        last_global = global_before[-1] if global_before else None

        # Detect if we're inside a quoted string
        in_quote = _is_inside_quote(text, m.start())

        # Detect if a {SUBJ} placeholder already fired in this sentence
        subj_already_set = _subj_in_sentence(text, sent_start, m.start())

        # Resolution logic:
        if base == "SUBJ":
            if in_quote:
                # Inside quoted speech, hint = the speaker
                chosen = hint or last_local or last_global or _DEFAULT
            else:
                chosen = last_local or hint or last_global or _DEFAULT
        elif base == "OBJ":
            if in_quote:
                # Inside quote, OBJ = hint (speaker's possessions/objects)
                chosen = hint or last_local or last_global or _DEFAULT
            elif subj_already_set and hint:
                # Subject already resolved → object is likely the OTHER agent → hint
                # But only if hint differs from last_local
                if hint.get("id") != (last_local or {}).get("id"):
                    chosen = hint
                else:
                    # Both agents in sentence: pick the one that's NOT last_local
                    other = _find_other_agent(local_agents, last_local)
                    chosen = other or hint or _DEFAULT
            elif hint and last_local and hint.get("id") != last_local.get("id"):
                chosen = hint
            else:
                chosen = hint or last_local or last_global or _DEFAULT
        elif base == "POSS":
            if in_quote:
                # Inside quote, possessive = hint (speaker owns it)
                chosen = hint or last_local or last_global or _DEFAULT
            elif subj_already_set and hint:
                # Possessive after subject resolved → use non-last-local (the other agent)
                if hint.get("id") != (last_local or {}).get("id"):
                    other = _find_other_agent(local_agents, last_local)
                    chosen = other or hint or last_local or _DEFAULT
                else:
                    chosen = last_local or hint or last_global or _DEFAULT
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
    """Return True if position is inside a double-quoted string."""
    before = text[:pos]
    return before.count('"') % 2 == 1

def _subj_in_sentence(text, sent_start, pos):
    """Return True if a {SUBJ} placeholder appears before pos in same sentence."""
    segment = text[sent_start:pos]
    return bool(re.search(r'\{SUBJ(?:_CAP)?\}', segment))

def _find_other_agent(local_agents, exclude):
    """Find first local agent that differs from exclude."""
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
    test = sys.argv[1] if len(sys.argv) > 1 else "Valentina published the article. {SUBJ_CAP} confirmed it was live."
    hint = sys.argv[2] if len(sys.argv) > 2 else None
    print(resolve_pronouns(test, hint, reg))
