#!/usr/bin/env python3
"""
Pronoun Skill — v1 baseline
Resolves pronouns in agency communications.

Given: a sentence or paragraph, an agent registry, and a context dict
Returns: the sentence with correct pronouns applied

v1 approach: simple name→pronoun lookup with last-mentioned antecedent heuristic.
Expected ceiling: ~70-75% (Tier 1+2 only, Tier 3+ will fail)
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
        registry[a["name"].lower()] = {
            "name": a["name"],
            "id": a["id"],
            "subject": pronouns[0],    # she/he/they/ze/xe
            "object": pronouns[1],     # her/him/them/hir/xem
            "possessive": _possessive(pronouns[0]),
            "reflexive": _reflexive(pronouns[0]),
        }
        # Also index by first name
        first = a["name"].split()[0].lower()
        if first not in registry:
            registry[first] = registry[a["name"].lower()]
    return registry

def _possessive(subject):
    return {"she": "her", "he": "his", "they": "their",
            "ze": "hir", "xe": "xyr"}.get(subject, "their")

def _reflexive(subject):
    return {"she": "herself", "he": "himself", "they": "themselves",
            "ze": "hirself", "xe": "xemself"}.get(subject, "themselves")

def resolve_pronouns(text, last_mentioned=None, registry=None):
    """
    Given text and optional last-mentioned agent name,
    resolve placeholder pronouns.
    
    Placeholders: {SUBJ}, {OBJ}, {POSS}, {REFL}
    Or inline: [SUBJ:AgentName], [OBJ:AgentName], etc.
    
    v1 strategy: last-mentioned antecedent wins.
    """
    if registry is None:
        registry = load_agents()
    
    # Find most recently mentioned agent in text
    agent = _find_last_mentioned(text, registry, last_mentioned)
    
    if not agent:
        # Default to they/them
        agent = {"subject": "they", "object": "them", "possessive": "their", "reflexive": "themselves"}
    
    # Replace placeholders
    text = text.replace("{SUBJ}", agent["subject"])
    text = text.replace("{OBJ}", agent["object"])
    text = text.replace("{POSS}", agent["possessive"])
    text = text.replace("{REFL}", agent["reflexive"])
    
    # Capitalized versions
    text = text.replace("{SUBJ_CAP}", agent["subject"].capitalize())
    text = text.replace("{OBJ_CAP}", agent["object"].capitalize())
    
    # Inline: [SUBJ:Name]
    def replace_inline(m):
        pronoun_type = m.group(1)
        name = m.group(2).lower()
        a = registry.get(name, agent)
        return {
            "SUBJ": a["subject"], "OBJ": a["object"],
            "POSS": a["possessive"], "REFL": a["reflexive"],
        }.get(pronoun_type, m.group(0))
    
    text = re.sub(r'\[(\w+):([^\]]+)\]', replace_inline, text)
    
    return text

def _find_last_mentioned(text, registry, hint=None):
    """Find the last agent mentioned by name in text."""
    if hint:
        h = hint.lower()
        if h in registry:
            return registry[h]
        first = h.split()[0]
        if first in registry:
            return registry[first]
    
    # Scan text for agent names (last occurrence wins)
    lower = text.lower()
    last_pos = -1
    last_agent = None
    
    for name, agent in registry.items():
        pos = lower.rfind(name)
        if pos > last_pos:
            last_pos = pos
            last_agent = agent
    
    return last_agent

def get_pronoun(name, pronoun_type="subject", registry=None):
    """Direct lookup: get a specific pronoun for a named agent."""
    if registry is None:
        registry = load_agents()
    key = name.lower().split()[0]
    agent = registry.get(name.lower()) or registry.get(key)
    if not agent:
        return {"subject": "they", "object": "them", "possessive": "their", "reflexive": "themselves"}.get(pronoun_type, "they")
    return agent.get(pronoun_type, "they")

if __name__ == "__main__":
    import sys
    reg = load_agents()
    test = sys.argv[1] if len(sys.argv) > 1 else "Valentina published the article. {SUBJ_CAP} confirmed it was live."
    hint = sys.argv[2] if len(sys.argv) > 2 else None
    print(resolve_pronouns(test, hint, reg))
