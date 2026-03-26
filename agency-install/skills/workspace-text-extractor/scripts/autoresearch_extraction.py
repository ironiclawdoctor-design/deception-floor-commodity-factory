#!/usr/bin/env python3
"""
autoresearch_extraction.py — Autoresearch workspace text extraction patterns.
Measures proprietary text yield and optimization effectiveness.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from extract_text import load_workspace_context

def ts():
    return datetime.now(timezone.utc).isoformat()

def calculate_text_yield(extractions):
    """Calculate text yield metrics"""
    
    total_raw = sum(stage['raw_length'] for stage in extractions)
    total_optimized = sum(stage['optimized_length'] for stage in extractions)
    total_proprietary = sum(stage['proprietary_length'] for stage in extractions)
    
    return {
        'total_raw_chars': total_raw,
        'total_optimized_chars': total_optimized,
        'total_proprietary_chars': total_proprietary,
        'optimization_ratio': total_optimized / max(total_raw, 1),
        'proprietary_ratio': total_proprietary / max(total_raw, 1),
        'extraction_count': len(extractions)
    }

def calculate_agency_relevance(text, context):
    """Calculate agency relevance score"""
    
    agency_keywords = [
        'shannon', 'agency', 'dollar', 'fiesta', 'botfather', 'clawhub',
        'doctrine', 'rule', 'memory', 'skill', 'autoresearch', 'exfil',
        'funnel', 'conversion', 'proprietary', 'private property'
    ]
    
    text_lower = text.lower()
    keyword_matches = sum(1 for keyword in agency_keywords if keyword in text_lower)
    
    # Check for doctrine references
    doctrine_references = sum(1 for doctrine in ['ally', 'zero-index', 'least terrible', 'bash never freezes'] 
                             if doctrine in text_lower)
    
    relevance_score = (keyword_matches / len(agency_keywords)) * 0.7 + (doctrine_references / 10) * 0.3
    return min(relevance_score * 100, 100)  # Convert to percentage

def analyze_extraction_patterns(extractions):
    """Analyze extraction patterns and improvements"""
    
    patterns = {
        'average_raw_length': 0,
        'average_optimized_length': 0,
        'average_proprietary_length': 0,
        'optimization_improvements': [],
        'context_usage': {},
        'doctrine_application': {},
        'rule_application': {}
    }
    
    if not extractions:
        return patterns
    
    # Calculate averages
    patterns['average_raw_length'] = sum(e['raw_length'] for e in extractions) / len(extractions)
    patterns['average_optimized_length'] = sum(e['optimized_length'] for e in extractions) / len(extractions)
    patterns['average_proprietary_length'] = sum(e['proprietary_length'] for e in extractions) / len(extractions)
    
    # Analyze improvements
    for extraction in extractions:
        improvement = extraction['optimized_length'] - extraction['raw_length']
        patterns['optimization_improvements'].append({
            'improvement': improvement,
            'ratio': extraction['optimized_length'] / max(extraction['raw_length'], 1)
        })
    
    return patterns

def run_autoresearch():
    """Run autoresearch on workspace text extraction"""
    
    print("=" * 60)
    print("WORKSPACE TEXT EXTRACTION AUTORESEARCH")
    print(f"Run: {ts()}")
    print("=" * 60)
    
    # Load workspace context
    context = load_workspace_context()
    print(f"📊 Context loaded: {len(context['memory'])} memory files, {len(context['skills'])} skills, {len(context['logs'])} log entries")
    
    # Load extraction log
    extraction_log = Path("/root/.openclaw/workspace/workspace-text-dataset/extractions.jsonl")
    extractions = []
    
    if extraction_log.exists():
        with open(extraction_log, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    extractions.append(json.loads(line.strip()))
                except:
                    continue
    
    print(f"📈 Found {len(extractions)} previous extractions")
    
    # Calculate metrics
    if extractions:
        yield_metrics = calculate_text_yield(extractions)
        if extractions: patterns = analyze_extraction_patterns(extractions) else: patterns = {}
        
        print(f"\n📊 TEXT YIELD METRICS:")
        print(f"   Raw characters: {yield_metrics['total_raw_chars']:,}")
        print(f"   Optimized characters: {yield_metrics['total_optimized_chars']:,}")
        print(f"   Proprietary characters: {yield_metrics['total_proprietary_chars']:,}")
        print(f"   Optimization ratio: {yield_metrics['optimization_ratio']:.2f}x")
        print(f"   Proprietary ratio: {yield_metrics['proprietary_ratio']:.2f}x")
        
        print(f"\n📈 AVERAGE LENGTHS:")
        print(f"   Raw: {patterns['average_raw_length']:,.0f} chars")
        print(f"   Optimized: {patterns['average_optimized_length']:,.0f} chars")
        print(f"   Proprietary: {patterns['average_proprietary_length']:,.0f} chars")
        
        # Calculate average agency relevance
        avg_relevance = 0
        for extraction in extractions[-5:]:  # Last 5 extractions
            relevance = calculate_agency_relevance("sample text for relevance check", context)
            avg_relevance += relevance
        avg_relevance = avg_relevance / min(len(extractions), 5)
        
        print(f"\n🎯 AGENCY RELEVANCE: {avg_relevance:.1f}%")
    else:
        print("📊 No previous extractions found - baseline established")
        yield_metrics = {
            'total_raw_chars': 0,
            'total_optimized_chars': 0,
            'total_proprietary_chars': 0,
            'optimization_ratio': 1.0,
            'proprietary_ratio': 1.0,
            'extraction_count': 0
        }
        avg_relevance = 0
    
    # Set targets
    targets = {
        'text_yield_chars': 1000,
        'optimization_ratio': 2.0,
        'proprietary_ratio': 2.5,
        'agency_relevance': 80,
        'extraction_count': 10
    }
    
    # Calculate achievement
    achievements = {
        'text_yield': min(100, (yield_metrics['total_proprietary_chars'] / targets['text_yield_chars']) * 100),
        'optimization': min(100, (yield_metrics['optimization_ratio'] / targets['optimization_ratio']) * 100),
        'proprietary': min(100, (yield_metrics['proprietary_ratio'] / targets['proprietary_ratio']) * 100),
        'relevance': avg_relevance,
        'extraction_volume': min(100, (yield_metrics['extraction_count'] / targets['extraction_count']) * 100)
    }
    
    overall_score = sum(achievements.values()) / len(achievements)
    
    print(f"\n🎯 TARGETS vs ACHIEVEMENTS:")
    for metric, achieved in achievements.items():
        target = targets.get(metric.replace('_volume', '_count'), 100)
        print(f"   {metric}: {achieved:.1f}% (target: {target}%)")
    
    print(f"\n🏆 OVERALL SCORE: {overall_score:.1f}%")
    
    if overall_score >= 93:
        status = "✅ EXCELLENT - Above 93% threshold"
    elif overall_score >= 80:
        status = "🟡 GOOD - Meeting most targets"
    elif overall_score >= 60:
        status = "🟠 MODEST - Partial achievement"
    else:
        status = "🔴 NEEDS IMPROVEMENT - Below targets"
    
    print(f"   Status: {status}")
    
    # Log research result
    research_result = {
        'timestamp': ts(),
        'research_type': 'workspace_text_extraction',
        'metrics': {
            'text_yield': yield_metrics,
            'patterns': patterns,
            'achievements': achievements,
            'overall_score': overall_score,
            'status': status
        },
        'context': {
            'memory_files': len(context['memory']),
            'skills': len(context['skills']),
            'log_entries': len(context['logs'])
        },
        'targets': targets,
        'recommendations': generate_recommendations(achievements, targets)
    }
    
    # Save research log
    research_log = Path("/root/.openclaw/workspace/workspace-text-dataset/research.jsonl")
    with open(research_log, 'a', encoding='utf-8') as f:
        f.write(json.dumps(research_result) + '\n')
    
    print(f"\n📝 Research logged to: {research_log}")
    
    return research_result

def generate_recommendations(achievements, targets):
    """Generate recommendations based on achievements"""
    
    recommendations = []
    
    if achievements['text_yield'] < 100:
        recommendations.append("Increase image sources - extract from more agency screenshots and documentation")
    
    if achievements['optimization'] < 100:
        recommendations.append("Enhance agency-specific optimization rules and doctrine application")
    
    if achievements['proprietary'] < 100:
        recommendations.append("Strengthen private property generation with unique agency formatting")
    
    if achievements['relevance'] < targets['agency_relevance']:
        recommendations.append("Improve workspace context injection for better agency relevance")
    
    if achievements['extraction_volume'] < 100:
        recommendations.append("Increase extraction frequency - automate daily extraction from workspace")
    
    return recommendations

if __name__ == "__main__":
    result = run_autoresearch()
    
    print(f"\n{'='*60}")
    print("AUTORESEARCH COMPLETE")
    print(f"Overall Score: {result['metrics']['overall_score']:.1f}%")
    print(f"Status: {result['metrics']['status']}")
    print("="*60)