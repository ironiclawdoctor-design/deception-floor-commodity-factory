#!/usr/bin/env python3
"""
Compare baseline vs optimized prompts.
"""

import re
from pathlib import Path

def evaluate_prompt(prompt_text):
    """Evaluate prompt quality based on heuristics. Returns score 0-100."""
    score = 0
    max_score = 100
    
    # 1. Length check (20-200 words optimal)
    words = len(prompt_text.split())
    if 20 <= words <= 200:
        score += 20
    elif words < 10:
        score += 5
    elif words > 500:
        score += 5
    else:
        score += 15
    
    # 2. Structure indicators
    has_bullets = bool(re.search(r'^[\-\*•]|\d+\.', prompt_text, re.MULTILINE))
    has_questions = bool(re.search(r'\?', prompt_text))
    has_context = bool(re.search(r'(context|background|goal|objective|constraint|need|want)', prompt_text, re.IGNORECASE))
    
    if has_bullets:
        score += 15
    if has_questions:
        score += 10
    if has_context:
        score += 15
    
    # 3. Clarity indicators
    has_specifics = bool(re.search(r'\b(specific|exact|precise|detailed|concrete)\b', prompt_text, re.IGNORECASE))
    has_actions = bool(re.search(r'\b(do|make|create|build|write|analyze|check|find|use|take|optimize|focus)\b', prompt_text, re.IGNORECASE))
    has_outcome = bool(re.search(r'\b(outcome|result|deliverable|output|goal|objective|better|improve|effective)\b', prompt_text, re.IGNORECASE))
    
    if has_specifics:
        score += 10
    if has_actions:
        score += 10
    if has_outcome:
        score += 10
    
    # 4. Readability
    sentences = re.split(r'[.!?]+', prompt_text)
    if len(sentences) > 1:
        avg_len = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
        if 5 <= avg_len <= 25:
            score += 10
    
    return min(score, max_score)

def read_prompts():
    """Read baseline and optimized prompts from template file."""
    template_path = Path("/root/.openclaw/workspace/autoresearch/prompt-templates/test-prompt.md")
    content = template_path.read_text()
    
    # Extract sections
    baseline_match = re.search(r'## Baseline Prompt.*?\n(.*?)(?=\n##|\n###|\n#|$)', content, re.DOTALL | re.IGNORECASE)
    optimized_match = re.search(r'## Optimized Variant.*?\n(.*?)(?=\n##|\n###|\n#|$)', content, re.DOTALL | re.IGNORECASE)
    
    baseline = baseline_match.group(1).strip() if baseline_match else ""
    optimized = optimized_match.group(1).strip() if optimized_match else ""
    
    return baseline, optimized

def main():
    print("=== Prompt Comparison Experiment ===\n")
    
    baseline, optimized = read_prompts()
    
    if not baseline:
        print("Error: Could not find baseline prompt")
        return 1
    
    print("1. BASELINE PROMPT:")
    print(f'   "{baseline[:80]}..."' if len(baseline) > 80 else f'   "{baseline}"')
    baseline_score = evaluate_prompt(baseline)
    print(f"   Score: {baseline_score}/100\n")
    
    if optimized:
        print("2. OPTIMIZED PROMPT:")
        print(f'   "{optimized[:80]}..."' if len(optimized) > 80 else f'   "{optimized}"')
        optimized_score = evaluate_prompt(optimized)
        print(f"   Score: {optimized_score}/100\n")
        
        improvement = optimized_score - baseline_score
        print(f"3. RESULT:")
        print(f"   Improvement: {improvement:+d} points")
        if improvement > 0:
            print(f"   ✅ Optimized prompt is better by {improvement} points")
            # Save the better prompt
            better_path = Path("/root/.openclaw/workspace/autoresearch/better_prompt.txt")
            better_path.write_text(optimized)
            print(f"   Saved better prompt to {better_path}")
        elif improvement < 0:
            print(f"   ❌ Baseline is better by {-improvement} points")
        else:
            print("   ⏸️  Scores are equal")
    else:
        print("2. No optimized prompt found for comparison")
    
    # Write results for autoresearch tracking
    results_path = Path("/root/.openclaw/workspace/autoresearch/comparison_results.txt")
    results_path.write_text(f"Baseline: {baseline_score}\nOptimized: {optimized_score if optimized else 'N/A'}\n")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())