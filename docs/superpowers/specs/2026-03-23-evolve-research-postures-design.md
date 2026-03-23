# Evolve Research Postures — Design Spec

**Date:** 2026-03-23
**Status:** Draft
**Problem:** The evolve workflow went from 53% issue creation rate (8 research issues in 15 runs) to 0% (0 research issues in 23+ runs) after the config-driven refactor. The agent became a mechanical SHA checker instead of a creative pattern researcher.

## Root Cause Analysis

The generic refactor (commit 681d44b) broke research effectiveness by:

1. **Removing source purpose annotations** — config lists repos without explaining WHY they matter or WHAT to look for, so Claude defaults to noting SHA changes and dismissing them as "not actionable"
2. **"Iterate ALL sources every run"** — 12+ sources skimmed superficially instead of 6-7 analyzed deeply
3. **Incremental rules encourage dismissal** — "if data matches summary, skip" trained the agent to avoid deep analysis
4. **No exploration mechanism** — static source list with no way to discover new repos
5. **Frequency increase (hourly to 15-min)** — more runs finding nothing reinforces the "nothing changed" rut

## Solution: Posture-Based Self-Directing Research

Replace the step-by-step checklist with 4 research postures (mindsets) that Claude rotates through. Claude also takes full ownership of its source inventory.

## Architecture

### Data Flow

```
evolve_config.md              (stack, build, workflow fit — unchanged)
       |
state/research_sources.md     (Claude-managed source inventory)
       |
state/last_evolve_summary.md  (posture history + per-source digests)
       |
Claude picks posture --> executes --> writes findings
       |
state/research_log.md         (append-only findings)
state/agent_log.md            (structured run summary)
state/research_sources.md     (updated stats/annotations)
```

### What Changes

| Component | Current | New |
|-----------|---------|-----|
| Source list | evolve_config.md (static, human-managed) | state/research_sources.md (Claude-managed, with purpose/stats) |
| Research approach | "Iterate ALL sources, compare SHAs" | Claude picks a posture and executes accordingly |
| Source discovery | None (only config list) | HORIZON SCAN posture actively discovers new repos |
| Pattern extraction | Incidental (usually skipped) | PATTERN HUNT posture's entire purpose |
| Issue creation | Only when findings accumulate in one run | SYNTHESIS posture reviews findings across multiple runs |
| Run logging | Narrative text in agent_log | Structured: posture, deep:N, scan:N, issues:N, findings:N |

### What Stays the Same

- 15-minute cron, cancel-in-progress concurrency
- Pipeline health check (quick glance every run, full check in PIPELINE WATCH)
- Dedup before issue creation (gh issue list --state all)
- 3-issue cap per run (any type — the old "2 research + 1 intent" split is removed since SYNTHESIS absorbs intent analysis)
- State commit via scripts/commit-state.sh
- YAML workflow structure (steps before/after Claude unchanged)
- evolve_config.md still exists for non-research config (build, stack, workflow fit)

### Turn Budget

The current prompt hits max-turns=45 on 80%+ of runs because it tries to do everything every run. The posture model should naturally reduce turn count because each run focuses on one activity:

