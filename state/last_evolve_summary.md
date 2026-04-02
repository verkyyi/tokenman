# Last Evolve Summary
Timestamp: 2026-04-02T15:31:13Z
Main HEAD: 4ff2d67
Posture: PIPELINE_WATCH (3 runs since last, Security Scan BROKEN #137, underrepresented 1/8 in recent window)
Posture history: [PATTERN_HUNT, HORIZON_SCAN, PIPELINE_WATCH, PATTERN_HUNT, SYNTHESIS, HORIZON_SCAN, PIPELINE_WATCH, PATTERN_HUNT, SYNTHESIS, PATTERN_HUNT, HORIZON_SCAN, PIPELINE_WATCH, PATTERN_HUNT, SYNTHESIS, HORIZON_SCAN, PIPELINE_WATCH, PATTERN_HUNT, SYNTHESIS, PIPELINE_WATCH, HORIZON_SCAN, PATTERN_HUNT, PIPELINE_WATCH, SYNTHESIS, PIPELINE_WATCH, HORIZON_SCAN, PATTERN_HUNT, SYNTHESIS, PIPELINE_WATCH, SYNTHESIS, PATTERN_HUNT, HORIZON_SCAN, PATTERN_HUNT, PIPELINE_WATCH, SYNTHESIS, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS, PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS, PATTERN_HUNT, SYNTHESIS, PIPELINE_WATCH]
Runs since each:
  PATTERN_HUNT: 2
  PIPELINE_WATCH: 0
  HORIZON_SCAN: 3
  SYNTHESIS: 1
Open issues: #137,#131,#124,#103,#100,#48,#22

## Source Digests
anthropics/claude-code: a50a919 | last-deep: 2026-04-02T00:41 | unchanged
hesreallyhim/awesome-claude-code: 2d2b4bc | last-deep: 2026-04-02T09:30 | unchanged
SethGammon/Citadel: 9cbc344 | last-deep: 2026-04-02T00:41 | unchanged
actions/runner: df50788 | last-deep: 2026-03-31T18:30 | unchanged
withastro/astro: 604f939 | last-deep: 2026-03-31T18:30 | SHA changed (3cd1b16 → 604f939)
verkyyi/tokenman: 4ff2d67 | last-deep: never | self
Watch: 0/11 SHAs changed. 11 unchanged.

## Findings This Run
- 10 pipeline failures analyzed: 6 ALREADY-FIXED (Coder ×4, Watcher ×1), 4 ACTIONABLE (Security Scan ×4 — runner-guard SARIF missing, #137 tracks)
- runner-guard v2.5.2 is latest release (Mar 30) — no upstream fix available. Fix must be in our workflow or wait for upstream
- Node.js 20 deprecation: June 2 forced to Node 24, Sept 16 removed. All 14 workflows use checkout@v4. Dependabot PRs #133-#136 (all 14 files) in review. Covered by closed #8.
0 issues created.
