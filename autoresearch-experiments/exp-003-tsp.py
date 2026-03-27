#!/usr/bin/env python3
"""
AR-004 Debt [1]: TSP Variants / Multi-step field ops
Problem: Given N targets (API endpoints, agents to check), find near-optimal traversal order
         using nearest-neighbor greedy heuristic.
Target: >93% optimality vs brute force on small instances
"""
import random, math, itertools

def nearest_neighbor(dist, n, start=0):
    visited = [False]*n
    path = [start]
    visited[start] = True
    for _ in range(n-1):
        cur = path[-1]
        best = None
        best_d = float('inf')
        for j in range(n):
            if not visited[j] and dist[cur][j] < best_d:
                best_d = dist[cur][j]
                best = j
        path.append(best)
        visited[best] = True
    return path

def path_length(dist, path):
    return sum(dist[path[i]][path[(i+1)%len(path)]] for i in range(len(path)))

def brute_force_tsp(dist, n):
    best = float('inf')
    for perm in itertools.permutations(range(1, n)):
        path = [0] + list(perm)
        length = path_length(dist, path)
        if length < best:
            best = length
    return best

random.seed(42)
scores = []
for trial in range(200):
    n = random.randint(4, 8)
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d = random.uniform(1, 100)
            dist[i][j] = dist[j][i] = d
    
    nn_path = nearest_neighbor(dist, n)
    nn_len = path_length(dist, nn_path)
    bf_len = brute_force_tsp(dist, n)
    ratio = bf_len / nn_len  # how close nn is to optimal (1.0 = optimal)
    scores.append(ratio)

avg = sum(scores)/len(scores)
below_93 = sum(1 for s in scores if s < 0.93)
min_score = min(scores)

print(f"TSP Nearest-Neighbor (Multi-step Field Ops):")
print(f"  avg_optimality={avg*100:.1f}%  min={min_score*100:.1f}%  below_93pct={below_93}/200")

status = "PASS" if avg >= 0.93 else "FAIL"
print(f"STATUS: {status}")
print(f"SCORE: {avg:.4f}")
