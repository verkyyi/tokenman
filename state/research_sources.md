# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-04-02T18:25:00Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-02T00:41 | **Pattern hits:** 2 | **SHA:** a50a919
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. v2.1.90 (Apr 2): /powerup interactive lessons, plugin offline cache, --resume cache miss fix (benefits headless workflows), auto mode boundary enforcement (validates CLAUDE.md autonomy), PowerShell security hardening, SSE/transcript quadratic→linear perf, Edit/Write format-on-save fix. Previous: v2.1.89 defer permission, autocompact fix, TaskCreated hook. v2.1.88 PermissionDenied hook. v2.1.85 hook `if` field (#122). v2.1.83 security patterns (#100). CC now has 18+ hook events.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-02T09:30 | **Pattern hits:** 0 | **SHA:** f28c6b6
- **Notes:** 0 pattern hits across 36+ observations. All recent commits are ticker auto-updates only. Retain for HORIZON_SCAN cross-reference only.

### SethGammon/Citadel
- **Why:** Agent orchestration harness (400 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks, skill benchmarking, daemon factory
- **Look for:** Skill benchmarking patterns, skill linting, governance hooks, testing infrastructure, fleet coordination, daemon factory patterns
- **Added:** 2026-03-24 (watch) | **Promoted:** 2026-03-27 (synthesis — 35 obs, closest architecture, V2 patterns) | **Last deep:** 2026-04-02T00:41 | **Pattern hits:** 1 | **SHA:** 9cbc344
- **Notes:** Promoted from Watch List. Runtime-agnostic foundation (#73-#87): runtime detection registry, fleet coordination (claims/instances/sweep), policy engine, structured telemetry schema, hook normalization across runtimes. Massive JS framework refactor — shows multi-runtime direction. Not adoptable for bash/markdown harness. 1 pattern hit (circuit breaker #76).

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-31T18:30 | **Pattern hits:** 0 | **SHA:** df50788
- **Notes:** Check releases, not just commits. df50788: brace-expansion dep bump. Bearer token auth for action archive downloads. PR #4296 (Mar 31): batch/dedup action resolution (merged). v2.333.1 (Mar 27): removed AllowCaseFunction. Node 20.20.2/24.14.1. 0 pattern hits across 11+ observations.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-04-02T18:25 | **Pattern hits:** 0 | **SHA:** 6d5469e
- **Notes:** Only actionable for security fixes or features that affect our site build. Recent: Cloudflare miniflare restart (#16059), test coverage (#16189), e2e test fix (#16183). SHA changed 604f939 → 6d5469e (Apr 2). 0 harness patterns across 16+ observations.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0 | **SHA:** 12d301c
- **Notes:** Used during HORIZON SCAN for adoption tracking. 0 forks, 0 adopters as of 2026-04-02.

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Demoted:** 2026-04-02 (synthesis — 13+ consecutive 0-pattern observations, all interactive-session specific, 0 CI-harness patterns)
- **Observations:** 55+ | **First seen:** 2026-03-20 | **SHA:** bf3fd69
- **Notes:** 1 pattern hit total (safety-guard PreToolUse hooks, early). CI cleanup, codex sync, install hardening — all interactive-session. From same author as agentshield. Monitor for CI-relevant patterns.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Demoted:** 2026-04-02 (synthesis — 19+ consecutive 0-pattern deep-dives, all Python application-specific, fundamentally different stack)
- **Observations:** 55+ | **First seen:** 2026-03-21 | **SHA:** ef711a4
- **Notes:** 1 pattern hit total (early). Very active (5+ commits/day). Per-agent skill filter, concurrent file locks, Langfuse tracing — all Python. No transferable harness patterns despite extensive monitoring.

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** Non-Codex workflow patterns, CI-transferable techniques
- **Demoted:** 2026-03-27 (synthesis — 14 consecutive PH with 0 adoptable patterns, all Codex/interactive-session specific)
- **Observations:** 52+ | **First seen:** 2026-03-20 | **SHA:** 6169273
- **Notes:** Historically most productive source (9 pattern hits across v0.9.7-v0.11.18.2). Demoted because pattern yield exhausted for CI-based harness. v0.14.3.0: Review Army (7 parallel specialist reviewers), always-on adversarial review, scope drift detection, ship idempotency. All interactive-session patterns. Monitor for CI-relevant patterns.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 41 | **First seen:** 2026-03-23 | **SHA:** d7f76b5
- **Decision (2026-03-31):** RETAIN on Watch List. 37 obs, 7+ days, 1 pattern hit (SKILL.md standard → #68, closed). 4K stars, 362 forks. Low pattern yield (1/37) — not promoting to Active. Actively maintained — not dropping. Serves as reference for future skill format work.
- **Notes:** 34+ plugins with formal SKILL.md standard. skill-improver quality loop. Codex compatibility layer. 1 pattern hit: SKILL.md quality standard (issue #68, closed). Key reference for skill format. New: mutation testing (#140), graph reasoning (#133), draw agent (#134).

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 42 | **First seen:** 2026-03-24 | **SHA:** b091cb4
- **Decision (2026-03-31):** RETAIN on Watch List. 38 obs, 7+ days, 1 pattern hit (plugin format). 14.3K stars. Active (MongoDB, SAP UI5 plugins added). Distribution channel for #66. Low pattern yield (1/38) — not promoting. Still relevant as plugin ecosystem reference.
- **Notes:** PR #1115: bash prefix for .sh hooks. Version field for cache invalidation. Standard plugin format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Distribution channel for #66. 1 pattern hit (official plugin format).

### agent-sh/agnix
- **Why:** CLAUDE.md/SKILL.md linter and LSP (103 stars) — validates AI coding assistant config files, autofixes, IDE plugins
- **Look for:** Validation rules for CLAUDE.md, SKILL.md format standards, CI integration patterns, autofix capabilities
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 44 | **First seen:** 2026-03-24 | **SHA:** d7eaebe
- **Decision (2026-03-31):** RETAIN on Watch List. 39 obs, 7+ days, 0 pattern hits. Key CC spec tracker but 0 adoptable CI patterns — not promoting. Active and useful — not dropping.
- **Notes:** v0.17.0: CC now has 18 hook events (PermissionDenied added in v2.1.88), HTTP hooks, once/async fields. 385 rules, 124 auto-fixes. Relevant to #66/#68.

### agent-sh/agentsys
- **Why:** Comprehensive plugin/agent/skill system (672 stars, 69 forks) from same org as agnix — 19 plugins, 47 agents, 39 skills
- **Look for:** Plugin marketplace patterns, repo-intel tooling, CI-transferable agent coordination, skill management architecture
- **Added:** 2026-03-29 (horizon scan) | **Observations:** 8 | **First seen:** 2026-03-29 | **SHA:** 94326af
- **Notes:** Same org as agnix (Watch List). v5.8.1 (Mar 28). 19-plugin marketplace (drift-detect, deslop, skillers, repo-intel, audit-project, etc). Deep-dived marketplace.json: validates our evolve/feedback-learner/watcher approach. CI vs plugin ecosystem mismatch. JavaScript. Active development.

### shinpr/claude-code-workflows
- **Why:** Production-ready multi-agent workflows (257 stars, 44 forks) — specialized agents (technical-designer, document-reviewer, work-planner)
- **Look for:** Multi-agent workflow organization, dependency verification patterns, role-based agent coordination
- **Added:** 2026-03-29 (horizon scan) | **Observations:** 13 | **First seen:** 2026-03-29 | **SHA:** a625676
- **Notes:** PR #91 (Mar 29): dependency existence verification for design workflow (3-case: found/external/needs-creation). PR #89: recipe isolation (removed recipe-to-recipe deps). Deep-dived: dependency verification interesting but marginal for coder.yml. Specialized agents with role assignments. Markdown-only. Active.

### Vigilant-LLC/runner-guard
- **Why:** CI/CD security scanner (6 stars, Go) — 18 detection rules for GHA vulnerabilities: fork checkout exploits, expression injection, AI config injection (CLAUDE.md hijacking), supply chain steganography, unpinned actions, auto-fix, SARIF output
- **Look for:** GHA vulnerability patterns applicable to our workflows, action pinning auto-fix, AI config injection defenses, SARIF integration for Code Scanning
- **Added:** 2026-04-01 (horizon scan) | **Observations:** 4 | **First seen:** 2026-04-01 | **SHA:** 15a4f57
- **Notes:** Only scanner specifically targeting AI agent attack vectors in CI/CD. Deep-dived: 18 rules, GitHub Action with SARIF, AI config injection detection. Our feedback-learner.yml has low-risk expression injection (lines 104-108) that RGS-002/003 would flag. Issue #127 created for adoption. v2.5.2. Low stars (6) but unique niche. Go single binary.

### affaan-m/agentshield
- **Why:** AI agent security scanner (289 stars, 55 forks) — scans .claude/ for secrets, permission misconfigs, hook injection, MCP risks, prompt injection vectors. CLI + GitHub Action + GitHub App.
- **Look for:** Agent config audit rules applicable to our harness, CI integration patterns, auto-fix capabilities for security issues
- **Added:** 2026-04-01 (horizon scan) | **Observations:** 2 | **First seen:** 2026-04-01 | **SHA:** 6f1b5cc
- **Notes:** From affaan-m (everything-claude-code author). TypeScript. Covers agent config security surface (complementary to runner-guard which covers CI/CD workflow security). Detects hardcoded secrets, overly permissive permissions, hook injection. Built at Claude Code Hackathon. GitHub Action available. Part of ECC ecosystem (42K+ stars). Our .claude/ config is minimal so immediate value is low — monitor for CI integration patterns.

### jnurre64/claude-agent-dispatch
- **Why:** Label-driven Claude Code GHA dispatch (Shell, 2 stars) — closest architecture to tokenman. Modular agent-dispatch.sh + lib/, label state machine (10 agent:* labels), two-phase plan→implement with human checkpoint, ShellCheck + BATS-Core CI testing.
- **Look for:** Shell script quality patterns, label state machine design, worktree isolation, error trap handling, BATS test patterns
- **Added:** 2026-04-02 (horizon scan) | **Observations:** 3 | **First seen:** 2026-04-02 | **SHA:** c41eb1d
- **Notes:** Created 2026-03-21, actively maintained. Shell-only, no Node/Python deps. Reusable workflows (dispatch-*.yml) consumed via workflow_call. CI validates all scripts with ShellCheck + BATS. Architecturally closest to tokenman: issue-driven, label-based state, GHA runners, claude -p headless. Deep-dived architecture: scripts/lib/ (5 modules), BATS tests (6 files), global error trap with diagnostic comments, label state machine (10 labels), worktree stale prune. Issues: #129 (ShellCheck), #131 (dependabot), #139 (BATS testing). 2 pattern hits.

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
