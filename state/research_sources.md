# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-24T01:10:47Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-23 | **Pattern hits:** 1
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. v2.1.81: --bare flag (issue #63).

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** New skill files, workflow patterns, agent guardrails, PR review techniques, structured output formats
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-23 | **Pattern hits:** 7
- **Notes:** Most productive source so far. v0.9.7-v0.11.3 yielded adversarial review, structured tables, anti-sycophancy, pre-merge gate, security patterns. v0.9.9.1: cross-model outside voice (issue #64). v0.11.6.0: /cso v2 infrastructure-first security audit (covered by #17). v0.11.10.0: CI evals with parallel runners (no evals framework yet). v0.11.9.0: auto-heal stale installs + Codex 1024-char description guard (build-time validation, not issueworthy). v0.11.7.0: zsh glob compat + /review satisfies ship readiness gate.

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-23 | **Pattern hits:** 1
- **Notes:** Large community repo. skill-comply (behavioral compliance), santa-method (multi-agent adversarial verification), Kiro IDE integration — interesting but not immediately adoptable. v2026-03-23: 6 gap-closing skills (safety-guard, canary-watch, benchmark, browser-qa, design-system, product-lens). safety-guard uses PreToolUse hooks for multi-mode guardrails (supports #67). canary-watch has structured alert thresholds (critical/warning/info). Kiro hooks include extract-patterns (agentStop → auto-extract lessons) — similar to feedback-learner. 18 Kiro SKILL.md files added.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-23 | **Pattern hits:** 0
- **Notes:** Categories: Skills, Workflows, Tooling, Hooks, Slash-Commands, CLAUDE.md Files, Status Lines, Alternative Clients. Recent additions: parry (prompt injection scanner), RIPER workflow, ccpm (project management). Value is cross-reference for HORIZON SCAN, not direct patterns. Recent commits are automated ticker updates only.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Added:** 2026-03-21 (seed) | **Last deep:** 2026-03-23 | **Pattern hits:** 1
- **Notes:** Very active (5+ commits/day). GuardrailMiddleware: pre-tool-call authorization with pluggable providers (AllowlistProvider, OAP passport, custom class-path), fail-closed option, numbered middleware chain (11 positions). Covered by #67. Also: Cmd+K command palette, podcast TTS error handling, thread cleanup — not harness-relevant.

### wshobson/agents
- **Why:** Agent framework patterns — autonomous agent architectures
- **Look for:** Retry patterns, memory management, tool selection, agent lifecycle
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Monitor for novel agent architecture ideas.

### VoltAgent/awesome-claude-code-subagents
- **Why:** Subagent patterns and skill registry — how others structure agent delegation
- **Look for:** New subagent types, skill file formats, delegation patterns
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-23 | **Pattern hits:** 0
- **Notes:** Community-curated list of subagent implementations. Mostly framework-specific experts (Rails, Expo, FastAPI) — not harness patterns.

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0
- **Notes:** Check releases, not just commits. Dependency bumps are usually noise. v2.333.0 (Mar 18). DAP server added (debugging protocol) — not actionable for our harness.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0
- **Notes:** Only actionable for security fixes or features that affect our site build. View transition fix (skip when browser provides one) — Astro internals, not adoptable.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Used during HORIZON SCAN for adoption tracking.

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### thedotmack/claude-mem
- **Why:** Session memory plugin (39K stars) — auto-captures sessions, AI-compresses context, injects relevance-filtered memory into future sessions
- **Look for:** Compression strategies, relevance filtering, context injection patterns, memory lifecycle management
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 3 | **First seen:** 2026-03-23
- **Notes:** v10.6.2 active (Mar 21). SHA e2a2302 unchanged. Their compress-filter-inject pipeline is more sophisticated than our simple state/ read/write. Could improve how we manage project_state.md context.

### BloopAI/vibe-kanban
- **Why:** Agent management platform (24K stars) — PR-issue linking, multi-provider orchestration, kanban-style agent task management
- **Look for:** PR-issue linking automation, relay architecture, agent task queuing, multi-model coordination
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 4 | **First seen:** 2026-03-23
- **Notes:** v0.1.36+, very active (SHA 83192b3 unchanged, auth refresh grace window). feat: link PRs to issues directly — interesting automation pattern. Rust+TS monorepo.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 4 | **First seen:** 2026-03-23
- **Notes:** Last commit Mar 17 (SHA 5c15f4f unchanged). 34 plugins with formal SKILL.md standard: YAML frontmatter (name, description, allowed-tools), structured sections (When to Use, When NOT to Use, Rationalizations to Reject, Anti-Patterns, Strictness Level). skill-improver: automated quality loop (Review->Categorize->Fix->Evaluate->Repeat) with Critical/Major/Minor severity. Codex compatibility layer. Pattern hit: SKILL.md quality standard (issue #68).

### sickn33/antigravity-awesome-skills
- **Why:** Largest skill catalog (27K stars, 1309+ skills) — installable via CLI, bundles, multi-platform (Claude Code, Codex, Gemini CLI, Cursor)
- **Look for:** Skill packaging/distribution model, CLI installer patterns, bundle organization, cross-platform skill format
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 4 | **First seen:** 2026-03-23
- **Notes:** v8.7.1 (Mar 23), SHA d5e95a3 unchanged (repo state sync). NPX installer (`npx antigravity-awesome-skills`) installs to target directory. Bundles by role (Web Wizard, Security Engineer, Essentials). Registry sync metadata in README. Confirms direction of #66. Distribution model: npm package + GitHub catalog + curated bundles.

### volcengine/OpenViking
- **Why:** Self-evolving context database (18.4K stars) — unified context management (memory, resources, skills) via file system paradigm, hierarchical context delivery
- **Look for:** "ov doctor" diagnostic patterns, loop memory optimization, context/memory/loop separation, self-evolving architecture
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 2 | **First seen:** 2026-03-23
- **Notes:** Very active (5+ commits/day). SHA 50e1ff9. Python. Bot agent has context.py/loop.py/memory.py separation. "ov doctor" diagnostic command merged (#851). Multi-read tool and loop memory optimization (#895). Could inspire a /health skill for our harness.

### OthmanAdi/planning-with-files
- **Why:** Persistent markdown planning skill (16.9K stars) — Manus-style file-based planning for Claude Code
- **Look for:** SKILL.md format, planning file structure, state persistence patterns, i18n skill variants
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 2 | **First seen:** 2026-03-23
- **Notes:** v2.28.0. SHA 3b6c3ce unchanged. Uses SKILL.md format with i18n variants (zh-TW). Validates our state/ markdown approach for persistent planning. Active community (113+ PRs).

### ruvnet/ruflo
- **Why:** Agent orchestration platform (23.9K stars, v3.5.42) — multi-agent swarms, hive-mind coordination, RAG, native Claude Code integration
- **Look for:** Hive-mind real status reporting, agent coordination patterns, security audit responses, MCP resilience
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 2 | **First seen:** 2026-03-23
- **Notes:** SHA 0590bf2 unchanged. "hive-mind_status reads real agent state instead of hardcoded values" — agents report actual status. Security audit: SQL injection fixes in 9 queries. MCP server self-kill prevention on startup.

### SethGammon/Citadel
- **Why:** Agent orchestration harness (220 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks
- **Look for:** Circuit breaker implementation, quality gate patterns, campaign persistence, fleet coordination, lifecycle hooks
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 1 | **First seen:** 2026-03-24
- **Notes:** SHA 28da845. 24 skills, 3 agents, 8 lifecycle hooks. PostToolUseFailure circuit breaker (3 failures → suggest alternative, 5 trips → hard stop). PreCompact/Restore-Compact for context preservation. Protect-files on Edit/Write. Pattern hit: circuit breaker (issue #76).

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 1 | **First seen:** 2026-03-24
- **Notes:** Standard format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Installation via `/plugin install`. External submission form. 15+ external plugins, 30+ internal (code-review, security-guidance, skill-creator, hookify). Distribution channel for #66.

### vibeeval/vibecosystem
- **Why:** Comprehensive agent team (275 stars) — 119 agents, 208 skills, 49 hooks, 21 rules. Self-learning pattern where errors auto-become rules
- **Look for:** Self-learning implementation, session evaluation patterns, skill gateway for external catalogs, workflow routing
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 1 | **First seen:** 2026-03-24
- **Notes:** SHA b3e8890. v1.2 released with Skill Gateway + Pyxel integration. evaluate-session.sh quantifies session outcomes. "One-question rule" for workflow routing. CI validation workflow. Self-learning pattern similar to our feedback-learner.

## Dropped Sources
<!-- Removed sources with reason. Kept for history so we don't re-discover them. -->

### godagoo/claude-code-always-on
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-02-03 (7+ weeks), no new patterns found

### humanlayer/humanlayer
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-01-07 (11+ weeks), no relevant patterns
