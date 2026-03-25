# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-25T16:43:26Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T07:41 | **Pattern hits:** 1 | **SHA:** a542f1b
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. v2.1.83 fully deep-dived: managed-settings.d/ (modular policy fragments, not needed for single-project), CwdChanged/FileChanged hooks (reactive env mgmt), initialPrompt frontmatter (requires --agent mode, not -p), CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1, sandbox.failIfUnavailable — all security patterns covered by #100. SHA a542f1b is pre-release CHANGELOG for upcoming v2.1.84. Previous: v2.1.81 --bare flag (issue #63), --channels permission relay.

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** New skill files, workflow patterns, agent guardrails, PR review techniques, structured output formats
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T16:14 | **Pattern hits:** 9
- **Notes:** Most productive source so far. 9 pattern hits across v0.9.7-v0.11.18.2. Open PRs: #258 synthetic memory, #266 codebase-audit pipeline (737-line skill: audit→fix plan→review→implement with health scoring — interesting architecture but premature for 8-skill set), #416 community telemetry, #487 Copilot CLI host, #488 Revyl MCP, #490 findPort race condition. SHA 9870a4e unchanged. Pattern yield declining — PRs are mature engineering, not novel harness patterns.

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T13:32 | **Pattern hits:** 1 | **SHA:** 678fb6f
- **Notes:** Large community repo. 1 pattern hit (safety-guard PreToolUse hooks). SHA 401e26a→678fb6f: desktop-notify-hook (macOS, PR #846), ecc2 risk-scoring (Rust TUI, PR #888), ecc2 tool-logging (PR #887). All platform-specific or ecc2 TUI. 0 harness patterns across 7+ consecutive observations. Retaining for community skill discoveries but lowest deep-dive priority.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T07:41 | **Pattern hits:** 0 | **SHA:** 63d7605
- **Notes:** SHA 4fa8827→63d7605: ticker only (10th+ consecutive, 0 content changes). 0 pattern hits across 9+ observations. Low-value for PATTERN_HUNT; retain for HORIZON_SCAN cross-reference only.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Added:** 2026-03-21 (seed) | **Last deep:** 2026-03-25T05:13 | **Pattern hits:** 1
- **Notes:** Very active (5+ commits/day). GuardrailMiddleware covered by #67. SHA d7e5107→ac97dc6: new commits. 0 harness patterns across 6+ consecutive deep-dives. Python/LangGraph-specific — reduced deep-dive priority.

### wshobson/agents
- **Why:** Agent framework patterns — autonomous agent architectures
- **Look for:** Retry patterns, memory management, tool selection, agent lifecycle
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0
- **Notes:** 32K stars, 3504 forks. Plugin/skill catalog for Claude Code. SHA 1ad2f00 unchanged 15d+ (last commit Mar 10). 0 pattern hits. Drop candidate Apr 14 (4-week staleness threshold).

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0
- **Notes:** Check releases, not just commits. SHA 9728019 unchanged. v2.333.0 (Mar 18). 0 pattern hits across 8+ observations.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-25T16:14 | **Pattern hits:** 0 | **SHA:** 6683086
- **Notes:** Only actionable for security fixes or features that affect our site build. SHA ee3ab41→6683086: new commits. Astro now has 5 agent skills — validates #66 convention. 0 harness patterns across 9+ deep-dives.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0 | **SHA:** b8cf246
- **Notes:** Used during HORIZON SCAN for adoption tracking. 0 forks, 0 adopters as of 2026-03-25.

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### thedotmack/claude-mem
- **Why:** Session memory plugin (40K stars) — auto-captures sessions, AI-compresses context, injects relevance-filtered memory into future sessions
- **Look for:** Compression strategies, relevance filtering, context injection patterns, memory lifecycle management
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 22 | **First seen:** 2026-03-23
- **Notes:** v10.6.2 active (Mar 21). SHA e2a2302 unchanged. Their compress-filter-inject pipeline is more sophisticated than our simple state/ read/write. Could improve how we manage project_state.md context.

### BloopAI/vibe-kanban
- **Why:** Agent management platform (24K stars) — PR-issue linking, multi-provider orchestration, kanban-style agent task management
- **Look for:** PR-issue linking automation, relay architecture, agent task queuing, multi-model coordination
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 21 | **First seen:** 2026-03-23
- **Notes:** v0.1.36+, very active. SHA 1e0f6cf→76c818f. #3233 conversation turn navigation popover (UI). #3252 SHA pinning merged. Pattern hit: SHA pinning (covered by existing security issue).

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 21 | **First seen:** 2026-03-23
- **Notes:** SHA 5c15f4f→9df4731 (#132 dimensional analysis plugin). 34+ plugins with formal SKILL.md standard: YAML frontmatter (name, description, allowed-tools), structured sections (When to Use, When NOT to Use, Rationalizations to Reject, Anti-Patterns, Strictness Level). skill-improver: automated quality loop (Review->Categorize->Fix->Evaluate->Repeat) with Critical/Major/Minor severity. Codex compatibility layer. PR #123: cross-platform sidecar symlink distribution (.codex/skills/ backed by same plugin content, 61 symlinks via installer). Pattern hit: SKILL.md quality standard (issue #68).

### sickn33/antigravity-awesome-skills
- **Why:** Largest skill catalog (27K stars, 1309+ skills) — installable via CLI, bundles, multi-platform (Claude Code, Codex, Gemini CLI, Cursor)
- **Look for:** Skill packaging/distribution model, CLI installer patterns, bundle organization, cross-platform skill format
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 28 | **First seen:** 2026-03-23
- **Notes:** SHA b2f9600→0afb519. NPX installer, bundles by role. Confirms direction of #66.

### volcengine/OpenViking
- **Why:** Self-evolving context database (18.4K stars) — unified context management (memory, resources, skills) via file system paradigm, hierarchical context delivery
- **Look for:** "ov doctor" diagnostic patterns, loop memory optimization, context/memory/loop separation, self-evolving architecture
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 30 | **First seen:** 2026-03-23
- **Notes:** Very active. SHA 659b22c→d56d7d4. Circuit breaker validates #76. All recent: Python-specific. 0 harness patterns across 7+ observations.

### OthmanAdi/planning-with-files
- **Why:** Persistent markdown planning skill (16.9K stars) — Manus-style file-based planning for Claude Code
- **Look for:** SKILL.md format, planning file structure, state persistence patterns, i18n skill variants
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 19 | **First seen:** 2026-03-23
- **Notes:** v2.29.0. SHA bb3a21a unchanged. Deep-dived: #115 adds analytics workflow templates (analytics_findings.md + analytics_task_plan.md) with phase-gated tasks, WHAT/WHY/WHEN self-documenting comments, and init-session script integration. Validates our markdown-as-memory approach. Uses SKILL.md format with i18n variants (zh-TW). Active community (115+ PRs).

### ruvnet/ruflo
- **Why:** Agent orchestration platform (24.2K stars, v3.5.42) — multi-agent swarms, hive-mind coordination, RAG, native Claude Code integration
- **Look for:** Hive-mind real status reporting, agent coordination patterns, security audit responses, MCP resilience
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 19 | **First seen:** 2026-03-23
- **Notes:** SHA 0590bf2 unchanged. "hive-mind_status reads real agent state instead of hardcoded values" — agents report actual status. Security audit: SQL injection fixes in 9 queries. MCP server self-kill prevention on startup.

### SethGammon/Citadel
- **Why:** Agent orchestration harness (242 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks
- **Look for:** Circuit breaker implementation, quality gate patterns, campaign persistence, fleet coordination, lifecycle hooks
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 22 | **First seen:** 2026-03-24
- **Notes:** SHA 0778426→8d96785. 26 skills, 3 agents, 10 hooks. Pattern hit: circuit breaker (issue #76). Recent: #22 hook installer for CLAUDE_PLUGIN_ROOT bug, #23 hooks.json→hooks-template.json rename (env var doesn't expand). Plugin packaging workaround, informational for #66.

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 20 | **First seen:** 2026-03-24
- **Notes:** SHA b10b583 unchanged. Deep-dived 2026-03-25: iMessage channel plugin — first multi-channel with MCP integration, 808-line server, skills/access and skills/configure sub-skills. Bash-only permission preview UX (input_preview shown only for Bash, others get name+desc — constrained channel optimization). Flint plugin added (#974). Standard format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Installation via `/plugin install`. 15+ external plugins, 30+ internal. Distribution channel for #66. Pattern hit: 1 (official plugin format).

### vibeeval/vibecosystem
- **Why:** Comprehensive agent team (275 stars) — 119 agents, 208 skills, 49 hooks, 21 rules. Self-learning pattern where errors auto-become rules
- **Look for:** Self-learning implementation, session evaluation patterns, skill gateway for external catalogs, workflow routing
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 18 | **First seen:** 2026-03-24
- **Notes:** SHA d7e1fc5→57d9c66. v1.4 Web Intelligence Pack (2 agents, 9 skills, 3 MCP integrations — browser-agent, harvest, loop detection in maestro). Deep-dived 2026-03-25: v1.3 SaaS Skill Pack (6 new, 2 enriched — payment, auth, email, compliance, analytics, launch). "Security hardened after 3-agent parallel review (18 fixes applied)" — multi-agent quality gate for skill content. UPGRADING.md for version migration. v1.2 had Skill Gateway + Pyxel integration. evaluate-session.sh quantifies session outcomes. Self-learning pattern similar to our feedback-learner. Pattern hit: 1 (multi-agent review quality gate).

### agent-sh/agnix
- **Why:** CLAUDE.md/SKILL.md linter and LSP (103 stars) — validates AI coding assistant config files, autofixes, IDE plugins
- **Look for:** Validation rules for CLAUDE.md, SKILL.md format standards, CI integration patterns, autofix capabilities
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 17 | **First seen:** 2026-03-24
- **Notes:** SHA 55adfcb unchanged. Rust. v0.16.5 (Mar 23). Active development (675+ PRs). Could validate our CLAUDE.md and SKILL.md files in CI or pre-commit hooks. Supports multiple formats: CLAUDE.md, AGENTS.md, SKILL.md, hooks, MCP configs.

### intertwine/hive-orchestrator
- **Why:** Markdown-native agent orchestration (14 stars) — closest architecture to tokenman. Git-native, GitHub Actions, markdown shared memory
- **Look for:** Markdown-as-memory patterns, vendor-agnostic coordination, hybrid retrieval, skills directory structure
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 18 | **First seen:** 2026-03-24
- **Notes:** SHA 51494de unchanged. Python. v2.3.1. Very active (5 commits this week). Deep-dived: hybrid dense retrieval with LanceDB + FastEmbed + reciprocal rank fusion (#162) — not adoptable (no retrieval layer). Canonical skills/ dir with symlinks to .agents/.claude/.opencode (#159) — validates our #66 packaging. Corpus fingerprint guard (SHA-256 skip when docs unchanged). Sandbox propagation (#161). Low stars but architecturally most similar to tokenman.

## Dropped Sources
<!-- Removed sources with reason. Kept for history so we don't re-discover them. -->

### VoltAgent/awesome-claude-code-subagents
- **Dropped:** 2026-03-24 | **Reason:** 0 pattern hits over 11+ observation runs and multiple deep-dives. Content is framework-specific experts (Rails, Expo, FastAPI) — not harness patterns.

### godagoo/claude-code-always-on
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-02-03 (7+ weeks), no new patterns found

### humanlayer/humanlayer
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-01-07 (11+ weeks), no relevant patterns
