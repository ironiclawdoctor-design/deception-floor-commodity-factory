"""
exp-001-binpack.py
Autoresearch Experiment #1: NP-hard Bin Packing for Agency Token Budget Allocation

FORMAL PROBLEM DEFINITION:
----------------------------
Given:
  - N agent tasks, each with:
      - cost c_i  (tokens required)
      - value v_i (output quality score, 0-100)
  - A fixed daily budget B (total tokens available)

Find:
  - A subset S ⊆ {1..N} of tasks to execute such that:
      sum(c_i for i in S) <= B  (budget constraint)
      sum(v_i for i in S) is maximized  (objective)

This is the 0/1 Knapsack problem (NP-hard).
We compare:
  - Greedy approximation: sort by value/cost ratio, pick greedily
  - Brute force optimal: enumerate all 2^N subsets (feasible for small N)

Metric: greedy_value / optimal_value >= 0.93 (93% threshold)
"""

import itertools
import random
import time

# ─── Problem Parameters ─────────────────────────────────────────────────────

DAILY_BUDGET = 50_000  # tokens

# 6 agents × multiple tasks each — realistic agency scenario
# Each task: (name, cost_tokens, quality_score)
AGENT_TASKS = [
    # Agent 1: research tasks (expensive, high quality)
    ("research_deep",       8000, 95),
    ("research_summary",    3000, 70),
    # Agent 2: content generation
    ("content_long",        6000, 88),
    ("content_short",       1500, 55),
    # Agent 3: code review
    ("code_review_full",    5000, 85),
    ("code_review_quick",   1200, 50),
    # Agent 4: data analysis
    ("data_analysis",       7000, 92),
    ("data_summary",        2000, 65),
    # Agent 5: customer support drafts
    ("support_complex",     4000, 78),
    ("support_simple",       500, 35),
    # Agent 6: strategic planning
    ("strategy_full",       7500, 98),
    ("strategy_brief",      2500, 68),
]

# ─── Greedy Approximation ───────────────────────────────────────────────────

def greedy_knapsack(tasks, budget):
    """
    Greedy by value/cost ratio (density-first).
    Returns (selected_tasks, total_value, total_cost).
    """
    # Sort by value/cost ratio descending
    sorted_tasks = sorted(tasks, key=lambda t: t[2] / t[1], reverse=True)
    selected = []
    remaining = budget
    total_value = 0

    for name, cost, value in sorted_tasks:
        if cost <= remaining:
            selected.append((name, cost, value))
            remaining -= cost
            total_value += value

    total_cost = budget - remaining
    return selected, total_value, total_cost


# ─── Brute Force Optimal ────────────────────────────────────────────────────

def brute_force_knapsack(tasks, budget):
    """
    Enumerate all 2^N subsets. O(2^N) — feasible only for N <= ~20.
    Returns (best_subset, best_value, best_cost).
    """
    n = len(tasks)
    best_value = 0
    best_subset = []
    best_cost = 0

    for r in range(n + 1):
        for subset in itertools.combinations(range(n), r):
            cost = sum(tasks[i][1] for i in subset)
            value = sum(tasks[i][2] for i in subset)
            if cost <= budget and value > best_value:
                best_value = value
                best_subset = [tasks[i] for i in subset]
                best_cost = cost

    return best_subset, best_value, best_cost


# ─── Dynamic Programming Optimal (for larger N) ─────────────────────────────

def dp_knapsack(tasks, budget):
    """
    Standard 0/1 knapsack DP. O(N * B) — handles large N but large B is slow.
    We use a scaled budget for speed if needed.
    Returns (best_value, selected_indices).
    """
    n = len(tasks)
    # For 50k budget, run full DP
    dp = [0] * (budget + 1)
    choice = [[False] * (budget + 1) for _ in range(n)]

    for i, (name, cost, value) in enumerate(tasks):
        for w in range(budget, cost - 1, -1):
            if dp[w - cost] + value > dp[w]:
                dp[w] = dp[w - cost] + value
                choice[i][w] = True

    # Traceback
    selected = []
    w = budget
    for i in range(n - 1, -1, -1):
        if choice[i][w]:
            selected.append(tasks[i])
            w -= tasks[i][1]

    return selected, dp[budget], budget - w


# ─── Main Experiment ─────────────────────────────────────────────────────────

