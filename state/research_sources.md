# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-29T06:34:46Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-27T09:27 | **Pattern hits:** 2 | **SHA:** 78a44f1
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. v2.1.87 (Mar 29): Cowork Dispatch message delivery fix (N/A to CI harness). v2.1.86 (Mar 27): plugin permission fix, memory growth fix, --resume fix, Session-Id header. Previous: v2.1.85 hook `if` field (#122), v2.1.84 paths: frontmatter (#66), v2.1.83 security patterns (#100), v2.1.81 --bare flag (#63).

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-29T06:34 | **Pattern hits:** 1 | **SHA:** 527c793
- **Notes:** Large community repo. 1 pattern hit (safety-guard PreToolUse hooks). PRs #998-#1000: Codex context7 compat, CLV2 config override, token-budget-advisor trigger. All Codex/CLV2-specific. 0 harness patterns across 10+ consecutive observations. Lowest deep-dive priority.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-28T03:54 | **Pattern hits:** 0 | **SHA:** ca3bf52
- **Notes:** SHA a511f96→b092ca6 (ticker data). 0 pattern hits across 26+ observations. Retain for HORIZON_SCAN cross-reference only.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Added:** 2026-03-21 (seed) | **Last deep:** 2026-03-28T15:14 | **Pattern hits:** 1 | **SHA:** 7eb3a15
- **Notes:** Very active (5+ commits/day). Latest: memory middleware thread_id fallback, channel assistant IDs, Docker fixes. All application-specific. 0 harness patterns across 11+ consecutive deep-dives. Lowest deep-dive priority.

### SethGammon/Citadel
- **Why:** Agent orchestration harness (354 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks, skill benchmarking
- **Look for:** Skill benchmarking patterns, skill linting, governance hooks, testing infrastructure, fleet coordination
- **Added:** 2026-03-24 (watch) | **Promoted:** 2026-03-27 (synthesis — 35 obs, closest architecture, V2 patterns) | **Last deep:** 2026-03-28T03:54 | **Pattern hits:** 1 | **SHA:** 82909b7
- **Notes:** Promoted from Watch List. SHA 2b3f87d→82909b7 (PR #59: three-pass health scan + repo cleanup, .planning/ directory). 21-hook ecosystem (V2). 1 pattern hit (circuit breaker #76). Rich reference for structured observability but low CI adoption potential.

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0 | **SHA:** f0c2286
- **Notes:** Check releases, not just commits. SHA 9728019→f0c2286 (changed). v2.333.0 (Mar 18). 0 pattern hits across 8+ observations.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T17:12 | **Pattern hits:** 0 | **SHA:** 0d24e3b
- **Notes:** Only actionable for security fixes or features that affect our site build. SHA 4198232→6464425 (changed). 0 harness patterns across 10+ deep-dives. Monitor Vite 8 compatibility.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0 | **SHA:** 2c72334
- **Notes:** Used during HORIZON SCAN for adoption tracking. 0 forks, 0 adopters as of 2026-03-29.

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** Non-Codex workflow patterns, CI-transferable techniques
- **Demoted:** 2026-03-27 (synthesis — 14 consecutive PH with 0 adoptable patterns, all Codex/interactive-session specific)
- **Observations:** 39+ | **First seen:** 2026-03-20 | **SHA:** ea7dbc9
- **Notes:** Historically most productive source (9 pattern hits across v0.9.7-v0.11.18.2). Demoted because pattern yield exhausted for CI-based harness. v0.13.4.0: prompt injection defense (XML framing, trust boundaries, command allowlist) — interesting security pattern but CI risk lower than interactive sessions, #17 covers domain. Monitor for CI-relevant patterns. Re-promote if non-Codex patterns emerge.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 34 | **First seen:** 2026-03-23 | **SHA:** 4b9a4e9
- **Notes:** 34+ plugins with formal SKILL.md standard. skill-improver quality loop. Codex compatibility layer. 1 pattern hit: SKILL.md quality standard (issue #68). Key reference for #66. SHA unchanged.

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 34 | **First seen:** 2026-03-24 | **SHA:** 183a6ca
- **Notes:** PR #1115: bash prefix for .sh hooks (fixes #993 permission denied). Validates our `bash scripts/...` approach. Version field added for cache invalidation. Standard plugin format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Distribution channel for #66. 1 pattern hit (official plugin format).

### agent-sh/agnix
- **Why:** CLAUDE.md/SKILL.md linter and LSP (103 stars) — validates AI coding assistant config files, autofixes, IDE plugins
- **Look for:** Validation rules for CLAUDE.md, SKILL.md format standards, CI integration patterns, autofix capabilities
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 35 | **First seen:** 2026-03-24 | **SHA:** 371142c
- **Notes:** v0.17.0 deep-dived: perf consolidation (11 JSON traversals→2 passes, copilot parse reduction, serde caching), 44 new rules, HTTP hook validation, 385 total rules, 124 auto-fixes. Architecture-specific optimizations, 0 CI-adoptable. Strongest promotion candidate — eligible Mar 31. Relevant to #66/#68. 0 pattern hits. Retain.

### code-yeongyu/oh-my-openagent
- **Why:** Largest agent harness repo (44K stars, 3273 forks) — TypeScript TUI, multi-model orchestration, subagent management, plugin discovery, hook isolation
- **Look for:** Hook isolation patterns, subagent lifecycle management, plugin discovery architecture, runtime fallback patterns
- **Added:** 2026-03-27 (horizon scan) | **Observations:** 9 | **First seen:** 2026-03-27 | **SHA:** 5a28ee1
- **Notes:** Very active (2900+ PRs, multiple commits/day). SHA 5d4e57c→5a28ee1. Architecture fundamentally different (interactive TUI vs CI workflows). Low direct adoption potential but large ecosystem influence. Monitor for transferable patterns.

## Dropped Sources
<!-- Removed sources with reason. Kept for history so we don't re-discover them. -->

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