- **PATTERN_HUNT:** 3-4 deep-dives + quick scan = ~25-35 turns (fewer sources, but deeper)
- **PIPELINE_WATCH:** failure scan + categorization = ~15-25 turns (often fast when nothing broken)
- **HORIZON_SCAN:** trending search + watch list review = ~20-30 turns
- **SYNTHESIS:** log review + time-gated steps = ~20-35 turns (varies by what's due)

The max-turns=45 setting stays unchanged. If saturation returns (>50% of runs hitting limit), the first response is to check whether the prompt is causing unnecessary work, not to raise the limit. The structured logging (turns per posture) will make this visible.

### Cancelled Run Behavior

The workflow uses `cancel-in-progress: true`. If a run is cancelled before state writes, the posture history won't update and the posture will appear "not run." This is acceptable — the staleness override will re-select it, and cancelled runs are infrequent with 15-min spacing.

## Research Sources File

`state/research_sources.md` — fully owned and managed by Claude. Seeded from evolve_config.md Research Sources on first run, then Claude adds, prunes, and annotates autonomously.

### Format

```markdown
# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-23T08:00:00Z

## Active Sources

### owner/repo
- **Why:** One sentence on why this source matters for our harness
- **Look for:** Specific patterns, features, or changes to watch for
- **Added:** YYYY-MM-DD (seed|discovered) | **Last deep:** ISO_TIMESTAMP | **Pattern hits:** N
- **Notes:** Free-text observations, productivity notes

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3-5 observations. -->

### owner/repo
- **Why:** How it was found and why it's interesting
- **First seen:** ISO_TIMESTAMP | **Observations:** N/3
- **Initial assessment:** Activity level, star count, relevance

## Dropped Sources
<!-- Removed sources with reason. Prevents re-discovery. -->

### owner/repo
- **Dropped:** YYYY-MM-DD | **Reason:** Why it was removed
```

### Source Management Rules

1. **Add freely** — any repo discovered via trending, dependency analysis, or cross-references
2. **New additions go to Watch List** — 3+ observations before promotion to Active
3. **Promote Watch to Active** when: 3+ observations over 7+ days, consistent activity, and relevant patterns found
4. **Drop** when: 4+ weeks inactive, OR 5+ deep-dives with 0 pattern hits
5. **Never drop** anthropics/claude-code (runtime dependency)
6. **Target:** 8-15 Active sources, 5-10 Watch List
7. **Always record a reason** when promoting or dropping

### Initial Seed

From current evolve_config.md, with purpose annotations added:

| Source | Purpose | Status |
|--------|---------|--------|
| anthropics/claude-code | Runtime we build on — releases, hooks, CLI flags | Active (protected) |
| garrytan/gstack | Harness patterns — skills, review protocols, agent orchestration | Active |
| affaan-m/everything-claude-code | Community patterns, skill collections, optimization | Active |
| hesreallyhim/awesome-claude-code | Curated ecosystem catalog — discover new tools | Active |
| bytedance/deer-flow | Multi-agent orchestration patterns | Active |
| wshobson/agents | Agent framework patterns | Active |
| VoltAgent/awesome-claude-code-subagents | Subagent patterns and skill registry | Active |
| actions/runner | CI/CD runtime — deprecation notices, new features | Active |
| withastro/astro | Framework we use — security fixes, breaking changes | Active |
| verkyyi/tokenman | Self-reference — track forks/adopters | Active |
| godagoo/claude-code-always-on | — | Dropped (inactive since 2026-02-03) |
| humanlayer/humanlayer | — | Dropped (inactive since 2026-01-07) |

## The Four Research Postures

A posture is a mindset and focus area, not a rigid step list. Each run Claude picks one posture. Constraint: must cycle through all 4 within every 8 runs.

### PATTERN HUNT

**Mindset:** "What can we adopt?"

1. Pick 3-4 Active sources to deep-dive. Prioritize:
   - Sources with recent changes (SHA differs from last summary)
   - Sources with high pattern-hit rate
   - Sources not deep-dived in 5+ runs
2. For each: fetch recent commits AND read actual commit diffs or PR descriptions (not just SHAs)
3. For each change ask: "What pattern is this? Could our harness adopt it?"
   - If yes: log the pattern in research_log.md with pattern name, what it does, how it could apply
   - If no: one sentence why not, move on
4. Update source's Last deep and Pattern hits in research_sources.md
5. Quick SHA scan of remaining Active sources (note changes for next run)

**Issue creation:** Issues for patterns with a clear adoption path. Frame as "[evolve] Adopt X pattern from Y".

### PIPELINE WATCH

**Mindset:** "Is anything broken or degrading?"

1. Full failure analysis: `gh run list --status failure --limit 10` with log reading and categorization (ALREADY-FIXED / TRANSIENT / ACTIONABLE)
2. For ACTIONABLE: check existing issues, create if needed
3. Check usage_log.md for cost trends or token saturation
4. Quick SHA scan of all Active sources (note changes, don't deep-dive)

**Issue creation:** Pipeline-fix issues only.

### HORIZON SCAN

**Mindset:** "What's new out there?"

1. GitHub trending search: claude code agent repos pushed in last 7 days, sorted by stars (per_page=15)
2. Cross-references from Active sources: dependencies, forks, related repos
3. Additional search terms: self-evolving systems, agent harness, claude skills
4. For interesting finds: check against Active/Watch/Dropped, add to Watch List if new
5. Review Watch List: check activity, promote (3+ observations over 7+ days + relevant) or drop
6. Review Active sources for staleness (4+ weeks inactive = drop candidate)
7. Check own repo forks/adopters

**Issue creation:** Rare — only if discovered repo has immediately adoptable pattern. Mostly feeds Watch List.

### SYNTHESIS

**Mindset:** "What patterns have emerged across runs?"

1. Read research_log.md entries from last 7 days
2. Read last 8 posture history entries
3. Look for convergent signals: same pattern in 2+ sources, Watch List source with repeated activity, earlier finding now with more evidence
4. Execute time-gated steps that are due:
   - Hour 06 UTC: growth metrics, adoption tracking
   - Hour 12 UTC: SEO & discoverability check
   - Every 7 days: config recheck, scaffold version check
5. Human intent analysis from recent issues
6. Create issues backed by accumulated evidence

**Issue creation:** Multi-run observations become issues. Higher confidence because backed by accumulated evidence.

### Posture Selection Logic

```
last_evolve_summary.md tracks:
  Posture history: [PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, ...]
  Runs since each posture: PATTERN_HUNT:1, PIPELINE_WATCH:2, etc.
```

Selection rules:
1. If any posture hasn't run in 8+ runs: MUST pick it (staleness override)
2. If 3+ new pipeline failures detected in quick health glance: MUST pick PIPELINE_WATCH
3. Otherwise: Claude chooses based on what's most productive right now. Example reasoning:
   - Many sources have new SHAs since last scan → PATTERN_HUNT
   - research_log has 5+ unresolved findings from recent runs → SYNTHESIS
   - Watch List is empty or stale → HORIZON_SCAN
   - Usage costs trending up or recent failures → PIPELINE_WATCH
4. Suggested cadence per 8-run window: PATTERN_HUNT x3, PIPELINE_WATCH x2, HORIZON_SCAN x2, SYNTHESIS x1

### Counter Initialization

On first run (no posture history exists):
- All "runs since" counters start at 8 (all overdue)
- Claude picks PATTERN_HUNT as the first posture (most valuable for cold start)
- Subsequent runs fill in the remaining postures naturally via staleness override

### Every-Run Quick Health Glance

Before posture selection, every run does:
```bash
FAILED=$(gh run list --status failure --limit 5 --json databaseId,workflowName,createdAt \
  -q '.[] | "\(.databaseId) | \(.workflowName) | \(.createdAt)"')
```
If 3+ NEW failures: switch to PIPELINE_WATCH. Otherwise: note for next PIPELINE_WATCH and proceed with chosen posture.

Note: this quick glance is the one cross-cutting concern that runs regardless of posture. It is intentionally lightweight (one API call) and does not break posture isolation — it only forces a posture switch when the system is actively failing.

### Time-Gated Steps

The hour-gated checks (growth metrics at 06, SEO at 12) live in SYNTHESIS. With ~1 SYNTHESIS per 8 runs (~2 hours), there's roughly a 50% chance of hitting any specific hour on a given day. This is acceptable for "once per day" checks — they'll hit within 48 hours. If more reliability is needed, these could be moved to the "always-do" quick glance, but that adds complexity to every run for checks that are low-urgency.

### Non-GitHub Sources

The current prompt hardcodes the OpenAI harness engineering blog, which has been Cloudflare-blocked for the entire run history. Non-GitHub sources are supported in research_sources.md by using the URL as the heading instead of owner/repo:

```markdown
### https://openai.com/index/harness-engineering/
- **Why:** Foundational patterns for agent harnesses
- **Look for:** New sections on tool orchestration, agent loops
- **Fetch:** curl -s "URL" | head -c 1500
```

Claude can add non-GitHub sources during HORIZON_SCAN. Blocked/unreachable sources should be dropped after 3 consecutive failed fetches.

## Prompt Redesign

### Structure

The current prompt is ~400 lines of sequential steps (Step 1, 2, 2a-2h, 3, 4, 5). The new prompt is structured as:

1. **Identity + Mandate** — researcher with judgment, not checklist executor
2. **Context inputs** — same as current + research_sources.md + recent research_log
3. **Always-do** — quick health glance (5 lines)
4. **Posture selection** — read history, pick posture, log choice
5. **Posture playbooks** — 4 blocks, execute the chosen one
6. **Source management** — add/prune/promote rules
7. **Issue creation** — dedup, framing, 3-issue cap
8. **Logging + state update** — structured agent_log, research_log, last_evolve_summary
9. **Hard rules** — cannot promote autonomy, cannot modify YAML, must log, must cycle postures

### Key Prompt Changes

| Removed | Replaced by |
|---------|-------------|
| "Iterate ALL configured sources every run" | Posture-driven source selection |
| Incremental Analysis Rules block | Postures handle depth vs scan naturally |
| "IMPORTANT CONFIG RULES: use ONLY Research Sources listed" | Claude manages own sources |
| Steps 2b-2h as top-level mandatory | Moved into SYNTHESIS posture (time-gated) |
| "The tier rotation system is no longer used" | Postures replace tiers |
| Lightweight Mode Gate | Not needed — postures vary naturally |

### Identity Text

```
You are a self-directing research agent for this project. Your mission:
find patterns, tools, and practices in the broader ecosystem that can
make this harness better — then turn the best findings into actionable issues.

You are NOT a checklist executor. You are a researcher with judgment.
Each run, you choose a research posture, go deep on what matters,
and skip what doesn't. Quality of insight beats breadth of coverage.
```

## Logging and Metrics

### agent_log.md — Structured Run Line

```
TIMESTAMP | evolve.yml | POSTURE_NAME | deep:N scan:N issues:N findings:N | narrative summary
```

### usage_log.md — Add Posture and Issues

The "Log usage metrics" workflow step adds posture and issues to the existing line:
```
TIMESTAMP | evolve | model:X | in:N | out:N | turns:N | cost:N | posture:X | issues:N
```

The posture and issues values are extracted from `state/last_evolve_summary.md` after Claude updates it (the Posture field on line 2 of the summary). This is more robust than a temp file — the summary is already written every run per the logging rules.

### last_evolve_summary.md — Posture History

```markdown
# Last Evolve Summary
Timestamp: ISO_TIMESTAMP
Main HEAD: <sha>
Posture: POSTURE_NAME (reason for choice)
Posture history: [last 8 postures as array]
Runs since each:
  PATTERN_HUNT: N
  PIPELINE_WATCH: N
  HORIZON_SCAN: N
  SYNTHESIS: N

## Source Digests
source/name: <sha> | last-deep: ISO_TIMESTAMP | one-line summary

## Findings This Run
- finding 1
- finding 2
N issues created.
```

### Derivable Metrics (for weekly analysis)

| Metric | Source | Health signal |
|--------|--------|---------------|
| Issue creation rate | issues:N across runs | Target: 1+ per 8 runs |
| Cost per issue | Sum costs / sum issues | Track trend |
| Posture distribution | Count postures in history | Should approximate 3:2:2:1 |
| Source productivity | Pattern hits in research_sources.md | Prune low-hit sources |
| Exploration rate | Watch List size and churn | 3-10 under observation |
| Deep-dive coverage | deep:N per run | PATTERN_HUNT should hit 3-4 |

## YAML Workflow Changes

Minimal changes to the workflow YAML outside the prompt:

1. **Prompt text** — replace the entire PROMPT heredoc with the new posture-based prompt
2. **Posture extraction** — after Claude runs, extract posture and issue count from last_evolve_summary.md for usage_log:
   ```bash
   POSTURE=$(grep -oP 'Posture: \K\w+' state/last_evolve_summary.md 2>/dev/null || echo "unknown")
   ISSUES=$(grep -oP '(\d+) issues created' state/last_evolve_summary.md 2>/dev/null | grep -oP '\d+' || echo "0")
   ```
3. **Remove** the Lightweight Mode Gate and Incremental Analysis Rules (replaced by postures)
4. The existing "Commit state changes via API" step already commits all `state/` files — no change needed (it uses `git diff --name-only state/` which covers research_sources.md automatically)

Everything else stays the same: onboarding check, install, git identity, usage logging, state commit, non-state commit, triage trigger, discovery trigger, labels.

## Migration

1. Create `state/research_sources.md` seeded from current evolve_config.md sources with purpose annotations
2. Replace the evolve.yml prompt (one commit, workflow YAML change = needs-review PR)
3. Remove Research Sources section from evolve_config.md (config keeps build, stack, workflow fit)
4. First run auto-detects "no posture history" and starts with PATTERN_HUNT

No breaking changes to other workflows. The watcher, coder, reviewer, and other workflows don't read evolve's prompt — they only read state files, which maintain the same format (with added structured fields).

## Success Criteria

1. **Research issue creation resumes** — at least 1 evolve-finding issue per 8 runs (vs current 0)
2. **Posture rotation works** — all 4 postures appear in 8-run windows
3. **Source inventory grows** — Watch List has 3+ sources within 24 hours of deployment
4. **Deep analysis returns** — PATTERN HUNT runs read actual diffs, not just SHAs
5. **No regression** — pipeline health detection continues working (PIPELINE WATCH)
