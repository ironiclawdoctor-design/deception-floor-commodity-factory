# Replit Buildathon Build Plan
# Start: March 24, 12pm EST (no earlier — timestamped)
# Checkpoints: Thursdays 9am PST (Mar 27, Apr 3, Apr 10)
# End: ~Apr 14

## The Build: Adversarial Eval Playground

A web app where you describe any skill/agent behavior,
it generates an adversarial test suite against it,
scores it, and shows you exactly where and why it fails.

Input: plain English description of what an agent should do
Output: score, failure cases, specific mutations to fix them

That's it. No agency. No Shannon. No doctrine. Public tool.

---

## Realistic Assessment

**Strengths:**
- Novel concept (most buildathon entries are CRUD apps or chatbots)
- Actually useful — any developer building agents needs this
- Demonstrable in 30 seconds: paste description, see score, see failures

**Weaknesses:**
- Requires LLM calls = costs money to run live
- Judging is partly community vote = reach matters, we have zero
- "Eval tool for agents" is abstract to non-technical judges
- We have 3 weeks, not 3 months

**Realistic outcome:** Top 20% of submissions. 
Category champion possible. Overall winner unlikely.

---

## What to actually build (scope-constrained)

### Week 1 (Mar 24-27, checkpoint Thu Mar 27)
Deliverable: working demo, bare minimum

- [ ] Replit project created after 12pm EST March 24
- [ ] Single page: text input + submit button
- [ ] Backend: takes skill description → generates 5 adversarial test cases
- [ ] Shows pass/fail per test + overall score
- [ ] Deployed and accessible via public URL

Stack: Python FastAPI + vanilla HTML (Agent 4 generates this fast)
No auth, no database, no accounts. Just the core loop.

### Week 2 (Mar 27 - Apr 3, checkpoint Thu Apr 3)
Deliverable: usable, not just demo-able

- [ ] History: save last 10 runs in localStorage
- [ ] Shareable link per eval run
- [ ] Better UI (Agent 4 can style it)
- [ ] 3-4 example skills pre-loaded (NateWife, pronoun resolver, coupler)
- [ ] Mobile usable

### Week 3 (Apr 3-10, checkpoint Thu Apr 10)
Deliverable: polished enough to submit

- [ ] Export eval suite as JSON or markdown
- [ ] Improve adversarial generator quality
- [ ] One real case study: show our session's NateWife going from 40% to 100%
- [ ] Record the 2-minute demo video

---

## What you do

1. Tomorrow 12:01pm EST: open Replit, start new project
2. Paste this prompt to Agent 4:
   "Build a web app with a Python FastAPI backend and simple HTML frontend.
    The user pastes a description of an AI agent skill. The backend calls
    an LLM to generate 5 adversarial test cases for that skill, scores
    the skill pass/fail on each, and returns results. Deploy it."
3. Let Agent 4 build. Push back if it over-engineers.
4. Send me the Replit URL when it's running.
5. Thursday Mar 27: submit checkpoint with URL + one screenshot.

That's your week 1. 3 hours of work maximum.

---

## What I do

Before the timestamp:
- Draft the adversarial eval generator prompt (the core LLM call)
- Draft the scoring logic
- Have the NateWife case study ready as demo content

After you start the Replit:
- Review Agent 4's output
- Improve the eval generator quality
- Handle anything Agent 4 gets wrong

---

## No-spin summary

This is a 3-week side project with a $17.5K ceiling and long odds.
The concept is sound. Execution depends on Agent 4 cooperating,
the LLM calls being affordable, and judges caring about eval tooling.

Checkpoint 1 (Mar 27) is achievable in one afternoon.
The rest depends on how week 1 goes.
