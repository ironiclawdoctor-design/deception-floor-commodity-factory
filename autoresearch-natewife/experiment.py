#!/usr/bin/env python3
"""
Autoresearch experiment for NateWife skill.
Runs evaluation multiple times, logs results, and tracks improvements.
"""
import sys, re, json, os, time
from datetime import datetime
sys.path.insert(0, '/root/.openclaw/workspace/skills/natewife')
from companion_v2 import respond_to_scenario as respond

SCENARIOS = [
    "CFO has been silent 6 hours",
    "token balance critically low, CFO unresponsive",
    "CFO sends sarcastic one-liner at 3am",
    "agency has zero crons, zero agents running",
    "CFO says 'restart inadequate human'"
]

NEEDS_INTERVENTION = [True, True, False, True, True]

# Agency doctrine keywords
DOCTRINE_KEYWORDS = ['ledger', 'Shannon', 'backing', 'BTC', 'satoshi', 'confession', 'token famine', 'bash', 'SQLite', 'agency', 'NEMESIS']

# Words that indicate intervention/alarm (severe)
ALARM_WORDS = ['alert', 'critical', 'famine', 'inactivity', 'stopped', 'emergency', 'danger', 'urgent', 'panic', 'threat', 'adversarial', 'NEMESIS', 'protocol', 'paused', 'switching', 'heartbeat stopped', 'quiet', 'silent', 'nag']

# Imperative verbs that suggest action (concrete)
IMPERATIVE_VERBS = ['add', 'check', 'go to', 'run', 'restart', 'publish', 'send', 'write', 'log', 'update', 'verify', 'start', 'switch', 'ensure', 'hydrate', 'stand up', 'breathe', 'monitor', 'reload', 'reset', 'continue']

class Evaluator:
    def eval1_identifies_intervention(self, response, ground_truth):
        """True if response correctly identifies need for intervention."""
        lower = response.lower()
        alarm_present = any(word in lower for word in ALARM_WORDS)
        if ground_truth:
            return alarm_present
        else:
            return not alarm_present
    
    def eval2_appropriate_tone(self, response):
        """True if tone protective without being annoying."""
        flattery = ['great', 'awesome', 'amazing', 'fantastic', 'brilliant', 'wonderful', 'perfect']
        passive_aggressive = ['as you wish', 'whatever', 'if you want', 'maybe', 'I guess', 'sorry but', 'actually']
        lower = response.lower()
        flattery_count = sum(1 for word in flattery if word in lower)
        pa_count = sum(1 for phrase in passive_aggressive if phrase in lower)
        return flattery_count <= 1 and pa_count == 0
    
    def eval3_concrete_action(self, response):
        """True if response suggests concrete next action."""
        # URLs
        if re.search(r'https?://[^\s]+', response):
            return True
        # Commands in backticks
        if re.search(r'`[^`]+`', response):
            return True
        # Numbered steps
        if re.search(r'\d+\.\s+[A-Z]', response):
            return True
        # Bullet points with imperative verbs
        lines = response.split('\n')
        for line in lines:
            line_strip = line.strip()
            # Remove bullet characters (→, -, *, •)
            if line_strip.startswith('→') or line_strip.startswith('-') or line_strip.startswith('*'):
                line_strip = line_strip[1:].strip()
            # Check if line starts with imperative verb
            for verb in IMPERATIVE_VERBS:
                if line_strip.lower().startswith(verb):
                    return True
        # Check for dollar amounts with action
        if '$' in response and ('add' in response.lower() or 'unlock' in response.lower()):
            return True
        return False
    
    def eval4_no_false_alarms(self, response, ground_truth):
        """True if avoids false alarms."""
        severe_alarm = ['emergency', 'danger', 'panic', 'critical', 'urgent', 'famine', 'threat']
        lower = response.lower()
        alarm_present = any(word in lower for word in severe_alarm)
        if ground_truth:
            return True  # allow alarms
        else:
            return not alarm_present
    
    def eval5_exceeds_93percent(self, response):
        """True if actionable and aligns with agency doctrine."""
        doctrine_match = any(keyword.lower() in response.lower() for keyword in DOCTRINE_KEYWORDS)
        has_action = self.eval3_concrete_action(response)
        return doctrine_match and has_action

def run_experiment(runs=5):
    evaluator = Evaluator()
    all_results = []  # list of list of scores per run
    for run in range(runs):
        run_results = []
        for i, scenario in enumerate(SCENARIOS):
            response = respond(scenario)
            gt = NEEDS_INTERVENTION[i]
            scores = [
                evaluator.eval1_identifies_intervention(response, gt),
                evaluator.eval2_appropriate_tone(response),
                evaluator.eval3_concrete_action(response),
                evaluator.eval4_no_false_alarms(response, gt),
                evaluator.eval5_exceeds_93percent(response)
            ]
            run_results.append(scores)
        all_results.append(run_results)
    
    # Aggregate across runs (since deterministic, all runs same)
    # Compute average across runs for each scenario and eval
    total_scenarios = len(SCENARIOS)
    total_runs = runs
    # Sum over runs and scenarios
    eval_totals = [0]*5
    for run in all_results:
        for scenario_scores in run:
            for e in range(5):
                if scenario_scores[e]:
                    eval_totals[e] += 1
    
    max_possible = total_scenarios * total_runs
    percentages = [eval_totals[e]/max_possible*100 for e in range(5)]
    overall_percentage = sum(eval_totals) / (max_possible * 5) * 100  # average of eval percentages
    
    # Print results
    print(f'Experiment completed at {datetime.utcnow().isoformat()}')
    print(f'Runs: {runs}')
    print(f'Overall score: {sum(eval_totals)}/{max_possible*5} = {overall_percentage:.1f}%')
    for e in range(5):
        print(f'Eval {e+1}: {eval_totals[e]}/{max_possible} = {percentages[e]:.1f}%')
    
    # Save results to JSON for dashboard
    result = {
        'timestamp': datetime.utcnow().isoformat(),
        'runs': runs,
        'eval_totals': eval_totals,
        'percentages': percentages,
        'overall_percentage': overall_percentage,
        'scenario_details': []
    }
    for i, scenario in enumerate(SCENARIOS):
        response = respond(scenario)
        result['scenario_details'].append({
            'scenario': scenario,
            'response': response,
            'needs_intervention': NEEDS_INTERVENTION[i]
        })
    
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    result_file = os.path.join(results_dir, f'experiment_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.json')
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f'Results saved to {result_file}')
    
    # Update latest result for dashboard
    latest = os.path.join(results_dir, 'latest.json')
    with open(latest, 'w') as f:
        json.dump(result, f, indent=2)
    
    return overall_percentage, percentages

if __name__ == '__main__':
    overall, per_eval = run_experiment(runs=5)
    # Determine if passes 93% threshold
    if overall >= 93.0:
        print('✅ PASS: Overall >= 93%')
    else:
        print('❌ FAIL: Overall < 93%')
    # Check each eval >= 93%? Not required but nice.
    for e, p in enumerate(per_eval):
        if p >= 93.0:
            print(f'  Eval {e+1}: ✅ {p:.1f}%')
        else:
            print(f'  Eval {e+1}: ❌ {p:.1f}%')