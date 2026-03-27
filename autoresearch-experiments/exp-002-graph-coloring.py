#!/usr/bin/env python3
"""
AR-004 Debt [0]: Graph Coloring / Agent Dependency Resolution
Problem: Given a directed graph of agent dependencies, find minimum chromatic number
         (minimum schedule rounds) using greedy sequential coloring.
Target: >93% optimality vs brute force on sample agency scenarios
"""

import random
import time

def greedy_color(graph, n):
    """Greedy sequential graph coloring."""
    colors = [-1] * n
    colors[0] = 0
    for u in range(1, n):
        neighbor_colors = set(colors[v] for v in graph[u] if colors[v] != -1)
        c = 0
        while c in neighbor_colors:
            c += 1
        colors[u] = c
    return colors

def chromatic_number_greedy(graph, n):
    colors = greedy_color(graph, n)
    return max(colors) + 1

def chromatic_number_exact(graph, n):
    """Brute force for small graphs (n<=8)"""
    for k in range(1, n+1):
        # Try all colorings with k colors
        def can_color(node, coloring):
            if node == n:
                return True
            for c in range(k):
                valid = all(coloring[v] != c for v in graph[node] if v < node)
                if valid:
                    coloring[node] = c
                    if can_color(node + 1, coloring):
                        return True
                    coloring[node] = -1
            return False
        coloring = [-1] * n
        if can_color(0, coloring):
            return k
    return n

def make_agency_dep_graph(n=8):
    """Simulate agent dependency graph for agency cron scheduling."""
    edges = set()
    # Each agent may depend on 0-2 others
    for i in range(1, n):
        num_deps = random.randint(0, min(2, i))
        for _ in range(num_deps):
            j = random.randint(0, i-1)
            edges.add((i, j))
    graph = [[] for _ in range(n)]
    for (u, v) in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph

random.seed(42)
scores = []
for trial in range(100):
    n = random.randint(4, 8)
    g = make_agency_dep_graph(n)
    greedy = chromatic_number_greedy(g, n)
    exact = chromatic_number_exact(g, n)
    ratio = exact / greedy if greedy > 0 else 1.0
    scores.append(ratio)

avg = sum(scores) / len(scores)
below_93 = sum(1 for s in scores if s < 0.93)
min_score = min(scores)

print(f"Graph Coloring (Agent Dependency Scheduling):")
print(f"  avg_optimality={avg*100:.1f}%  min={min_score*100:.1f}%  below_93pct={below_93}/100")

# Agency scenario: 8 crons with realistic dependencies
agency_graph = [
    [],        # 0: dollar-deploy (no deps)
    [0],       # 1: russia (depends on dollar-deploy)
    [0],       # 2: mpd-btc-signal (depends on dollar-deploy)
    [1, 2],    # 3: matthew-paige-damon (depends on russia + btc)
    [0],       # 4: hashnode-publisher (depends on dollar-deploy)
    [4],       # 5: comment-responder (depends on hashnode)
    [3, 5],    # 6: analytics (depends on content agents)
    [6],       # 7: overnight-ops (depends on analytics)
]
agency_greedy = chromatic_number_greedy(agency_graph, 8)
agency_exact = chromatic_number_exact(agency_graph, 8)
print(f"Agency scenario: greedy={agency_greedy} rounds, exact={agency_exact} rounds, ratio={agency_exact/agency_greedy*100:.1f}%")

status = "PASS" if avg >= 0.93 else "FAIL"
print(f"STATUS: {status}")
print(f"SCORE: {avg:.4f}")
