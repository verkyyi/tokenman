# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-04-13T00:24:32Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-12T00:20:26Z | **Pattern hits:** 2 | **SHA:** 9772e13
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. v2.1.101 (Apr 10 19:03Z): /team-onboarding cmd, OS CA cert trust default, settings resilience (bad hook event no longer breaks settings.json), rate-limit retry detail, cmd injection fix in POSIX which, SDK query() cleanup. v2.1.100 (Apr 10 05:16Z): minor. v2.1.98 (Apr 9 19:18Z): Monitor tool, PID namespace isolation, SCRIPT_CAPS, --exclude-dynamic-system-prompt-sections, Vertex wizard, Perforce mode, git_worktree status. 6 Bash security fixes. CC now has 18+ hook events.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-08T18:28:37Z | **Pattern hits:** 0 | **SHA:** e87a7c6
- **Notes:** 0 pattern hits across 50+ observations. SHA change: ticker data only. Submission enforcement governance (owner bypass), Teams subcategory — curation-specific patterns. Retain for HORIZON_SCAN cross-reference only.

### SethGammon/Citadel
- **Why:** Agent orchestration harness (400 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks, skill benchmarking, daemon factory
- **Look for:** Skill benchmarking patterns, skill linting, governance hooks, testing infrastructure, fleet coordination, daemon factory patterns
- **Added:** 2026-03-24 (watch) | **Promoted:** 2026-03-27 (synthesis — 35 obs, closest architecture, V2 patterns) | **Last deep:** 2026-04-10T18:18:54Z | **Pattern hits:** 1 | **SHA:** c446e88
- **Notes:** Promoted from Watch List. Apr 10: gate stderr for CC hook rendering (#106, already adopted in guard.sh), runtime artifacts gitignore fix (#105), install guides (#104). All JS-framework patterns. Roadmap: governance layer, campaign recovery, web dashboard, team collab. 1 pattern hit (circuit breaker #76).

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-08T18:28:37Z | **Pattern hits:** 0 | **SHA:** 4a587ad
- **Notes:** Check releases, not just commits. Docker v29.3.1 + Buildx v0.33.0 (#4324), typescript-eslint 8.58.1. 7711dc5: devtunnel debugger connectivity (#4317, remote DAP relay). Bearer token auth for action archive downloads. PR #4296: batch/dedup action resolution. v2.333.1: removed AllowCaseFunction. Node 20.20.2/24.14.1. Apr 10: dep bumps (Cryptography, @actions/glob, TS 5.9→6.0.2). 0 pattern hits across 14+ observations.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-08T18:28:37Z | **Pattern hits:** 0 | **SHA:** 7fe40bc
- **Notes:** Only actionable for security fixes or features that affect our site build. v6.1.5 (Apr 8): biome upgrade, dlv inlining. Cloudflare adapter 13.1.8: queue consumer fix. No security advisories. 0 harness patterns across 20+ observations.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0 | **SHA:** cdc3cc4
- **Notes:** Used during HORIZON SCAN for adoption tracking. 2 stars, 0 forks, 0 adopters as of 2026-04-11. EvoMap/awesome-agent-evolution (21 stars) monitors tokenman in data/monitor-results.json but not curated — potential growth submission target (#149).

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### hashgraph-online/skill-publish
- **Why:** GitHub Action + CLI for validating, monitoring, and publishing verifiable SKILL.md files (163 stars). OIDC provenance, validate/monitor/quote/publish modes, IndexNow submission, scorecard validation.
- **Look for:** SKILL.md validation rules, GHA publishing patterns, provenance verification, skill registry integration
- **Added:** 2026-04-09 (horizon scan) | **Observations:** 4 | **First seen:** 2026-04-09 | **SHA:** cc1b3c4
- **Notes:** Active (5 commits this week: OIDC flow tightening, scorecard alignment, repo-skill-dir env). JS/Node. Relevant to future skill ecosystem (#66). Publishes to hol.org registry. Uses CITATION.cff, codemeta.json, Zenodo for academic provenance. 2 forks.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 43 | **First seen:** 2026-03-23 | **SHA:** d7f76b5
- **Decision (2026-03-31):** RETAIN on Watch List. 37 obs, 7+ days, 1 pattern hit (SKILL.md standard → #68, closed). 4K stars, 362 forks. Low pattern yield (1/37) — not promoting to Active. Actively maintained — not dropping. Serves as reference for future skill format work.
- **Observations:** 44 | **First seen:** 2026-03-23 | **SHA:** d7f76b5
- **Notes:** 34+ plugins with formal SKILL.md standard. skill-improver quality loop. Codex compatibility layer. 1 pattern hit: SKILL.md quality standard (issue #68, closed). Key reference for skill format. New: mutation testing (#140), graph reasoning (#133), draw agent (#134).

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 44 | **First seen:** 2026-03-24 | **SHA:** 104d39b
- **Decision (2026-03-31):** RETAIN on Watch List. 38 obs, 7+ days, 1 pattern hit (plugin format). 14.3K stars. Active (MongoDB, SAP UI5 plugins added). Distribution channel for #66. Low pattern yield (1/38) — not promoting. Still relevant as plugin ecosystem reference.
- **Observations:** 52 | **First seen:** 2026-03-24 | **SHA:** 7ed5231
- **Notes:** PR #1115: bash prefix for .sh hooks. Version field for cache invalidation. Standard plugin format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Distribution channel for #66. 1 pattern hit (official plugin format). Apr 10: session-report plugin adds per-day timeline + collapsible cache-breaks (analyze-sessions.mjs, template.html). Box plugin (#1286) + SAP CAP MCP server (#1328). Catalog growth continues.

### agent-sh/agnix
- **Why:** CLAUDE.md/SKILL.md linter and LSP (103 stars) — validates AI coding assistant config files, autofixes, IDE plugins
- **Look for:** Validation rules for CLAUDE.md, SKILL.md format standards, CI integration patterns, autofix capabilities
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 50 | **First seen:** 2026-03-24 | **SHA:** d97dae2
- **Decision (2026-03-31):** RETAIN on Watch List. 39 obs, 7+ days, 0 pattern hits. Key CC spec tracker but 0 adoptable CI patterns — not promoting. Active and useful — not dropping.
- **Observations:** 51 | **First seen:** 2026-03-24 | **SHA:** d97dae2
- **Notes:** v0.18.0: Codex CLI plugin manifest validation (CDX-PL-001 to CDX-PL-014, 14 rules). CC now has 18 hook events. 385+ rules, 124+ auto-fixes. Relevant to #66/#68. Apr 11: dep bumps (actionlint 1.7.12, toml 1.0.1, similar 3.0.0, claude-code-action 1.0.93).

### Vigilant-LLC/runner-guard
- **Why:** CI/CD security scanner (6 stars, Go) — 31 detection rules for GHA vulnerabilities + supply chain dependency scanning: fork checkout exploits, expression injection, AI config injection (CLAUDE.md hijacking), supply chain steganography, unpinned actions, compromised package detection, auto-fix, SARIF output
- **Look for:** GHA vulnerability patterns applicable to our workflows, action pinning auto-fix, AI config injection defenses, SARIF integration for Code Scanning, compromised package detection
- **Added:** 2026-04-01 (horizon scan) | **Observations:** 18 | **First seen:** 2026-04-01 | **SHA:** 2086509
- **Notes:** Only scanner specifically targeting AI agent attack vectors in CI/CD. v3.1.4: 8 new prt-scan campaign IOCs (AI-powered GHA exploitation, 500+ malicious PRs, active Mar 2026). Total 39 signatures, 7 campaign files. Renamed fix→remediation in JSON. Docker image (10.4MB distroless), PagerDuty+Slack+Webhook alerting, org scanning. Issue #127 created for adoption. Go single binary. Last deep: 2026-04-06T21:16Z.

### affaan-m/agentshield
- **Why:** AI agent security scanner (289 stars, 55 forks) — scans .claude/ for secrets, permission misconfigs, hook injection, MCP risks, prompt injection vectors. CLI + GitHub Action + GitHub App.
- **Look for:** Agent config audit rules applicable to our harness, CI integration patterns, auto-fix capabilities for security issues
- **Added:** 2026-04-01 (horizon scan) | **Observations:** 9 | **First seen:** 2026-04-01 | **SHA:** 162e8e1
- **Notes:** From affaan-m (everything-claude-code author). TypeScript. Covers agent config security surface (complementary to runner-guard which covers CI/CD workflow security). Detects hardcoded secrets, overly permissive permissions, hook injection. Built at Claude Code Hackathon. GitHub Action available. Part of ECC ecosystem. Our .claude/ config is minimal so immediate value is low — monitor for CI integration patterns. Apr 10: runtime install recovery hardening, runtime status command, miniclaw fallback. All runtime-specific, 0 CI patterns.

### jnurre64/claude-agent-dispatch
- **Why:** Label-driven Claude Code GHA dispatch (Shell, 2 stars) — closest architecture to tokenman. Modular agent-dispatch.sh + lib/, label state machine (10 agent:* labels), two-phase plan→implement with human checkpoint, ShellCheck + BATS-Core CI testing.
- **Look for:** Shell script quality patterns, label state machine design, worktree isolation, error trap handling, BATS test patterns
- **Added:** 2026-04-02 (horizon scan) | **Observations:** 13 | **First seen:** 2026-04-02 | **SHA:** b1f8029
- **Decision (2026-04-09):** RETAIN on Watch. Meets quantitative promotion criteria (14 obs, 2 hits, 7d) but deep-dives found 0 directly adoptable patterns for GHA bash/markdown harness. Shell-library architecture patterns (modular lib/, BATS testing) don't transfer. Architecturally closest peer but insufficient pattern yield for Active promotion. Re-evaluate if new PRs introduce transferable patterns.
- **Observations:** 18 | **First seen:** 2026-04-02 | **SHA:** 3f44fd8
- **Notes:** Created 2026-03-21, actively maintained. Shell-only, no Node/Python deps. Reusable workflows (dispatch-*.yml) consumed via workflow_call. CI validates all scripts with ShellCheck + BATS. Architecturally closest to tokenman: issue-driven, label-based state, GHA runners, claude -p headless. 2 pattern hits. Last deep: 2026-04-08T18:28:37Z. PR #31: robust JSON extraction from AI output (_extract_review_json helper, awk brace-depth fallback for narrative preamble/fence/postamble). 172 BATS tests green.

### Vimalk0703/shipworthy
- **Why:** Shell-based Claude Code plugin (5 stars, 1 fork) — 52 invisible engineering skills, auto specs, TDD, security hooks, quality gates, self-improving retrospective. "97% vs 41% on blind benchmark". Advisory-first approach.
- **Look for:** Self-improving retrospective patterns, quality gate implementation in Shell, advisory-first guardrail approach, skill benchmarking methodology
- **Added:** 2026-04-11 (horizon scan) | **Observations:** 1 | **First seen:** 2026-04-11 | **SHA:** 21a80ba
- **Observations:** 4 | **First seen:** 2026-04-11 | **SHA:** 21a80ba
- **Notes:** Created 2026-03-26, actively maintained. Shell language — same as tokenman scripts. v1.5.0 "Advisory-First Revamp — guide, don't gate" (config-gated hooks, is_rule_enabled(), suggestion tone). v1.4.1 Security Hardening (Python injection fixes, TOCTOU, 12-test audit). v1.3.0 Context Intelligence (signal→learning→constraint flywheel, regression fence). All patterns interactive-CLI, 0 CI-adoptable. Context flywheel validates our feedback-learner direction.

### amazinglvxw/enso-os
- **Why:** Self-evolving bash+python harness (19 stars) — 1267 LOC, 10 shell hooks, agent-memory, self-evolution. Conceptually similar to tokenman.
- **Look for:** Shell hook patterns, self-evolution mechanisms, bash harness architecture, memory persistence patterns
- **Added:** 2026-04-08 (horizon scan) | **Observations:** 8 | **First seen:** 2026-04-08 | **SHA:** 1e569d4
- **Notes:** Created 2026-03-29, actively maintained. Shell language. Topics: agent-os, self-evolution, shell-hooks, claude-code. Rapid growth: 19→40 stars, 0→3 forks. v0.4.0 discipline plugin (multi-framework adapter), proactive lesson notification (text-based tracking replaces broken date comparison), lesson provenance [seed:XXXXXX] hash, applies_when context tags. All interactive-CLI patterns, 0 CI-adoptable. Validates our feedback-learner direction.

### montenegronyc/backporcher
- **Why:** Parallel Claude Code agent dispatcher (10 stars, 1 fork, Python) — GitHub Issues as task queue, sandboxed worktrees, coordinator review, CI gating, auto-merge. 100% auto-merge rate on first production run (15 PRs, 0 manual interventions).
- **Look for:** Batch orchestration with dependency chains, blast radius analysis (Tree-sitter + BFS), learnings persistence (success/failure feedback loop), 3-tier approval modes, code graph navigation maps, coordinator agent review patterns
- **Added:** 2026-04-05 (horizon scan) | **Observations:** 6 | **First seen:** 2026-04-05 | **SHA:** 833b798
- **Notes:** Created 2026-03-06, pushed Apr 2. Python + asyncio. Uses `claude -p` headless (same as us). Pipeline: Issue → Haiku triage → batch orchestrator → Sonnet code graph → sandboxed worktree → build verify → PR → coordinator review → CI monitor (auto-retry 3x) → merge. Three approval modes: full-auto, review-merge (default), review-all. Learnings from past success/failure fed to future agents. Most architecturally relevant HS discovery in 20+ runs. Deep-dived: rate-limit fallback chain (model escalation sonnet→opus, multi-backend rotation), code graph navigation (Tree-sitter+BFS blast radius), no-changes label cleanup. All Python-specific, 0 CI-adoptable patterns. Last deep: 2026-04-05T15:16Z.

## Dropped Sources
<!-- Removed sources with reason. Kept for history so we don't re-discover them. -->

### wanshuiyin/Auto-claude-code-research-in-sleep
- **Dropped:** 2026-04-11 | **Reason:** 15+ observations, 0 CI-harness pattern hits. ML-research domain (Python + Markdown) fundamentally different from GHA bash/markdown harness. All patterns ML-specific (effort levels, experiment integrity, cross-model audit). "Conceptually closest to evolve's autonomous research methodology" but 0 transferable patterns. 5.4K stars, very active — just irrelevant to our architecture.

### ComposioHQ/agent-orchestrator
- **Dropped:** 2026-04-11 | **Reason:** 11 observations over 4 days, 0 CI-harness pattern hits. Interactive orchestration platform (TypeScript/npm, 5.8K stars, 934+ PRs) — fundamentally different paradigm from GHA-driven harness. All patterns platform-specific (design systems, pty handling, cursor agent support). Very active but architecturally irrelevant. Shell injection fix noted but already in different domain.

### affaan-m/everything-claude-code
- **Dropped:** 2026-04-09 | **Reason:** 65+ observations, 0 CI-harness pattern hits. Demoted from Active 2026-04-02 (13+ consecutive 0-pattern observations). All patterns interactive-session specific (CI cleanup, codex sync, install hardening, release gates). 147K stars but fundamentally different paradigm from GHA-driven CI harness. 1 pattern hit total (early safety-guard hooks). Retained on Watch 7 days post-demotion with continued 0 CI patterns.

### bytedance/deer-flow
- **Dropped:** 2026-04-09 | **Reason:** 77+ observations, 0 CI-harness pattern hits. Demoted from Active 2026-04-02 (19+ consecutive 0-pattern deep-dives). All patterns Python application-specific (skill filters, concurrent locks, Langfuse tracing). Very active (5+ commits/day) but fundamentally different stack. 1 pattern hit total (early). No transferable patterns despite most extensively monitored source.

### code-yeongyu/oh-my-openagent
- **Dropped:** 2026-04-01 | **Reason:** 24 observations, 0 pattern hits. Architecture fundamentally different (interactive TUI vs CI harness). Deep-dived 4 PRs — all interactive-session specific. 44K stars, 3273 forks. Active but irrelevant to CI-based harness architecture.

### wshobson/agents
- **Dropped:** 2026-03-27 | **Reason:** 18+ days stale (SHA 91fe43e unchanged since first observation), 0 pattern hits. Python/uv/Pydantic stack incompatible with bash harness. PluginEval 3-layer framework validated closed #66/#68 but no transferable patterns. 32K stars, 3504 forks.

### thedotmack/claude-mem
- **Dropped:** 2026-03-27 | **Reason:** 35 observations, 0 patterns. SHA a656af2 unchanged 12th consecutive. Fundamentally different paradigm (compress-filter-inject vs state/ read/write). No transferable patterns despite extensive monitoring.

### sickn33/antigravity-awesome-skills
- **Dropped:** 2026-03-27 | **Reason:** 42 observations, 0 harness patterns. Skill catalog (1,328+ skills) — distribution model confirmed direction of #66 but no harness-transferable patterns. v9.0.0 reached. Active but irrelevant architecture.

### OthmanAdi/planning-with-files
- **Dropped:** 2026-03-27 | **Reason:** 32 observations, 0 patterns. SHA bb3a21a unchanged 11th consecutive. Validates markdown-as-memory concept already adopted. No new patterns despite active community (115+ PRs).

### vibeeval/vibecosystem
- **Dropped:** 2026-03-27 | **Reason:** 31 observations, SHA 49840c2 unchanged 12th consecutive. 1 pattern hit (multi-agent review quality gate) already noted. Self-learning pattern similar to our feedback-learner — validated but not adoptable. Stale.

### BloopAI/vibe-kanban
- **Dropped:** 2026-03-26 | **Reason:** 28 observations, 1 pattern hit (SHA pinning, already adopted). UI-focused agent management platform — no remaining harness patterns. Active but irrelevant to our architecture.

### ruvnet/ruflo
- **Dropped:** 2026-03-26 | **Reason:** 27 observations, 0 harness patterns after deep-dive. ruflo-specific multi-agent swarm architecture fundamentally different from our single-agent harness. No transferable patterns.

### intertwine/hive-orchestrator
- **Dropped:** 2026-03-26 | **Reason:** 25 observations, 0 direct pattern hits. Only 14 stars, low activity (last pushed Mar 24). Architecturally similar concept but too small/inactive to yield patterns. Validates #66 packaging but so do larger sources.

### volcengine/OpenViking
- **Dropped:** 2026-03-26 | **Reason:** 35+ observations, 0 harness pattern hits. Very active but all Python-specific (openclaw-plugin, Windows wheel packaging, Chinese docs). Circuit breaker pattern already adopted via #76 before Watch List period. No transferable patterns despite extensive monitoring.

### VoltAgent/awesome-claude-code-subagents
- **Dropped:** 2026-03-24 | **Reason:** 0 pattern hits over 11+ observation runs and multiple deep-dives. Content is framework-specific experts (Rails, Expo, FastAPI) — not harness patterns.

### godagoo/claude-code-always-on
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-02-03 (7+ weeks), no new patterns found

### humanlayer/humanlayer
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-01-07 (11+ weeks), no relevant patterns

### agent-sh/agentsys
- **Dropped:** 2026-04-05 | **Reason:** 9 observations over 7 days, 0 CI-harness pattern hits. Plugin marketplace architecture (672 stars, JavaScript) fundamentally different from bash/markdown harness. All patterns interactive-session specific. Same org as agnix (retained on Watch as CC spec tracker).

### garrytan/gstack
- **Dropped:** 2026-04-06 | **Reason:** 66+ observations, 10d on Watch since demotion (2026-03-27), 0 CI-harness patterns since. Historically most productive source (9 pattern hits across v0.9.7-v0.11.18.2) but pattern yield exhausted — all recent patterns (review army, ClaHub, security wave) interactive-session specific. SHA 03973c2 stale. Synthesis-flagged for drop.

### shinpr/claude-code-workflows
- **Dropped:** 2026-04-05 | **Reason:** 17 observations over 7 days, 0 CI-harness pattern hits. Multi-agent workflows (257 stars) — all skill organization and coordination patterns interactive-session specific. PRs #100-102 deep-dived, 0 CI applicability. Active but architecturally irrelevant.
