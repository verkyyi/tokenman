# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-04-06T00:41:47Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-05T21:12:19Z | **Pattern hits:** 2 | **SHA:** b543a25
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. v2.1.92 (Apr 4): forceRemoteSettingsRefresh fail-closed policy, Stop hook preventContinuation fix, Write tool 60% faster (tabs/&/$), Linux sandbox seccomp, /tag+/vim removed, Bedrock setup wizard, per-model /cost breakdown, tmux pane fix. Previous: v2.1.91 MCP 500K result override, disableSkillShellExecution, bin/ in plugins. v2.1.90 /powerup, plugin offline cache. CC now has 18+ hook events.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-05T04:06:27Z | **Pattern hits:** 0 | **SHA:** 658dc4e
- **Notes:** 0 pattern hits across 45+ observations. Submission enforcement governance (owner bypass), Teams subcategory — curation-specific patterns. Retain for HORIZON_SCAN cross-reference only.

### SethGammon/Citadel
- **Why:** Agent orchestration harness (400 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks, skill benchmarking, daemon factory
- **Look for:** Skill benchmarking patterns, skill linting, governance hooks, testing infrastructure, fleet coordination, daemon factory patterns
- **Added:** 2026-03-24 (watch) | **Promoted:** 2026-03-27 (synthesis — 35 obs, closest architecture, V2 patterns) | **Last deep:** 2026-04-05T21:12:19Z | **Pattern hits:** 1 | **SHA:** 37d151d
- **Notes:** Promoted from Watch List. PR #93 (Apr 2): community docs, roadmap, contributing guide. Roadmap: governance layer (per-agent policies, immutable audit), campaign recovery, web dashboard, team collab. Governance concept already informal in our autonomy rules. Runtime-agnostic foundation (#73-#87): JS framework refactor, multi-runtime direction. Not adoptable for bash/markdown harness. 1 pattern hit (circuit breaker #76).

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-05T21:12:19Z | **Pattern hits:** 0 | **SHA:** df50788
- **Notes:** Check releases, not just commits. df50788: brace-expansion dep bump. Bearer token auth for action archive downloads. PR #4296 (Mar 31): batch/dedup action resolution (merged). v2.333.1 (Mar 27): removed AllowCaseFunction. Node 20.20.2/24.14.1. 0 pattern hits across 11+ observations.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-03T15:20 | **Pattern hits:** 0 | **SHA:** fa8033b
- **Notes:** Only actionable for security fixes or features that affect our site build. SHA changed 23425e2→fa8033b (Apr 4). 0 harness patterns across 18+ observations.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0 | **SHA:** d3022f6
- **Notes:** Used during HORIZON SCAN for adoption tracking. 0 forks, 0 adopters as of 2026-04-05. EvoMap/awesome-agent-evolution (21 stars) monitors tokenman in data/monitor-results.json but not curated — potential growth submission target (#149).

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Demoted:** 2026-04-02 (synthesis — 13+ consecutive 0-pattern observations, all interactive-session specific, 0 CI-harness patterns)
- **Observations:** 59+ | **First seen:** 2026-03-20 | **SHA:** a1e37d7
- **Notes:** 1 pattern hit total (safety-guard PreToolUse hooks, early). CI cleanup, codex sync, install hardening — all interactive-session. From same author as agentshield. Monitor for CI-relevant patterns.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Demoted:** 2026-04-02 (synthesis — 19+ consecutive 0-pattern deep-dives, all Python application-specific, fundamentally different stack)
- **Observations:** 70+ | **First seen:** 2026-03-21 | **SHA:** ed90a2e
- **Notes:** 1 pattern hit total (early). Very active (5+ commits/day). Per-agent skill filter, concurrent file locks, Langfuse tracing — all Python. No transferable harness patterns despite extensive monitoring. Apr 5: sandbox guard fix, API soul field fix, deps update.

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** Non-Codex workflow patterns, CI-transferable techniques
- **Demoted:** 2026-03-27 (synthesis — 14 consecutive PH with 0 adoptable patterns, all Codex/interactive-session specific)
- **Observations:** 63+ | **First seen:** 2026-03-20 | **SHA:** 422f172
- **Notes:** Historically most productive source (9 pattern hits across v0.9.7-v0.11.18.2). Demoted because pattern yield exhausted for CI-based harness. v0.15.10.0: review army idempotency + cross-review dedup, native OpenClaw skills + ClaHub publishing. All interactive-session patterns. Monitor for CI-relevant patterns.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 41 | **First seen:** 2026-03-23 | **SHA:** d7f76b5
- **Decision (2026-03-31):** RETAIN on Watch List. 37 obs, 7+ days, 1 pattern hit (SKILL.md standard → #68, closed). 4K stars, 362 forks. Low pattern yield (1/37) — not promoting to Active. Actively maintained — not dropping. Serves as reference for future skill format work.
- **Notes:** 34+ plugins with formal SKILL.md standard. skill-improver quality loop. Codex compatibility layer. 1 pattern hit: SKILL.md quality standard (issue #68, closed). Key reference for skill format. New: mutation testing (#140), graph reasoning (#133), draw agent (#134).

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 44 | **First seen:** 2026-03-24 | **SHA:** 104d39b
- **Decision (2026-03-31):** RETAIN on Watch List. 38 obs, 7+ days, 1 pattern hit (plugin format). 14.3K stars. Active (MongoDB, SAP UI5 plugins added). Distribution channel for #66. Low pattern yield (1/38) — not promoting. Still relevant as plugin ecosystem reference.
- **Notes:** PR #1115: bash prefix for .sh hooks. Version field for cache invalidation. Standard plugin format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Distribution channel for #66. 1 pattern hit (official plugin format). Apr 3: SonarQube plugin added (#1085, secrets-scanning hooks).

### agent-sh/agnix
- **Why:** CLAUDE.md/SKILL.md linter and LSP (103 stars) — validates AI coding assistant config files, autofixes, IDE plugins
- **Look for:** Validation rules for CLAUDE.md, SKILL.md format standards, CI integration patterns, autofix capabilities
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 45 | **First seen:** 2026-03-24 | **SHA:** 0089efa
- **Decision (2026-03-31):** RETAIN on Watch List. 39 obs, 7+ days, 0 pattern hits. Key CC spec tracker but 0 adoptable CI patterns — not promoting. Active and useful — not dropping.
- **Notes:** v0.18.0: Codex CLI plugin manifest validation (CDX-PL-001 to CDX-PL-014, 14 rules). CC now has 18 hook events. 385+ rules, 124+ auto-fixes. Relevant to #66/#68.

### Vigilant-LLC/runner-guard
- **Why:** CI/CD security scanner (6 stars, Go) — 18 detection rules for GHA vulnerabilities: fork checkout exploits, expression injection, AI config injection (CLAUDE.md hijacking), supply chain steganography, unpinned actions, auto-fix, SARIF output
- **Look for:** GHA vulnerability patterns applicable to our workflows, action pinning auto-fix, AI config injection defenses, SARIF integration for Code Scanning
- **Added:** 2026-04-01 (horizon scan) | **Observations:** 7 | **First seen:** 2026-04-01 | **SHA:** 5d60811
- **Notes:** Only scanner specifically targeting AI agent attack vectors in CI/CD. Deep-dived: 18→31 rules. v2.7.0 (Apr 5): batch multi-repo scanning, file path + manual entry, permissions-aware severity, vigilantdefense.com domain. Issue #127 created for adoption. Go single binary. Last deep: 2026-04-05T04:06Z.

### affaan-m/agentshield
- **Why:** AI agent security scanner (289 stars, 55 forks) — scans .claude/ for secrets, permission misconfigs, hook injection, MCP risks, prompt injection vectors. CLI + GitHub Action + GitHub App.
- **Look for:** Agent config audit rules applicable to our harness, CI integration patterns, auto-fix capabilities for security issues
- **Added:** 2026-04-01 (horizon scan) | **Observations:** 4 | **First seen:** 2026-04-01 | **SHA:** 0440830
- **Notes:** From affaan-m (everything-claude-code author). TypeScript. Covers agent config security surface (complementary to runner-guard which covers CI/CD workflow security). Detects hardcoded secrets, overly permissive permissions, hook injection. Built at Claude Code Hackathon. GitHub Action available. Part of ECC ecosystem (42K+ stars). Our .claude/ config is minimal so immediate value is low — monitor for CI integration patterns. Apr 5: prompt defense posture audit rules added.

### wanshuiyin/Auto-claude-code-research-in-sleep
- **Why:** Autonomous ML research harness (5.4K stars, 455 forks) — markdown-only skills, cross-model review loops, idea discovery. Conceptually closest to evolve's autonomous research methodology.
- **Look for:** Autonomous research workflow patterns, cross-model review loops, skill organization, persistent memory patterns
- **Added:** 2026-04-03 (horizon scan) | **Observations:** 9 | **First seen:** 2026-04-03 | **SHA:** d86b656
- **Notes:** ARIS v0.3.3. Recent: Zenodo DOI badge, What's New updates — doc-only. Python + Markdown. ML-research domain, not CI harness. Same methodology concept as our evolve. Monitor for transferable workflow patterns.

### jnurre64/claude-agent-dispatch
- **Why:** Label-driven Claude Code GHA dispatch (Shell, 2 stars) — closest architecture to tokenman. Modular agent-dispatch.sh + lib/, label state machine (10 agent:* labels), two-phase plan→implement with human checkpoint, ShellCheck + BATS-Core CI testing.
- **Look for:** Shell script quality patterns, label state machine design, worktree isolation, error trap handling, BATS test patterns
- **Added:** 2026-04-02 (horizon scan) | **Observations:** 9 | **First seen:** 2026-04-02 | **SHA:** aecacf4
- **Notes:** Created 2026-03-21, actively maintained. Shell-only, no Node/Python deps. PR #15: runner setup guide (130-line SKILL.md expansion, public repo security warnings, credential mgmt). Reusable workflows (dispatch-*.yml) consumed via workflow_call. CI validates all scripts with ShellCheck + BATS. Architecturally closest to tokenman: issue-driven, label-based state, GHA runners, claude -p headless. Deep-dived architecture: scripts/lib/ (5 modules), BATS tests (6 files), global error trap with diagnostic comments, label state machine (10 labels), worktree stale prune. Issues: #129 (ShellCheck), #131 (dependabot), #139 (BATS testing). 2 pattern hits. Last deep: 2026-04-05T15:16Z. Apr 5: direct implement feature (PR #16, 1790 additions), per-workflow concurrency groups (prevent cross-workflow cancellation). Both patterns not CI-adoptable for our architecture.

### montenegronyc/backporcher
- **Why:** Parallel Claude Code agent dispatcher (10 stars, 1 fork, Python) — GitHub Issues as task queue, sandboxed worktrees, coordinator review, CI gating, auto-merge. 100% auto-merge rate on first production run (15 PRs, 0 manual interventions).
- **Look for:** Batch orchestration with dependency chains, blast radius analysis (Tree-sitter + BFS), learnings persistence (success/failure feedback loop), 3-tier approval modes, code graph navigation maps, coordinator agent review patterns
- **Added:** 2026-04-05 (horizon scan) | **Observations:** 3 | **First seen:** 2026-04-05 | **SHA:** 833b798
- **Notes:** Created 2026-03-06, pushed Apr 2. Python + asyncio. Uses `claude -p` headless (same as us). Pipeline: Issue → Haiku triage → batch orchestrator → Sonnet code graph → sandboxed worktree → build verify → PR → coordinator review → CI monitor (auto-retry 3x) → merge. Three approval modes: full-auto, review-merge (default), review-all. Learnings from past success/failure fed to future agents. Most architecturally relevant HS discovery in 20+ runs. Deep-dived: rate-limit fallback chain (model escalation sonnet→opus, multi-backend rotation), code graph navigation (Tree-sitter+BFS blast radius), no-changes label cleanup. All Python-specific, 0 CI-adoptable patterns. Last deep: 2026-04-05T15:16Z.

## Dropped Sources
<!-- Removed sources with reason. Kept for history so we don't re-discover them. -->

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

### shinpr/claude-code-workflows
- **Dropped:** 2026-04-05 | **Reason:** 17 observations over 7 days, 0 CI-harness pattern hits. Multi-agent workflows (257 stars) — all skill organization and coordination patterns interactive-session specific. PRs #100-102 deep-dived, 0 CI applicability. Active but architecturally irrelevant.
