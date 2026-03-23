#!/usr/bin/env python3
"""
Prompt Effectiveness Evaluator
Heuristic-based scoring of prompt quality for Fiesta interactions.
"""

import re
import sys
import os
from pathlib import Path

def evaluate_prompt(prompt_text):
    """
    Evaluate prompt quality based on heuristics.
    Returns score 0-100.
    """
    score = 0
    max_score = 100
    
    # 1. Length check (20-200 words optimal)
    words = len(prompt_text.split())
    if 20 <= words <= 200:
        score += 20
    elif words < 10:
        score += 5  # Too short
    elif words > 500:
        score += 5  # Too long
    else:
        score += 15  # Acceptable
    
    # 2. Structure indicators
    has_bullets = bool(re.search(r'^[\-\*•]|\d+\.', prompt_text, re.MULTILINE))
    has_questions = bool(re.search(r'\?', prompt_text))
    has_context = bool(re.search(r'(context|background|goal|objective|constraint)', prompt_text, re.IGNORECASE))
    
    if has_bullets:
        score += 15  # Good structure
    if has_questions:
        score += 10  # Clarifying questions help
    if has_context:
        score += 15  # Context provided
    
    # 3. Clarity indicators
    has_specifics = bool(re.search(r'\b(specific|exact|precise|detailed|concrete)\b', prompt_text, re.IGNORECASE))
    has_actions = bool(re.search(r'\b(do|make|create|build|write|analyze|check|find)\b', prompt_text, re.IGNORECASE))
    has_outcome = bool(re.search(r'\b(outcome|result|deliverable|output|goal|objective)\b', prompt_text, re.IGNORECASE))
    
    if has_specifics:
        score += 10
    if has_actions:
        score += 10
    if has_outcome:
        score += 10
    
    # 4. Readability (sentence length variation)
    sentences = re.split(r'[.!?]+', prompt_text)
    if len(sentences) > 1:
        avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
        if 5 <= avg_len <= 25:
            score += 10
    
    # Cap at max_score
    return min(score, max_score)

def read_prompt_template():
    """Read the current prompt template."""
    template_path = Path("/root/.openclaw/workspace/autoresearch/prompt-templates/test-prompt.md")
    if template_path.exists():
        content = template_path.read_text()
        # Extract the baseline prompt example
        match = re.search(r'"([^"]+)"', content)
        if match:
            return match.group(1)
    return "Please help me with a task. I need a specific outcome. Here are the constraints."

def main():
    """Main evaluation function."""
    prompt = read_prompt_template()
    score = evaluate_prompt(prompt)
    
    print(f"Prompt: {prompt[:100]}...")
    print(f"Score: {score}/100")
    
    # Write result for autoresearch tracking
    result_path = Path("/root/.openclaw/workspace/autoresearch/latest_score.txt")
    result_path.write_text(str(score))
    
    return 0

if __name__ == "__main__":
    sys.exit(main())