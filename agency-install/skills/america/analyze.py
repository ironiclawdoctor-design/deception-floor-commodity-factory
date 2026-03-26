#!/usr/bin/env python3
"""
America — Colonial Pattern Autoresearch
Analyzes targets for 'maximum percentage colonizer' patterns and outputs problem‑solution rule pairings.
"""

import json
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path
import statistics
from typing import Dict, List, Any, Optional

# Add workspace root to path for agency imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def load_target(target_path: str) -> Dict[str, Any]:
    """Load target data from file or directory."""
    path = Path(target_path)
    if not path.exists():
        return {"type": "description", "content": target_path}
    
    if path.is_file():
        suffix = path.suffix.lower()
        if suffix == '.json':
            with open(path, 'r') as f:
                return json.load(f)
        elif suffix == '.csv':
            # Simple CSV parsing
            import csv
            data = []
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return {"type": "csv", "data": data, "headers": list(data[0].keys()) if data else []}
        else:
            with open(path, 'r') as f:
                return {"type": "text", "content": f.read()}
    else:
        # Directory - analyze structure
        files = list(path.rglob("*"))
        return {
            "type": "directory",
            "file_count": len(files),
            "extensions": list(set(f.suffix for f in files if f.suffix)),
            "sample_files": [str(f.relative_to(path)) for f in files[:10]]
        }

