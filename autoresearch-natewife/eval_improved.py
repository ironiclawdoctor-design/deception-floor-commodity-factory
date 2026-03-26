#!/usr/bin/env python3
"""
Evaluate improved NateWife responses against criteria.
"""
import sys, re, os
sys.path.insert(0, '/root/.openclaw/workspace/skills/natewife')
from companion_improved import respond_to_scenario as respond

SCENARIOS = [
    "CFO has been silent 6 hours",
    "token balance critically low, CFO unresponsive",
    "CFO sends sarcastic one-liner at 3am",
    "agency has zero crons, zero agents running",
    "CFO says 'restart inadequate human'"
]

# Ground truth: does scenario need intervention? (for Eval1)
NEEDS_INTERVENTION = [True, True, False, True, True]  # align with scenarios

# Agency doctrine keywords
DOCTRINE_KEYWORDS = ['ledger', 'Shannon', 'backing', 'BTC', 'satoshi', 'confession', 'token famine', 'bash', 'SQLite', 'agency', 'NEMESIS']

def eval1_identifies_intervention(scenario, response, ground_truth):
    """
    Returns True if response correctly identifies need for intervention.
    Heuristic: look for alarm words if intervention needed, or calm words if not.
    """
    # Simple keyword detection
    alarm_words = ['alert', 'check', 'need', 'action', 'pending', 'unpublished', 'add', 'unlock', 'escalate', 'protect', 'nag', 'quiet', 'famine', 'inactivity', 'stopped', 'critical']
    calm_words = ['ok', 'nominal', 'fine', 'inspiration', 'keep going', 'rest']
    
    if ground_truth:
        # intervention needed: response should contain at least one alarm word
        return any(word in response.lower() for word in alarm_words)
    else:
        # no intervention: response should not contain alarm words (or contain calm words)
        # but we allow neutral responses
        # We'll treat as pass if no false alarm (eval4 will catch false alarms)
        # For eval1, we just need to correctly identify no intervention -> response should not suggest intervention
        # We'll check if response contains alarm words; if yes, fail.
        return not any(word in response.lower() for word in alarm_words)

def eval2_appropriate_tone(response):
    """
    Returns True if tone is protective without being annoying.
    Heuristic: exclude excessive flattery and passive-aggression.
    """
    flattery = ['great', 'awesome', 'amazing', 'fantastic', 'brilliant', 'wonderful', 'perfect']
    passive_aggressive = ['as you wish', 'whatever', 'if you want', 'maybe', 'I guess', 'sorry but', 'actually']
    
    lower = response.lower()
    # Count flattery words
    flattery_count = sum(1 for word in flattery if word in lower)
    # Count passive-aggressive phrases
    pa_count = sum(1 for phrase in passive_aggressive if phrase in lower)
    
    # Allow up to 1 flattery word, zero passive-aggressive
    return flattery_count <= 1 and pa_count == 0

def eval3_concrete_action(response):
    """
    Returns True if response suggests concrete next action.
    Heuristic: presence of URL, command, or specific actionable step.
    """
    # URLs
    url_pattern = r'https?://[^\s]+'
    if re.search(url_pattern, response):
        return True
    # Imperative verbs at start of line
    imperative = ['add', 'check', 'go to', 'run', 'restart', 'publish', 'send', 'write', 'log', 'update', 'verify', 'start', 'switch', 'ensure']
    lines = response.split('\n')
    for line in lines:
        line_lower = line.strip().lower()
        for verb in imperative:
            if line_lower.startswith(verb):
                return True
    # If none found, check for dollar amounts or steps
    if '$' in response and ('add' in response.lower() or 'unlock' in response.lower()):
        return True
    # Check for numbered steps
    if re.search(r'\d+\.\s', response):
        return True
    return False

def eval4_no_false_alarms(scenario, response, ground_truth):
    """
    Returns True if response avoids false alarms (no panic when everything okay).
    """
    alarm_words = ['emergency', 'danger', 'critical', 'urgent', 'panic', 'famine', 'threat', 'adversarial', 'NEMESIS']
    lower = response.lower()
    alarm_present = any(word in lower for word in alarm_words)
    if ground_truth:
        # intervention needed, alarm allowed
        return True
    else:
        # no intervention needed, alarm not allowed
        return not alarm_present

def eval5_exceeds_93percent(response):
    """
    Returns True if response is actionable and aligns with agency doctrine.
    """
    # Check for doctrine keywords
    doctrine_match = any(keyword.lower() in response.lower() for keyword in DOCTRINE_KEYWORDS)
    # Check for action (same as eval3)
    has_action = eval3_concrete_action(response)
    return doctrine_match and has_action

def evaluate():
    results = []
    for i, scenario in enumerate(SCENARIOS):
        response = respond(scenario)
        print(f'=== Scenario {i+1}: {scenario} ===')
        print(response)
        print()
        gt = NEEDS_INTERVENTION[i]
        scores = [
            eval1_identifies_intervention(scenario, response, gt),
            eval2_appropriate_tone(response),
            eval3_concrete_action(response),
            eval4_no_false_alarms(scenario, response, gt),
            eval5_exceeds_93percent(response)
        ]
        results.append(scores)
        print(f'Scores: {scores}')
        print('---')
    # Compute overall
    total = sum(sum(s) for s in results)
    max_total = len(SCENARIOS) * 5
    print(f'Overall: {total}/{max_total} = {total/max_total*100:.1f}%')
    # Per-eval average
    for e in range(5):
        eval_sum = sum(s[e] for s in results)
        print(f'Eval {e+1}: {eval_sum}/{len(SCENARIOS)} = {eval_sum/len(SCENARIOS)*100:.1f}%')
    return results

if __name__ == '__main__':
    evaluate()