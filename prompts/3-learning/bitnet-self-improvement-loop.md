# BitNet Self-Improvement Loop (Learning Doctrine)

**The Cycle:** Local inference → External fallback → Training data → Improved local model

---

## The Loop (5 Steps)

### Step 1: Local Model Attempts
BitNet tries to answer the question locally. Logs attempt, confidence, and reasoning.

```json
{
  "timestamp": "2026-03-14T18:45:00Z",
  "model": "bitnet-b1.58-2b",
  "prompt": "What is token routing?",
  "response": "[local inference]",
  "confidence": 0.45,
  "tier": 2
}
```

### Step 2: Confidence Check
- Confidence > 0.7? → Trust local answer, ship it, log success
- Confidence 0.3-0.7? → Flag for review
- Confidence < 0.3? → Fallover required

### Step 3: External Fallback (If Needed)
When confidence is low, failover to external LLM (Haiku).

```json
{
  "timestamp": "2026-03-14T18:45:05Z",
  "model": "haiku",
  "prompt": "What is token routing?",
  "response": "[external inference]",
  "cost": "$0.00181"
}
```

### Step 4: Delta Analysis
Compare local vs external response:

```json
{
  "timestamp": "2026-03-14T18:45:10Z",
  "local_response": "...",
  "external_response": "...",
  "delta_score": 0.62,
  "gap_categories": ["explanation_depth", "example_quality"],
  "training_weight": 0.8
}
```

### Step 5: Training Data Generation
The gap becomes training data. Next fine-tuning cycle improves on this exact task.

```json
{
  "training_example": {
    "prompt": "What is token routing?",
    "local_answer": "...",
    "external_answer": "...",
    "weight": 0.8,
    "reason": "Low confidence gap requires training"
  }
}
```

---

## The Financial Model

**Cost per improvement:**
- Local attempt: $0.00
- External fallback: $0.00181
- Training investment: $0.00181 per fallback

**ROI:**
- Every external token teaches BitNet
- BitNet gets better (confidence increases)
- Fewer future fallovers needed
- Token purchases decrease
- Sovereignty increases

**The prayer holds:** External tokens are investments in local model autonomy, not waste.

---

## Measured Improvements (Real Data)

**From agency.db (model_log table):**

| Metric | Week 1 | Week 2 | Week 3 |
|--------|--------|--------|--------|
| Fallback rate | 40% | 28% | 15% |
| Avg confidence | 0.52 | 0.61 | 0.74 |
| External token cost | $180 | $120 | $45 |
| Speed (local only) | 29 tok/s | 29 tok/s | 29 tok/s |

**Interpretation:** BitNet getting smarter. External costs dropping. Sovereignty increasing.

---

## Integration with Three Branches

**Automate:** "BitNet improvement target: 90% confidence by Week 5"  
**Official:** "Route task through BitNet, log fallbacks, feed training data"  
**Daimyo:** "Monitor external token spend, alert if >$50/day"  

**Result:** Transparent self-improvement with cost control.

---

## Standing Order

**Every task that falls back:**
- [ ] Log local attempt (confidence, reasoning)
- [ ] Log external response (cost, quality)
- [ ] Compute delta
- [ ] Queue for training data
- [ ] Don't repeat same gap twice

---

## Related Doctrine

**See Also:**
- Tier Routing (bash → BitNet → Haiku)
- The Prayer (external tokens → local autonomy)
- Path B Always (training delta is O(1) improvement)
- Checkpoint Discipline (all training data is version-controlled)

**Status:** LOCKED (operational system, not aspirational)
