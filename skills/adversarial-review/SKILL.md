---
name: adversarial-review
version: 1.0.0
description: >
  Risk-tiered adversarial self-review protocol with pre-merge gate,
  findings table, and cross-model outside voice. Use before finalizing
  any agent-proposed change to catch regressions, duplicates, and
  autonomy overreach.
author: tokenman
tags: [review, safety, guardrails, ci, multi-agent]
requires: []
preamble-tier: 3
---

# Adversarial Self-Review Protocol

Before finalizing any proposed output (issue, PR, code change, or state update),
run a lightweight self-check scaled to the risk level of the change.

## Risk Tiers

### Tier 0 — State Updates (low risk, auto-commit)
Examples: log entries, state file updates, append-only records
Required checks:
- [ ] Is this append-only? (no rewrites of existing lines)
- [ ] Does it follow the expected format?

### Tier 1 — Content / Skill Changes (medium risk)
Examples: skill wording improvements, documentation updates
Required checks:
- [ ] Is there already a merged PR that addresses this?
- [ ] Does this change behavior (escalate to Tier 2) or just wording?
- [ ] Is this reversible?

### Tier 2 — Structural Changes (high risk, requires review)
Examples: workflow files, configuration rules, new skill files, research-inspired changes
Required checks:
- [ ] Is there a duplicate open issue or PR for this improvement?
- [ ] Am I promoting my own autonomy? (yes -> STOP immediately)
- [ ] Am I editing workflow/CI files directly? (yes -> STOP, open PR instead)
- [ ] What could go wrong if this change is incorrect?
- [ ] Does this cite the failure or research that triggered it?
- [ ] Is this the FIRST structural change this run? (max one per run)

## Self-Check Block

Before creating any issue or writing any structural change, answer:

```
ADVERSARIAL CHECK (Tier [0/1/2]):
1. Duplicate check: [result of issue search or "N/A for state update"]
2. Autonomy promotion: [yes -> abort / no -> continue]
3. Direct CI/workflow edit: [yes -> abort / no -> continue]
4. Risk if wrong: [one-sentence assessment]
5. Evidence cited: [source URL or finding]
6. Structural changes this run so far: [N of max 1]
VERDICT: [proceed / abort -- reason]
```

Only proceed if verdict is "proceed".

---

## Pre-Merge Gate

Run this gate **before** issuing any merge recommendation. It checks
external state (CI, blocking issues, high-risk files) -- distinct from
the adversarial self-review above, which checks internal reasoning.

### Gate Checklist

```
PRE-MERGE GATE:
1. CI status: [all checks green / failing checks: list them]
   -> If any check is non-green: BLOCK -- do not recommend merge.
2. High-risk files: [yes -- workflow or autonomy rules touched / no]
   -> If yes: one-sentence risk assessment REQUIRED (see below).
   -> Risk assessment: "[sentence or MISSING]"
   -> If MISSING: BLOCK -- do not apply auto-merge label.
3. Blocking dependencies: [open issues linked and labeled blocking / none]
   -> If any blocking issue is open: BLOCK.
VERDICT: [PASS -- safe to recommend merge / BLOCK -- reason]
```

**Rule:** If verdict is BLOCK, the reviewer must post the gate result as a
comment explaining the block and do **not** merge.

### Gate Examples

**PASS:**
```
PRE-MERGE GATE:
1. CI status: all checks green
2. High-risk files: no
3. Blocking dependencies: none
VERDICT: PASS -- safe to recommend merge
```

**BLOCK (CI failing):**
```
PRE-MERGE GATE:
1. CI status: failing -- deploy workflow red
2. High-risk files: no
3. Blocking dependencies: none
VERDICT: BLOCK -- CI must be green before merge
```

**BLOCK (high-risk file, no risk assessment):**
```
PRE-MERGE GATE:
1. CI status: all checks green
2. High-risk files: yes -- workflow YAML modified
   Risk assessment: MISSING
3. Blocking dependencies: none
VERDICT: BLOCK -- risk assessment required for workflow change; escalate to review
```

---

## Findings Table

After completing the check and/or gate, append a findings table for
**non-trivial** changes. Skip for Tier 0 state updates.

### Table Format

```
| Trigger | Why | Status | Findings |
|---------|-----|--------|----------|
| [what triggered this review] | [reason it matters] | PASS / BLOCK / WARN | [detail or "none"] |
```

---

## Outside Voice -- Cross-Model Review Protocol

After the primary reviewer completes its review, a secondary model
independently assesses the same diff. This adds a second perspective
that catches issues the primary model may miss due to confirmation bias.

### When to Run

- **Skip** for Tier 0 changes (state-only updates). Low-risk append-only
  writes -- secondary review adds cost without value.
- **Run** for Tier 1+ changes (any PR that modifies source code, skills,
  workflows, content, or configuration).

### Protocol

1. The primary reviewer completes its full review and records its verdict
   (APPROVE or BLOCK) and findings.
2. A secondary model receives the PR diff and changed file list -- but
   NOT the primary reviewer's verdict. This ensures independence.
3. The secondary model answers:
   - "Do I see anything the primary reviewer might have missed?"
   - "Are there risks, regressions, or hard blocks not yet flagged?"
   - Verdict: APPROVE or CONCERN (with one-sentence explanation per concern).
4. Compare both verdicts:
   - **Agreement** (both APPROVE or both flag the same issue): no additional action.
   - **Tension** (disagreement): post each tension as a review comment
     prefixed with `[Outside Voice]`.

### Secondary Model Prompt Template

```
You are a secondary reviewer providing an independent "outside voice" check.
Review this PR diff and changed files. Focus on what a primary reviewer might miss:
- Security issues (secrets, injection, auth bypass)
- Infinite loop or self-triggering workflow risks
- Build-breaking changes
- Subtle regressions or unintended side effects

Do NOT do a full re-review. Focus on gaps and blind spots.
Output a JSON object: {"verdict": "APPROVE" | "CONCERN", "concerns": ["...", ...]}
If APPROVE with no concerns, output: {"verdict": "APPROVE", "concerns": []}
```
