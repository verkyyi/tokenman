# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-27T18:24:00Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-27T09:27 | **Pattern hits:** 2 | **SHA:** f75b613
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. v2.1.85 deep-dived: conditional `if` field for hooks (permission rule syntax, reduces process spawning — issue #122), PreToolUse can satisfy AskUserQuestion (headless integrations), MCP OAuth RFC 9728, /compact fix, --worktree fix, ECONNRESET retry fix, memory leak fix. Previous: v2.1.84 TaskCreated hook + paths: frontmatter (#66), v2.1.83 security patterns (#100), v2.1.81 --bare flag (#63).

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T13:32 | **Pattern hits:** 1 | **SHA:** 8b6140d
- **Notes:** Large community repo. 1 pattern hit (safety-guard PreToolUse hooks). SHA cc60bf6→8b6140d: ajv runtime dependency fix (PR #956). All platform-specific or ecc2 TUI. 0 harness patterns across 7+ consecutive observations. Retaining for community skill discoveries but lowest deep-dive priority.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-26T09:28 | **Pattern hits:** 0 | **SHA:** 7f0aafc
- **Notes:** SHA 22d444f→7f0aafc (changed). 0 pattern hits across 20+ observations. Low-value for PATTERN_HUNT; retain for HORIZON_SCAN cross-reference only.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Added:** 2026-03-21 (seed) | **Last deep:** 2026-03-26T09:28 | **Pattern hits:** 1 | **SHA:** ca20b48
- **Notes:** Very active (5+ commits/day). SHA 03b144f→ca20b48 (changed). Skill frontmatter validation tests (PR #1309). Converges with Citadel V2 skill-lint pattern. 0 harness patterns across 9+ consecutive deep-dives. Lowest deep-dive priority.

### SethGammon/Citadel
- **Why:** Agent orchestration harness (354 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks, skill benchmarking
- **Look for:** Skill benchmarking patterns, skill linting, governance hooks, testing infrastructure, fleet coordination
- **Added:** 2026-03-24 (watch) | **Promoted:** 2026-03-27 (synthesis — 35 obs, closest architecture, V2 patterns) | **Last deep:** never | **Pattern hits:** 1 | **SHA:** 25c4755
- **Notes:** Promoted from Watch List. V2 released (PR #26): skill-bench.js (scenario-based benchmarks with static + execute modes), skill-lint.js (structural SKILL.md validator FAIL/WARN/INFO), governance.js (audit logging hook), __benchmarks__/ per-skill fixtures. 1 pattern hit (circuit breaker #76). Skill-lint pattern converges with deer-flow frontmatter validation tests — ecosystem-wide signal. Prioritize for next PATTERN_HUNT deep-dive.

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0 | **SHA:** f0c2286
- **Notes:** Check releases, not just commits. SHA 9728019→f0c2286 (changed). v2.333.0 (Mar 18). 0 pattern hits across 8+ observations.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T17:12 | **Pattern hits:** 0 | **SHA:** 6464425
- **Notes:** Only actionable for security fixes or features that affect our site build. SHA 4198232→6464425 (changed). 0 harness patterns across 10+ deep-dives. Monitor Vite 8 compatibility.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0 | **SHA:** 733efef
- **Notes:** Used during HORIZON SCAN for adoption tracking. 0 forks, 0 adopters as of 2026-03-27.

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** Non-Codex workflow patterns, CI-transferable techniques
- **Demoted:** 2026-03-27 (synthesis — 14 consecutive PH with 0 adoptable patterns, all Codex/interactive-session specific)
- **Observations:** 35+ | **First seen:** 2026-03-20 | **SHA:** 11695e3
- **Notes:** Historically most productive source (9 pattern hits across v0.9.7-v0.11.18.2). Demoted because pattern yield exhausted for CI-based harness — all recent changes Codex/interactive-session specific. Monitor for CI-relevant patterns. Re-promote if non-Codex patterns emerge.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 34 | **First seen:** 2026-03-23 | **SHA:** 4b9a4e9
- **Notes:** 34+ plugins with formal SKILL.md standard. skill-improver quality loop. Codex compatibility layer. 1 pattern hit: SKILL.md quality standard (issue #68). Key reference for #66. SHA unchanged.

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 33 | **First seen:** 2026-03-24 | **SHA:** 451c481
- **Notes:** SHA 72b9754→451c481 (changed). Standard plugin format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Distribution channel for #66. 1 pattern hit (official plugin format).

### agent-sh/agnix
- **Why:** CLAUDE.md/SKILL.md linter and LSP (103 stars) — validates AI coding assistant config files, autofixes, IDE plugins
- **Look for:** Validation rules for CLAUDE.md, SKILL.md format standards, CI integration patterns, autofix capabilities
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 30 | **First seen:** 2026-03-24 | **SHA:** 98c5c53
- **Notes:** SHA d6e0a48→98c5c53 (changed). Rust. Active development (676+ PRs). Could validate CLAUDE.md/SKILL.md in CI. 0 pattern hits. Still active — retain for observation.

### code-yeongyu/oh-my-openagent
- **Why:** Largest agent harness repo (44K stars, 3273 forks) — TypeScript TUI, multi-model orchestration, subagent management, plugin discovery, hook isolation
- **Look for:** Hook isolation patterns, subagent lifecycle management, plugin discovery architecture, runtime fallback patterns
- **Added:** 2026-03-27 (horizon scan) | **Observations:** 3 | **First seen:** 2026-03-27 | **SHA:** 44b039b
- **Notes:** Very active (2800+ PRs, multiple commits/day). Architecture fundamentally different (interactive TUI vs CI workflows). Low direct adoption potential but large ecosystem influence. Monitor for transferable patterns.

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
