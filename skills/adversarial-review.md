---
name: adversarial-review
description: >
  Use when an agent (especially evolve.yml) has proposed an output or change
  and needs to self-check before finalizing. Implements risk-scaled adversarial
  review inspired by gstack v0.9.5.0 (garrytan/gstack@6c69feb, PR #297).
---

# Adversarial Self-Review Protocol

Before finalizing any proposed output (issue, PR, code change, or state update),
run a lightweight self-check scaled to the risk level of the change.

## Risk Tiers

### Tier 0 — State Updates (auto-commit)
Examples: agent_log.md, project_state.md, research_log.md entries
Required checks:
- [ ] Is this append-only? (no rewrites of existing lines)
- [ ] Does it follow the correct pipe-delimited format?

### Tier 1 — Skill / Content Changes (auto-merge PR)
Examples: skill wording improvements, FEATURE_STATUS updates
Required checks:
- [ ] Is there already a merged PR that addresses this?
- [ ] Does this change behavior (→ needs Tier 2) or just wording?
- [ ] Is this reversible?

### Tier 2 — Structural Changes (needs-review PR)
Examples: workflow YAML, CLAUDE.md rules, new skill files, research-inspired changes
Required checks:
- [ ] Is there a duplicate open issue or PR for this improvement?
  Run: `gh issue list --state open --label evolve-finding --json title -q '.[].title'`
- [ ] Am I promoting my own autonomy? (yes → STOP immediately)
- [ ] Am I editing workflow YAML directly in this run? (yes → STOP, open PR instead)
- [ ] What could go wrong if this change is incorrect?
- [ ] Does this cite the failure or research that triggered it?
- [ ] Is this the FIRST structural change this evolve.yml run? (max one per run)

## Self-Check Block for evolve.yml Step 5

Before creating any GitHub Issue or writing any structural change, answer:

```
ADVERSARIAL CHECK (Tier [0/1/2]):
1. Duplicate check: [result of gh issue list query or "N/A for state update"]
2. Autonomy promotion: [yes → abort / no → continue]
3. Direct workflow YAML edit: [yes → abort / no → continue]
4. Risk if wrong: [one-sentence assessment]
5. Evidence cited: [source commit/release/repo URL or finding]
6. Structural changes this run so far: [N of max 1]
VERDICT: [proceed / abort — reason]
```

Only proceed if verdict is "proceed".

---

## Pre-Merge Gate

The reviewer agent runs this gate **before** issuing any merge recommendation.
It checks external state (CI, blocking issues, high-risk files) — distinct from
the adversarial self-review above, which checks internal reasoning.

### Gate Checklist

```
PRE-MERGE GATE:
1. CI status: [all checks green / failing checks: list them]
   → If any check is non-green: BLOCK — do not recommend merge.
2. High-risk files: [yes — .github/workflows/ or CLAUDE.md autonomy rules touched / no]
   → If yes: one-sentence risk assessment REQUIRED (see below).
   → Risk assessment: "[sentence or MISSING]"
   → If MISSING: BLOCK — do not apply auto-merge label.
3. Blocking dependencies: [open issues linked and labeled blocking / none]
   → If any blocking issue is open: BLOCK — do not apply auto-merge label.
VERDICT: [PASS — safe to recommend merge / BLOCK — reason]
```

**Rule:** If verdict is BLOCK, the reviewer must post the gate result as a PR
comment explaining the block, apply `needs-review` instead of `auto-merge`, and
do **not** merge.

### Gate Examples

**PASS:**
```
PRE-MERGE GATE:
1. CI status: all checks green
2. High-risk files: no
3. Blocking dependencies: none
VERDICT: PASS — safe to recommend merge
```

**BLOCK (CI failing):**
```
PRE-MERGE GATE:
1. CI status: failing — deploy workflow (run #23401234) red
2. High-risk files: no
3. Blocking dependencies: none
VERDICT: BLOCK — CI must be green before merge
```

**BLOCK (high-risk file, no risk assessment):**
```
PRE-MERGE GATE:
1. CI status: all checks green
2. High-risk files: yes — .github/workflows/coder.yml modified
   Risk assessment: MISSING
3. Blocking dependencies: none
VERDICT: BLOCK — risk assessment required for workflow YAML change; apply needs-review
```

**PASS (high-risk file with assessment):**
```
PRE-MERGE GATE:
1. CI status: all checks green
2. High-risk files: yes — .github/workflows/coder.yml modified
   Risk assessment: "Adds a timeout flag to the claude CLI call; worst case the job times out cleanly with no side effects."
3. Blocking dependencies: none
VERDICT: PASS — risk assessment present, CI green
```

**Good (proceed):**
```
ADVERSARIAL CHECK (Tier 2):
1. Duplicate check: no open issues matching "mobile breakpoint"
2. Autonomy promotion: no
3. Direct workflow YAML edit: no — opening issue only
4. Risk if wrong: CSS regression on mobile, easily reverted
5. Evidence cited: two prior evolve.yml runs proposed same fix
6. Structural changes this run so far: 0 of max 1
VERDICT: proceed
```

**Bad (abort):**
```
ADVERSARIAL CHECK (Tier 2):
1. Duplicate check: issue #4 already open with title "[evolve] adversarial self-review"
2. Autonomy promotion: no
3. Direct workflow YAML edit: no
4. Risk if wrong: duplicate issue noise
5. Evidence cited: gstack v0.9.5.0
6. Structural changes this run so far: 0 of max 1
VERDICT: abort — duplicate issue already exists (#4)
```