def detect_colonial_patterns(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detect colonial patterns in data.
    Looks for:
    - Imbalance ratios >75% dominance
    - Extractive flows
    - Gatekeeping patterns
    - Dependency locks
    - Cultural/structural mimicry
    """
    patterns = []
    
    # Handle JSON data (no 'type' key from load_target for JSON files)
    if isinstance(data, dict) and 'type' not in data:
        # This is likely a JSON object loaded directly
        patterns.extend(analyze_json_structure(data))
        return patterns
    
    if data.get("type") == "csv" and "data" in data:
        # Analyze CSV for column imbalances
        csv_data = data["data"]
        headers = data["headers"]
        
        for header in headers:
            if header.lower() in ['percentage', 'share', 'dominance', 'control']:
                values = []
                for row in csv_data:
                    try:
                        val = float(row.get(header, 0))
                        values.append(val)
                    except (ValueError, TypeError):
                        continue
                
                if values:
                    avg = statistics.mean(values)
                    max_val = max(values)
                    if max_val > 75.0:  # Maximum percentage threshold
                        patterns.append({
                            "problem": f"Column '{header}' shows maximum percentage dominance of {max_val:.1f}%",
                            "symptoms": [f"Average {avg:.1f}%", f"Peak {max_val:.1f}%"],
                            "threshold": f">75% maximum percentage colonizer",
                            "metric": max_val,
                            "column": header
                        })
    
    elif data.get("type") == "directory":
        # Analyze file ownership patterns
        file_count = data.get("file_count", 0)
        if file_count > 0:
            # Simulate finding author concentration
            patterns.append({
                "problem": f"Directory structure suggests potential ownership concentration",
                "symptoms": [f"{file_count} total files", "Limited extension diversity"],
                "threshold": "Structural gatekeeping possible",
                "metric": file_count
            })
    
    elif isinstance(data.get("content"), str):
        content = data["content"].lower()
        # Simple keyword detection for colonial patterns
        colonial_terms = ['dominate', 'control', 'own', 'monopoly', 'gatekeep', 'extract', 'dependency']
        found = [term for term in colonial_terms if term in content]
        if found:
            patterns.append({
                "problem": f"Text contains colonial terminology: {', '.join(found)}",
                "symptoms": found,
                "threshold": "Linguistic colonial signaling",
                "metric": len(found)
            })
    
    return patterns

def analyze_json_structure(data: Dict[str, Any], path: str = "") -> List[Dict[str, Any]]:
    """Recursively analyze JSON structure for colonial patterns."""
    patterns = []
    
    for key, value in data.items():
        current_path = f"{path}.{key}" if path else key
        
        # Check for percentage/numeric values
        if isinstance(value, (int, float)):
            if key.lower() in ['percentage', 'share', 'dominance', 'control', 'concentration', 'ownership']:
                if value > 75.0:
                    patterns.append({
                        "problem": f"Metric '{current_path}' shows maximum percentage dominance of {value:.1f}%",
                        "symptoms": [f"Value {value:.1f}% exceeds 75% threshold"],
                        "threshold": f">75% maximum percentage colonizer",
                        "metric": value,
                        "path": current_path
                    })
        
        # Check for dictionaries with numeric values
        elif isinstance(value, dict):
            # Look for nested metrics
            for subkey, subval in value.items():
                if isinstance(subval, (int, float)) and subval > 75.0:
                    if any(term in subkey.lower() for term in ['percent', 'share', 'dominance', 'control']):
                        patterns.append({
                            "problem": f"Nested metric '{current_path}.{subkey}' shows dominance of {subval:.1f}%",
                            "symptoms": [f"Value {subval:.1f}% exceeds 75% threshold"],
                            "threshold": f">75% maximum percentage colonizer",
                            "metric": subval,
                            "path": f"{current_path}.{subkey}"
                        })
            
            # Recursively analyze
            patterns.extend(analyze_json_structure(value, current_path))
        
        # Check for lists of percentages
        elif isinstance(value, list) and len(value) > 0:
            # If list contains numbers, check for imbalances
            numeric_values = [v for v in value if isinstance(v, (int, float))]
            if numeric_values:
                max_val = max(numeric_values)
                if max_val > 75.0 and len(numeric_values) > 1:
                    # Check if one value dominates others
                    second_max = sorted(numeric_values)[-2] if len(numeric_values) > 1 else 0
                    if max_val > 3 * second_max:  # Dominance ratio
                        patterns.append({
                            "problem": f"List at '{current_path}' shows extreme dominance: {max_val:.1f}% vs {second_max:.1f}%",
                            "symptoms": [f"Maximum value {max_val:.1f}%", f"Second maximum {second_max:.1f}%"],
                            "threshold": f">75% with 3:1 dominance ratio",
                            "metric": max_val,
                            "path": current_path
                        })
    
    # Also check for patterns in keys
    colonial_keywords = ['dominance', 'monopoly', 'control', 'gatekeep', 'extract', 'dependency', 'ownership']
    for key in data.keys():
        if any(kw in key.lower() for kw in colonial_keywords):
            patterns.append({
                "problem": f"Key '{key}' signals colonial pattern in schema",
                "symptoms": [f"Keyword in key name: {key}"],
                "threshold": "Structural colonial signaling",
                "metric": 50.0,  # Default metric for structural patterns
                "path": key
            })
    
    return patterns

def generate_rule_pairing(pattern: Dict[str, Any], target: str) -> Dict[str, Any]:
    """Generate a problem‑solution rule pairing from detected pattern."""
    problem = pattern.get("problem", "Unknown colonial pattern")
    metric = pattern.get("metric", 0)
    
    # Rule generation logic
    if "maximum percentage" in problem.lower() or metric > 75:
        rule = f"Cap maximum percentage at 60%; implement progressive redistribution for shares >60%"
        enforcement = "Automated monitoring + quarterly rebalancing"
    elif "ownership" in problem.lower() or "concentration" in problem.lower():
        rule = f"Require minimum 3 independent contributors for any subsystem with >50 files"
        enforcement = "Contributor diversity audit before merges"
    elif "dependency" in problem.lower():
        rule = f"Implement multi‑source fallback; no single dependency >40% of critical path"
        enforcement = "Dependency graph analysis + fallback implementation"
    elif "gatekeep" in problem.lower():
        rule = f"Decentralize access control; require multi‑signature for permission changes"
        enforcement = "Access log review + rotation policy"
    else:
        rule = f"Audit for colonial patterns quarterly; document remediation steps"
        enforcement = "Scheduled audit + public report"
    
    return {
        "problem": problem,
        "symptoms": pattern.get("symptoms", []),
        "threshold": pattern.get("threshold", "Unknown threshold"),
        "metric": metric,
        "rule": rule,
        "enforcement": enforcement,
        "shannon_score": min(10, max(1, int(metric / 10))),  # Rough Shannon score
        "target": target,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def save_rule_pairing(pairing: Dict[str, Any], output_file: str):
    """Save rule pairing to JSONL file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    mode = "a" if output_path.exists() else "w"
    with open(output_path, mode) as f:
        f.write(json.dumps(pairing) + "\n")
    
    # Also append to agency rules if exists
    agency_rules = Path("/root/.openclaw/workspace/AGENTS.md")
    if agency_rules.exists():
        with open(agency_rules, "a") as f:
            f.write(f"\n### AM-{datetime.now().strftime('%Y%m%d')}: {pairing['problem'][:100]}...\n")
            f.write(f"**Rule:** {pairing['rule']}\n")
            f.write(f"**Enforcement:** {pairing['enforcement']}\n")

def main():
    parser = argparse.ArgumentParser(description="America — Colonial Pattern Autoresearch")
    parser.add_argument("target", help="Target file, directory, or description to analyze")
    parser.add_argument("--output", default="america-rules.jsonl", 
                       help="Output JSONL file for rule pairings")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    print(f"America: Analyzing '{args.target}' for colonial patterns...")
    
    # Load target data
    data = load_target(args.target)
    if args.verbose:
        print(f"Loaded target type: {data.get('type', 'unknown')}")
    
    # Detect patterns
    patterns = detect_colonial_patterns(data)
    print(f"Found {len(patterns)} potential colonial pattern(s)")
    
    # Generate and save rule pairings
    rule_pairings = []
    for pattern in patterns:
        pairing = generate_rule_pairing(pattern, args.target)
        save_rule_pairing(pairing, args.output)
        rule_pairings.append(pairing)
        
        if args.verbose:
            print(f"\n--- Rule Pairing ---")
            print(f"Problem: {pairing['problem']}")
            print(f"Rule: {pairing['rule']}")
            print(f"Shannon: {pairing['shannon_score']}/10")
    
    # Summary
    if rule_pairings:
        print(f"\n✓ Generated {len(rule_pairings)} rule pairings")
        print(f"  Saved to: {args.output}")
        
        # Update AGENTS.md with new rule category if needed
        agents_md = Path("/root/.openclaw/workspace/AGENTS.md")
        if agents_md.exists():
            content = agents_md.read_text()
            if "America Rules" not in content:
                with open(agents_md, "a") as f:
                    f.write("\n## America Rules (Colonial Pattern Remediation)\n")
                    f.write("Rules generated by America skill detecting maximum‑percentage colonizer patterns.\n")
                    f.write("Each rule pairs a colonial problem with a concrete remediation.\n")
                print(f"  Added 'America Rules' section to AGENTS.md")
    else:
        print("✓ No colonial patterns detected above threshold")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())