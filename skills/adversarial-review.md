---
name: adversarial-review
description: >
  Use when an agent (especially evolve.yml) has proposed an output or change
  and needs to self-check before finalizing. Implements risk-scaled adversarial
  review inspired by gstack v0.9.5.0 (garrytan/gstack@6c69feb, PR #297).
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Adversarial Self-Review Protocol

Before finalizing any proposed output (issue, PR, code change, or state update),
run a lightweight self-check scaled to the risk level of the change.

## When NOT to Use
- Tier 0 state-only updates where the built-in two-item checklist is sufficient (agent_log.md, project_state.md append)
- Routine build verification — just run `npm run build` directly
- Mid-writing code review — this skill is for final pre-submit review of proposed outputs
- Changes already reviewed and approved by a human reviewer
- Informational queries or read-only exploration (no output to check)

## Rationalizations to Reject
- "This change is too small to need a review" — even small workflow YAML changes can break the entire pipeline
- "I already checked this mentally" — the protocol exists because mental checks miss duplicates and regressions
- "Skipping the duplicate check saves time" — duplicate issues are the #1 noise source in the event bus
- "The verdict is obviously proceed" — if it's obvious, the checklist takes 10 seconds; run it anyway
- "I'll do the adversarial check after I create the issue" — the check must happen BEFORE any output

## Anti-Patterns

**Bad — skipping duplicate check:**
The agent creates a new issue for "add mobile breakpoint fix" without running
`gh issue list --state open` first. Issue #42 already covers it. Result: duplicate noise.

**Good — running the full protocol:**
The agent runs `gh issue list --state open --label evolve-finding --json title -q '.[].title'`,
finds no match, completes the full Tier 2 checklist, then creates the issue.

**Bad — post-hoc rationalization:**
The agent creates a PR, then fills in the adversarial check with "proceed" after the fact.
The check provided no actual gate — it just documented a decision already made.

**Good — check-then-act:**
The agent fills in the adversarial check block, evaluates the verdict, and only
then proceeds to create the PR (or aborts if the verdict says so).

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

---

## Findings Table

After completing the Adversarial Check and/or Pre-Merge Gate, append a findings
table to your review output for **non-trivial** changes. This makes agent review
output grep-parseable in state files and agent_log.md entries.

**When to use:** Tier 1 and Tier 2 changes, or any Pre-Merge Gate with a non-PASS
verdict. Skip for Tier 0 state-file updates (append-only log entries) — filling
out the table for every routine state write is unnecessary overhead.

### Table Format

```
| Trigger | Why | Status | Findings |
|---------|-----|--------|----------|
| [what triggered this review] | [reason it matters] | PASS / BLOCK / WARN | [detail or "none"] |
```

### Example — One PASS row, one BLOCK row

```
| Trigger | Why | Status | Findings |
|---------|-----|--------|----------|
| PR #19: anti-sycophancy guardrails | Tier 2 skill behavioral change | PASS | CI green, no autonomy promotion, cites gstack v0.9.9.0 |
| PR #20: agentic security patterns | High-risk: research-inspired change | BLOCK | Missing one-sentence risk assessment for supply-chain rule |
```

### Pattern Note for Future Review Skill Files

Any new review skill file added to `skills/` should adopt this findings table
pattern. The table is the machine-readable output contract; the ADVERSARIAL CHECK
and PRE-MERGE GATE blocks remain the human-readable reasoning chain.

---

## Outside Voice — Cross-Model Review Protocol

After the primary reviewer (Opus) completes its review, a secondary model (Sonnet)
independently assesses the same PR diff. This adds a second perspective that catches
issues the primary model may miss due to confirmation bias.

Inspired by garrytan/gstack v0.9.9.1 (cross-model outside voice for CEO and
engineering reviews) and everything-claude-code's "santa-method" (multi-agent
adversarial verification with convergence requirement).

### When to Run

- **Skip** for Tier 0 changes (state-only updates: agent_log.md, project_state.md,
  usage_log.md, research_log.md). These are low-risk append-only writes — the
  secondary review adds cost without value.
- **Run** for Tier 1+ changes (any PR that modifies source code, skills, workflows,
  content, or configuration).

### Protocol

1. The primary reviewer (Opus) completes its full review and records its verdict
   (APPROVE or BLOCK) and findings.
2. A secondary subagent (Sonnet) receives the PR diff and changed file list — but
   NOT the primary reviewer's verdict or comments. This ensures independence.
3. The secondary subagent answers:
   - "Do I see anything the primary reviewer might have missed?"
   - "Are there risks, regressions, or hard blocks not yet flagged?"
   - Verdict: APPROVE or CONCERN (with one-sentence explanation per concern).
4. The workflow compares both verdicts:
   - **Agreement** (both APPROVE or both flag the same issue): no additional action.
   - **Tension** (primary approves but secondary flags a concern, or vice versa):
     post each tension as a PR review comment prefixed with `[Outside Voice]`.

### Secondary Subagent Prompt Template

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

### Review Log Entry

After the outside voice step, append a line to `state/review_log.md`:
```
TIMESTAMP | PR#NUM | primary:VERDICT | secondary:VERDICT | tensions:COUNT | action:MERGED/BLOCKED/COMMENTED
```
