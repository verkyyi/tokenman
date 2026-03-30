# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-30T18:25:00Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-27T09:27 | **Pattern hits:** 2 | **SHA:** 78a44f1
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. SHA unchanged since v2.1.87 (Mar 29). v2.1.87: Cowork Dispatch fix (N/A). v2.1.86 (Mar 27): plugin permission fix, memory growth fix. Previous: v2.1.85 hook `if` field (#122), v2.1.84 paths: frontmatter (#66), v2.1.83 security patterns (#100). Agnix v0.17.0 spec tracking reveals CC now has 17 hook events (PostCompact, InstructionsLoaded, ConfigChange, CwdChanged, FileChanged, TaskCreated, WorktreeCreate, WorktreeRemove, Elicitation, ElicitationResult, StopFailure + original 6), HTTP hooks, once/async fields.

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-29T06:34 | **Pattern hits:** 1 | **SHA:** e68233c
- **Notes:** Large community repo. 1 pattern hit (safety-guard PreToolUse hooks). PR #833: gitagent format for cross-harness portability (agent.yaml/SOUL.md/RULES.md). All Codex/CLV2-specific or cross-platform distribution — 0 CI-harness patterns across 10+ consecutive observations. Lowest deep-dive priority.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-28T03:54 | **Pattern hits:** 0 | **SHA:** 4b3c275
- **Notes:** SHA 6612770→43610cb (ticker data only). 0 pattern hits across 30+ observations. Retain for HORIZON_SCAN cross-reference only.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Added:** 2026-03-21 (seed) | **Last deep:** 2026-03-28T15:14 | **Pattern hits:** 1 | **SHA:** 9e3d484
- **Notes:** Very active (5+ commits/day). SHA 9a55775→4bb3c10 (Docker build speedups, dev tooling). All application-specific. 0 harness patterns across 15+ consecutive deep-dives. Lowest deep-dive priority.

### SethGammon/Citadel
- **Why:** Agent orchestration harness (400 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks, skill benchmarking, daemon factory
- **Look for:** Skill benchmarking patterns, skill linting, governance hooks, testing infrastructure, fleet coordination, daemon factory patterns
- **Added:** 2026-03-24 (watch) | **Promoted:** 2026-03-27 (synthesis — 35 obs, closest architecture, V2 patterns) | **Last deep:** 2026-03-30T18:25 | **Pattern hits:** 1 | **SHA:** 8593c3a
- **Notes:** Promoted from Watch List. PR #67: real token telemetry from session JSONL (scripts/session-tokens.js), external pricing.json config, consent pattern (configurable external action policy with protected branches). Our simpler usage_log.md + CLAUDE.md autonomy rules approach sufficient. 1 pattern hit (circuit breaker #76).

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0 | **SHA:** b9275b5
- **Notes:** Check releases, not just commits. v2.333.1 (Mar 27): removed AllowCaseFunction feature flag only. 0 pattern hits across 9+ observations.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T17:12 | **Pattern hits:** 0 | **SHA:** 0f8a0d7
- **Notes:** Only actionable for security fixes or features that affect our site build. SHA 4198232→6464425 (changed). 0 harness patterns across 10+ deep-dives. Monitor Vite 8 compatibility.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0 | **SHA:** 44c6b8c
- **Notes:** Used during HORIZON SCAN for adoption tracking. 0 forks, 0 adopters as of 2026-03-29.

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** Non-Codex workflow patterns, CI-transferable techniques
- **Demoted:** 2026-03-27 (synthesis — 14 consecutive PH with 0 adoptable patterns, all Codex/interactive-session specific)
- **Observations:** 44+ | **First seen:** 2026-03-20 | **SHA:** 7911b7b
- **Notes:** Historically most productive source (9 pattern hits across v0.9.7-v0.11.18.2). Demoted because pattern yield exhausted for CI-based harness. v0.13.5.0: Factory Droid compat (multi-host generation). v0.13.4.0: prompt injection defense. CI risk lower than interactive sessions, #17 covers domain. Monitor for CI-relevant patterns.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 36 | **First seen:** 2026-03-23 | **SHA:** 4b9a4e9
- **Decision (2026-03-30):** RETAIN on Watch List. 35 obs, 7+ days, 1 pattern hit (SKILL.md standard → #68, closed). 4K stars, 362 forks, active (last commit Mar 27). Low pattern yield (1/35) — not promoting to Active. Actively maintained — not dropping. Serves as reference for future skill format work.
- **Notes:** 34+ plugins with formal SKILL.md standard. skill-improver quality loop. Codex compatibility layer. 1 pattern hit: SKILL.md quality standard (issue #68, closed). Key reference for skill format. SHA unchanged.

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 36 | **First seen:** 2026-03-24 | **SHA:** 183a6ca
- **Notes:** PR #1115: bash prefix for .sh hooks (fixes #993 permission denied). Validates our `bash scripts/...` approach. Version field added for cache invalidation. Standard plugin format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Distribution channel for #66. 1 pattern hit (official plugin format). SHA unchanged.

### agent-sh/agnix
- **Why:** CLAUDE.md/SKILL.md linter and LSP (103 stars) — validates AI coding assistant config files, autofixes, IDE plugins
- **Look for:** Validation rules for CLAUDE.md, SKILL.md format standards, CI integration patterns, autofix capabilities
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 38 | **First seen:** 2026-03-24 | **SHA:** 371142c
- **Notes:** Deep-dived v0.17.0 P0 fix: revealed CC now has 17 hook events (was 4), HTTP hook type, once/async fields, expanded agent schema (maxTurns, effort, background, isolation, mcpServers). 385 rules, 124 auto-fixes. Key CC spec tracker. Promotion candidate — eligible Mar 31. Relevant to #66/#68. 0 pattern hits (informational, not adoptable for CI). Retain.

### code-yeongyu/oh-my-openagent
- **Why:** Largest agent harness repo (44K stars, 3273 forks) — TypeScript TUI, multi-model orchestration, subagent management, plugin discovery, hook isolation
- **Look for:** Hook isolation patterns, subagent lifecycle management, plugin discovery architecture, runtime fallback patterns
- **Added:** 2026-03-27 (horizon scan) | **Observations:** 15 | **First seen:** 2026-03-27 | **SHA:** 7f36011
- **Notes:** Deep-dived PR #2931 (tmux session isolation — N/A CI), PR #2929 (rules-injector config gating — validates our separate-workflow isolation), PR #2912 (fallback matrix testing), PR #2919 (configurable TDD). Architecture fundamentally different (interactive TUI vs CI). Low direct adoption. 0 pattern hits.

### agent-sh/agentsys
- **Why:** Comprehensive plugin/agent/skill system (672 stars, 69 forks) from same org as agnix — 19 plugins, 47 agents, 39 skills
- **Look for:** Plugin marketplace patterns, repo-intel tooling, CI-transferable agent coordination, skill management architecture
- **Added:** 2026-03-29 (horizon scan) | **Observations:** 4 | **First seen:** 2026-03-29 | **SHA:** 94326af
- **Notes:** Same org as agnix (Watch List). v5.8.1 (Mar 28). 19-plugin marketplace (drift-detect, deslop, skillers, repo-intel, audit-project, etc). Deep-dived marketplace.json: validates our evolve/feedback-learner/watcher approach. CI vs plugin ecosystem mismatch. JavaScript. Active development.

### shinpr/claude-code-workflows
- **Why:** Production-ready multi-agent workflows (257 stars, 44 forks) — specialized agents (technical-designer, document-reviewer, work-planner)
- **Look for:** Multi-agent workflow organization, dependency verification patterns, role-based agent coordination
- **Added:** 2026-03-29 (horizon scan) | **Observations:** 4 | **First seen:** 2026-03-29 | **SHA:** f4d10db
- **Notes:** PR #91 (Mar 29): dependency existence verification for design workflow (3-case: found/external/needs-creation). PR #89: recipe isolation (removed recipe-to-recipe deps). Deep-dived: dependency verification interesting but marginal for coder.yml. Specialized agents with role assignments. Markdown-only. Active.

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
