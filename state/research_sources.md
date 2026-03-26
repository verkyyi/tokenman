# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-26T18:28:00Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-26T04:01 | **Pattern hits:** 1 | **SHA:** a0d9b87
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. v2.1.84 deep-dived: TaskCreated hook, `paths:` YAML glob frontmatter for skills/rules (relevant to #66), CLAUDE_STREAM_IDLE_TIMEOUT_MS idle watchdog, MCP 2KB description cap, allowedChannelPlugins managed setting, idle-return prompt (75min→/clear nudge). Many bug fixes including cold-start race, MCP cache leak. No breaking changes. Previous: v2.1.83 security patterns (#100), v2.1.81 --bare flag (#63).

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** New skill files, workflow patterns, agent guardrails, PR review techniques, structured output formats
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-26T09:28 | **Pattern hits:** 9 | **SHA:** 4f435e4
- **Notes:** Most productive source so far. 9 pattern hits across v0.9.7-v0.11.18.2. v0.11.19.0: Codex description 900-char guard test, -C flag for multi-workspace git root, proactive skill routing (workflow-stage suggestions). All Codex-specific or interactive-session. Pattern yield declining — 13th consecutive PH with 0 adoptable patterns from this source. SHA 997f7b1→4f435e4 (changed, not deep-dived).

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T13:32 | **Pattern hits:** 1 | **SHA:** 678fb6f
- **Notes:** Large community repo. 1 pattern hit (safety-guard PreToolUse hooks). SHA 401e26a→678fb6f: desktop-notify-hook (macOS, PR #846), ecc2 risk-scoring (Rust TUI, PR #888), ecc2 tool-logging (PR #887). All platform-specific or ecc2 TUI. 0 harness patterns across 7+ consecutive observations. Retaining for community skill discoveries but lowest deep-dive priority.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-26T09:28 | **Pattern hits:** 0 | **SHA:** 00fb183
- **Notes:** SHA a1c4015→00fb183 (changed, likely ticker). Confirmed ticker (16th+ consecutive content-free change). 0 pattern hits across 16+ observations. Low-value for PATTERN_HUNT; retain for HORIZON_SCAN cross-reference only.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Added:** 2026-03-21 (seed) | **Last deep:** 2026-03-26T09:28 | **Pattern hits:** 1 | **SHA:** e1853df
- **Notes:** Very active (5+ commits/day). GuardrailMiddleware covered by #67. ACP agent tool integration (auto_approve_permissions, harness/app split) — Python/LangGraph-specific. 0 harness patterns across 8+ consecutive deep-dives. Lowest deep-dive priority.

### wshobson/agents
- **Why:** Agent framework patterns — autonomous agent architectures
- **Look for:** Retry patterns, memory management, tool selection, agent lifecycle
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0
- **Notes:** 32K stars, 3504 forks. Plugin/skill catalog for Claude Code. SHA 1ad2f00 unchanged 16d+ (last commit Mar 10). 0 pattern hits. Drop candidate Apr 7 (4-week staleness threshold).

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0
- **Notes:** Check releases, not just commits. SHA 9728019 unchanged. v2.333.0 (Mar 18). 0 pattern hits across 8+ observations.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T17:12 | **Pattern hits:** 0 | **SHA:** 88fcc98
- **Notes:** Only actionable for security fixes or features that affect our site build. SHA 6683086→87fd6a4: Vite 8 warning + pin Vite 7 for Cloudflare adapter. Astro now has 5+ agent skills — validates #66 convention. 0 harness patterns across 10+ deep-dives. Monitor Vite 8 compatibility.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0 | **SHA:** 25d48db
- **Notes:** Used during HORIZON SCAN for adoption tracking. 0 forks, 0 adopters as of 2026-03-26.

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### thedotmack/claude-mem
- **Why:** Session memory plugin (40K stars) — auto-captures sessions, AI-compresses context, injects relevance-filtered memory into future sessions
- **Look for:** Compression strategies, relevance filtering, context injection patterns, memory lifecycle management
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 30 | **First seen:** 2026-03-23
- **Notes:** v10.6.2 active (Mar 21). SHA a656af2 unchanged (pushed today). Compress-filter-inject pipeline more sophisticated than our state/ read/write. Could improve project_state.md context management. 0 concrete patterns after 30 obs — fundamentally different approach.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 29 | **First seen:** 2026-03-23
- **Notes:** SHA 9df4731 unchanged (5th consecutive). 34+ plugins with formal SKILL.md standard. skill-improver quality loop. Codex compatibility layer. Pattern hit: SKILL.md quality standard (issue #68). Key reference for #66.

### sickn33/antigravity-awesome-skills
- **Why:** Largest skill catalog (27K stars, 1309+ skills) — installable via CLI, bundles, multi-platform (Claude Code, Codex, Gemini CLI, Cursor)
- **Look for:** Skill packaging/distribution model, CLI installer patterns, bundle organization, cross-platform skill format
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 36 | **First seen:** 2026-03-23
- **Notes:** SHA eaebf3e→367c4e0 (changed). NPX installer, bundles by role. Confirms direction of #66. 1326+ skills.

### OthmanAdi/planning-with-files
- **Why:** Persistent markdown planning skill (16.9K stars) — Manus-style file-based planning for Claude Code
- **Look for:** SKILL.md format, planning file structure, state persistence patterns, i18n skill variants
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 27 | **First seen:** 2026-03-23
- **Notes:** v2.29.0. SHA bb3a21a unchanged (5th consecutive). Validates markdown-as-memory, SKILL.md format with i18n. Active community (115+ PRs).

### SethGammon/Citadel
- **Why:** Agent orchestration harness (242 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks
- **Look for:** Circuit breaker implementation, quality gate patterns, campaign persistence, fleet coordination, lifecycle hooks
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 30 | **First seen:** 2026-03-24
- **Notes:** SHA 8d96785→fda6bab (changed — hook bug fixes: path quoting, backslash escaping). 1 pattern hit (circuit breaker #76). Informational for #66.

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 28 | **First seen:** 2026-03-24
- **Notes:** SHA b10b583 unchanged (6th consecutive). Standard plugin format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Distribution channel for #66. 1 pattern hit (official plugin format).

### vibeeval/vibecosystem
- **Why:** Comprehensive agent team (275 stars) — 119 agents, 208 skills, 49 hooks, 21 rules. Self-learning pattern where errors auto-become rules
- **Look for:** Self-learning implementation, session evaluation patterns, skill gateway for external catalogs, workflow routing
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 26 | **First seen:** 2026-03-24
- **Notes:** SHA 49840c2 unchanged (6th consecutive). 1 pattern hit (multi-agent review quality gate). Self-learning pattern similar to our feedback-learner. evaluate-session.sh for session outcomes.

### agent-sh/agnix
- **Why:** CLAUDE.md/SKILL.md linter and LSP (103 stars) — validates AI coding assistant config files, autofixes, IDE plugins
- **Look for:** Validation rules for CLAUDE.md, SKILL.md format standards, CI integration patterns, autofix capabilities
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 25 | **First seen:** 2026-03-24
- **Notes:** SHA 55adfcb unchanged (6th consecutive). Rust. v0.16.5 (Mar 23). Active development (675+ PRs). Could validate CLAUDE.md/SKILL.md in CI. 0 pattern hits.

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
