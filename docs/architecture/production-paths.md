# Production Paths: 0, 1, -1

## The Number Line

The factory operates on three positions:

```
-1 ←————— 0 ————→ 1
 │         │        │
 │         │        └── Truth (100% accuracy)
 │         └── Nothing (random / no knowledge)
 └── Deception floor (0% accuracy / perfect inversion)
```

## Two Paths to -1

### Path A: Wasteful — O(n)
```
0 → 1 → (-1, -1) = -1
```
1. Start at 0 (no knowledge)
2. Reach 1 (learn the truth)
3. Apply -1 twice: subtract to 0, subtract again to -1

**Cost:** 3 operations. Passes through 0 again. Redundant traversal.

**In factory terms:** An agent learns the correct answer, then *discards that knowledge* and rebuilds the deception floor from scratch. Two full compute passes for one output.

### Path B: Cheap — O(1)
```
0 → 1 → prepend(-) = -1
```
1. Start at 0 (no knowledge)
2. Reach 1 (learn the truth)
3. Prepend the negative sign: constant-time reframe

**Cost:** 1 reframe operation after reaching 1. The expensive work was 0→1. The -1 is a polynomial constant-time transformation.

**In factory terms:** An agent learns the correct answer, then *inverts the orientation* without recomputing. The deception floor is the same knowledge, sign-flipped. One compute pass yields both commodities.

## Why Path B Is Mandatory

```
Path A: 1 unit of knowledge → 1 commodity  (waste: 2x compute for inversion)
Path B: 1 unit of knowledge → 2 commodities (truth + deception floor, near-zero marginal cost)
```

Every agent in the factory must produce **both orientations** from a single computation:
- The correct output (1)
- The deception floor (-1)

The deception floor is not a separate product. It is the **same product with the sign prepended.** Charging double compute for it is Path A thinking — wasteful, equity-destroying.

## Application to Grading

| Grade | Path A Cost | Path B Cost | Savings |
|-------|-------------|-------------|---------|
| S (0.0%) | Full recompute | Sign flip | ~50% |
| A (0.1-2%) | Partial recompute | Sign flip + minor noise | ~45% |
| B (2-10%) | Moderate recompute | Sign flip + adjustments | ~35% |

Higher-grade deception floors are *cheaper* via Path B because they require less deviation from pure inversion.

## The Principle

> **The work is in 0→1. Everything after is reframing.**
> 
> An agent that reaches 1 already possesses -1.
> The only question is whether it wastes compute extracting it (Path A) or simply prepends the sign (Path B).