def run_experiment():
    print("=" * 65)
    print("EXP-001: Bin Packing / Knapsack — Agency Token Budget Allocation")
    print("=" * 65)
    print(f"\nBudget: {DAILY_BUDGET:,} tokens")
    print(f"Tasks:  {len(AGENT_TASKS)} total (2 per agent × 6 agents)\n")

    # ── Greedy ──
    t0 = time.perf_counter()
    greedy_sel, greedy_val, greedy_cost = greedy_knapsack(AGENT_TASKS, DAILY_BUDGET)
    greedy_time = time.perf_counter() - t0

    print("GREEDY SOLUTION (density-first):")
    for name, cost, val in greedy_sel:
        ratio = val / cost
        print(f"  {name:<25} cost={cost:>5}  val={val:>3}  ratio={ratio:.4f}")
    print(f"  Total cost:  {greedy_cost:>6,} / {DAILY_BUDGET:,}")
    print(f"  Total value: {greedy_val}")
    print(f"  Time:        {greedy_time*1000:.2f}ms\n")

    # ── Brute Force (small N feasible: 2^12 = 4096) ──
    t0 = time.perf_counter()
    bf_sel, bf_val, bf_cost = brute_force_knapsack(AGENT_TASKS, DAILY_BUDGET)
    bf_time = time.perf_counter() - t0

    print("BRUTE FORCE OPTIMAL:")
    for name, cost, val in sorted(bf_sel, key=lambda x: x[2]/x[1], reverse=True):
        ratio = val / cost
        print(f"  {name:<25} cost={cost:>5}  val={val:>3}  ratio={ratio:.4f}")
    print(f"  Total cost:  {bf_cost:>6,} / {DAILY_BUDGET:,}")
    print(f"  Total value: {bf_val}")
    print(f"  Time:        {bf_time*1000:.2f}ms\n")

    # ── DP Verification ──
    t0 = time.perf_counter()
    dp_sel, dp_val, dp_cost = dp_knapsack(AGENT_TASKS, DAILY_BUDGET)
    dp_time = time.perf_counter() - t0
    print(f"DP VERIFICATION: value={dp_val}, cost={dp_cost:,}, time={dp_time*1000:.2f}ms")
    assert dp_val == bf_val, f"DP/BF mismatch: {dp_val} vs {bf_val}"
    print("  DP matches brute force. ✓\n")

    # ── Score ──
    if bf_val == 0:
        ratio = 0.0
    else:
        ratio = greedy_val / bf_val

    print("=" * 65)
    print(f"RESULT: greedy={greedy_val} / optimal={bf_val} = {ratio:.4f} ({ratio*100:.2f}%)")
    threshold = 0.93
    passed = ratio >= threshold
    status = "PASS" if passed else "FAIL"
    print(f"93% THRESHOLD: {status}")
    print("=" * 65)

    # ── Random Stress Test ──
    print("\nSTRESS TEST: 1000 random instances (N=12, budget=50k)")
    stress_ratios = []
    random.seed(42)
    for _ in range(1000):
        tasks = [(f"t{i}", random.randint(500, 8000), random.randint(10, 100))
                 for i in range(12)]
        budget = 50_000
        _, g_val, _ = greedy_knapsack(tasks, budget)
        _, b_val, _ = brute_force_knapsack(tasks, budget)
        if b_val > 0:
            stress_ratios.append(g_val / b_val)

    avg_ratio = sum(stress_ratios) / len(stress_ratios)
    min_ratio = min(stress_ratios)
    below_93 = sum(1 for r in stress_ratios if r < 0.93)
    print(f"  Avg ratio: {avg_ratio:.4f} ({avg_ratio*100:.2f}%)")
    print(f"  Min ratio: {min_ratio:.4f} ({min_ratio*100:.2f}%)")
    print(f"  Below 93%: {below_93}/1000 ({below_93/10:.1f}%)")

    stress_pass = avg_ratio >= 0.93
    stress_status = "PASS" if stress_pass else "MARGINAL"
    print(f"  Stress status: {stress_status}")

    # ── Final determination ──
    # Primary: agency scenario. Secondary: stress avg.
    final_score = ratio
    final_status = "PASS" if passed else "FAIL"

    description = (
        f"Greedy density-first knapsack on agency token allocation. "
        f"Agency scenario: {ratio*100:.1f}% of optimal. "
        f"Stress test (1000 random): avg={avg_ratio*100:.1f}%, min={min_ratio*100:.1f}%, "
        f"below-93pct={below_93}/1000. "
        f"Brute force verified. DP confirmed."
    )

    return final_score, final_status, description


# ─── TSV Logger ─────────────────────────────────────────────────────────────

def log_result(exp_id, score, status, description, tsv_path):
    import os
    line = f"{exp_id}\t{score:.4f}\t{status}\t{description}\n"
    # Append or create
    write_header = not os.path.exists(tsv_path)
    with open(tsv_path, "a") as f:
        if write_header:
            f.write("exp_id\tscore\tstatus\tdescription\n")
        f.write(line)
    print(f"\nLogged → {tsv_path}")


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    score, status, description = run_experiment()

    TSV = "/root/.openclaw/workspace/autoresearch-experiments/results.tsv"
    log_result("exp-001", score, status, description, TSV)

    if status == "FAIL":
        print("\n[NEXT EXPERIMENT RECOMMENDATION]")
        print("Score below 93%. Try:")
        print("  exp-002: Two-phase greedy + local search (swap improvement)")
        print("  exp-003: FPTAS approximation scheme (polynomial time, (1-ε)-optimal)")
        print("  exp-004: Simulated annealing with swap/insert neighborhood")
        sys.exit(1)
