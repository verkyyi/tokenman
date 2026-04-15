# Last Evolve Summary
Timestamp: 2026-04-15T18:31:34Z
Main HEAD: 303380b
Posture: PIPELINE_WATCH (PH/HS both 0-yield early exit, SYN just ran — PW only productive option. Cost/model investigation.)
Posture history: [PIPELINE_WATCH, SYNTHESIS, PIPELINE_WATCH, PATTERN_HUNT, HORIZON_SCAN, SYNTHESIS, PIPELINE_WATCH, SYNTHESIS]
Runs since each:
  PATTERN_HUNT: 3
  PIPELINE_WATCH: 0
  HORIZON_SCAN: 4
  SYNTHESIS: 1
Open issues: #22, #48, #100, #103, #124, #149

## Source Digests
anthropics/claude-code: f348a16 | last-deep: 2026-04-15T06:40:00Z | unchanged (v2.1.109 latest).
hesreallyhim/awesome-claude-code: d3ee97d | last-deep: 2026-04-08T18:28:37Z | changed (67251e1→d3ee97d).
SethGammon/Citadel: 9713f2b | last-deep: 2026-04-13T06:47:28Z | changed (c446e88→9713f2b).
actions/runner: 4a587ad | last-deep: 2026-04-08T18:28:37Z | unchanged.
withastro/astro: eca29c1 | last-deep: 2026-04-08T18:28:37Z | changed (8ddb800→eca29c1).
verkyyi/tokenman: 303380b | last-deep: never | self. 2 stars, 0 forks.
Watch: 0/10 changed. All SHAs unchanged. Portfolio: 6 Active + 10 Watch.

## Findings This Run
- Cost correction: 7-day actual $147.88 (Apr 9-15), near $150 target. Previous $107/wk was Haiku-period artifact. Opus steady-state projects ~$165/wk (above target). The apparent 51% cost drop was driven by rate-limit-induced Haiku fallback, not structural improvement.
- Extended Haiku fallback: ~17h tail after rate-limit resolution (01:05Z → 18:24Z Apr 15). All 13 pre-this-run Apr 15 runs were Haiku despite --model opus config. Opus recovery confirmed this run.
- All 10 pipeline failures ALREADY-FIXED/TRANSIENT. 0 actionable. 0 open pipeline-fix issues.
- SHA scan: Active 3/5 changed (awesome-cc, Citadel, astro), Watch 0/10 unchanged. Self flat 2 stars 0 forks.
0 issues created.
