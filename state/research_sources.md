# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-27T12:21:00Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-27T09:27 | **Pattern hits:** 2 | **SHA:** f75b613
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. v2.1.85 deep-dived: conditional `if` field for hooks (permission rule syntax, reduces process spawning — issue #122), PreToolUse can satisfy AskUserQuestion (headless integrations), MCP OAuth RFC 9728, /compact fix, --worktree fix, ECONNRESET retry fix, memory leak fix. Previous: v2.1.84 TaskCreated hook + paths: frontmatter (#66), v2.1.83 security patterns (#100), v2.1.81 --bare flag (#63).

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** New skill files, workflow patterns, agent guardrails, PR review techniques, structured output formats
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-26T21:16 | **Pattern hits:** 9 | **SHA:** 5319b8a
- **Notes:** Most productive source so far. 9 pattern hits across v0.9.7-v0.11.18.2. SHA 3d52382→60061d0: changed. All recent patterns Codex/interactive-session specific. 14th consecutive PH with 0 adoptable patterns from this source. Pattern yield exhausted for our CI-based harness.

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T13:32 | **Pattern hits:** 1 | **SHA:** 8b6140d
- **Notes:** Large community repo. 1 pattern hit (safety-guard PreToolUse hooks). SHA cc60bf6→8b6140d: ajv runtime dependency fix (PR #956). All platform-specific or ecc2 TUI. 0 harness patterns across 7+ consecutive observations. Retaining for community skill discoveries but lowest deep-dive priority.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-26T09:28 | **Pattern hits:** 0 | **SHA:** 22d444f
- **Notes:** SHA 9e36346→22d444f (ticker update). 0 pattern hits across 20+ observations. Low-value for PATTERN_HUNT; retain for HORIZON_SCAN cross-reference only.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Added:** 2026-03-21 (seed) | **Last deep:** 2026-03-26T09:28 | **Pattern hits:** 1 | **SHA:** 50f50d7
- **Notes:** Very active (5+ commits/day). SHA 43a19f9→50f50d7: skill frontmatter validation tests (PR #1309). Converges with Citadel V2 skill-lint pattern. 0 harness patterns across 9+ consecutive deep-dives. Lowest deep-dive priority.

### wshobson/agents
- **Why:** Agent framework patterns — autonomous agent architectures, plugin evaluation
- **Look for:** Plugin eval framework, retry patterns, memory management, tool selection, agent lifecycle
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-27T09:27 | **Pattern hits:** 0 | **SHA:** 91fe43e
- **Notes:** 32K stars, 3504 forks. Deep-dived PR #464: PluginEval 3-layer quality framework (L1 static, L2 LLM judge, L3 Monte Carlo). 10 quality dimensions, anti-pattern detection, Elo ranking. 40+ skill improvements. Python/uv/Pydantic stack too heavy for our bash harness. Validates already-closed #66/#68. SKILL.md frontmatter + references/ dir pattern already adopted. 0 new adoptable patterns. Drop candidate Apr 14 if no new patterns emerge.

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0
- **Notes:** Check releases, not just commits. SHA 9728019 unchanged. v2.333.0 (Mar 18). 0 pattern hits across 8+ observations.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T17:12 | **Pattern hits:** 0 | **SHA:** efb2e4b
- **Notes:** Only actionable for security fixes or features that affect our site build. SHA 9117cac→efb2e4b: ts tests (#16102). 0 harness patterns across 10+ deep-dives. Monitor Vite 8 compatibility.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0 | **SHA:** 98e38ef
- **Notes:** Used during HORIZON SCAN for adoption tracking. 0 forks, 0 adopters as of 2026-03-27.

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### thedotmack/claude-mem
- **Why:** Session memory plugin (40K stars) — auto-captures sessions, AI-compresses context, injects relevance-filtered memory into future sessions
- **Look for:** Compression strategies, relevance filtering, context injection patterns, memory lifecycle management
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 35 | **First seen:** 2026-03-23
- **Notes:** v10.6.2 active (Mar 21). SHA a656af2 unchanged (11th consecutive). 0 concrete patterns after 35 obs — fundamentally different approach (compress-filter-inject vs state/ read/write). Strongest drop candidate at Mar 30 threshold.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 34 | **First seen:** 2026-03-23
- **Notes:** SHA 9df4731→4b9a4e9 (changed — aflpp env vars guide, dimensional analysis plugin). 34+ plugins with formal SKILL.md standard. skill-improver quality loop. Codex compatibility layer. Pattern hit: SKILL.md quality standard (issue #68). Key reference for #66.

### sickn33/antigravity-awesome-skills
- **Why:** Largest skill catalog (27K stars, 1309+ skills) — installable via CLI, bundles, multi-platform (Claude Code, Codex, Gemini CLI, Cursor)
- **Look for:** Skill packaging/distribution model, CLI installer patterns, bundle organization, cross-platform skill format
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 41 | **First seen:** 2026-03-23
- **Notes:** SHA 4c0cc5f→bafe144 (changed). v9.0.0 released (Mar 27): plugin distributions for Claude Code + Codex. 1,328+ skills. Confirms direction of #66. 0 harness patterns after 41 obs.

### OthmanAdi/planning-with-files
- **Why:** Persistent markdown planning skill (16.9K stars) — Manus-style file-based planning for Claude Code
- **Look for:** SKILL.md format, planning file structure, state persistence patterns, i18n skill variants
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 32 | **First seen:** 2026-03-23
- **Notes:** v2.29.0. SHA bb3a21a unchanged (10th consecutive). Validates markdown-as-memory, SKILL.md format with i18n. Active community (115+ PRs).

### SethGammon/Citadel
- **Why:** Agent orchestration harness (354 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks, skill benchmarking
- **Look for:** Skill benchmarking patterns, skill linting, governance hooks, testing infrastructure, fleet coordination
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 35 | **First seen:** 2026-03-24
- **Notes:** V2 released (PR #26): skill-bench.js (scenario-based benchmarks with static + execute modes), skill-lint.js (structural SKILL.md validator FAIL/WARN/INFO), governance.js (audit logging hook), __benchmarks__/ per-skill fixtures. 1 pattern hit (circuit breaker #76). Skill-lint pattern converges with deer-flow frontmatter validation tests — ecosystem-wide signal.

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 33 | **First seen:** 2026-03-24
- **Notes:** SHA 72b9754 unchanged (terraform plugin added via separate PR). Standard plugin format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Distribution channel for #66. 1 pattern hit (official plugin format).

### vibeeval/vibecosystem
- **Why:** Comprehensive agent team (275 stars) — 119 agents, 208 skills, 49 hooks, 21 rules. Self-learning pattern where errors auto-become rules
- **Look for:** Self-learning implementation, session evaluation patterns, skill gateway for external catalogs, workflow routing
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 31 | **First seen:** 2026-03-24
- **Notes:** SHA 49840c2 unchanged (11th consecutive). v2.0 released (134 agents, 246 skills, 53 hooks). 1 pattern hit (multi-agent review quality gate). Self-learning pattern similar to our feedback-learner.

### agent-sh/agnix
- **Why:** CLAUDE.md/SKILL.md linter and LSP (103 stars) — validates AI coding assistant config files, autofixes, IDE plugins
- **Look for:** Validation rules for CLAUDE.md, SKILL.md format standards, CI integration patterns, autofix capabilities
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 30 | **First seen:** 2026-03-24
- **Notes:** SHA d6e0a48 unchanged (deps bump, download URL fix). Rust. Active development (676+ PRs). Could validate CLAUDE.md/SKILL.md in CI. 0 pattern hits.

### code-yeongyu/oh-my-openagent
- **Why:** Largest agent harness repo (44K stars, 3273 forks) — TypeScript TUI, multi-model orchestration, subagent management, plugin discovery, hook isolation
- **Look for:** Hook isolation patterns, subagent lifecycle management, plugin discovery architecture, runtime fallback patterns
- **Added:** 2026-03-27 (horizon scan) | **Observations:** 1 | **First seen:** 2026-03-27
- **Notes:** Very active (2800+ PRs, multiple commits/day). Architecture fundamentally different (interactive TUI vs CI workflows). Low direct adoption potential but large ecosystem influence. Monitor for transferable patterns.

## Dropped Sources
<!-- Removed sources with reason. Kept for history so we don't re-discover them. -->

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
