# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-24T17:34:54Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-23 | **Pattern hits:** 1
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits. v2.1.81: --bare flag (issue #63).

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** New skill files, workflow patterns, agent guardrails, PR review techniques, structured output formats
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 8
- **Notes:** Most productive source so far. v0.9.7-v0.11.3 yielded adversarial review, structured tables, anti-sycophancy, pre-merge gate, security patterns. v0.9.9.1: cross-model outside voice (issue #64). v0.11.6.0: /cso v2 infrastructure-first security audit (covered by #17). v0.11.10.0: CI evals with parallel runners (no evals framework yet). v0.11.9.0: auto-heal stale installs + Codex 1024-char description guard (build-time validation, not issueworthy). v0.11.7.0: zsh glob compat + /review satisfies ship readiness gate. v0.11.12.0 (SHA dc5e053, PR #425): tiered preamble system (T1-T4) — skills pay for only needed context, ~40% token reduction for lightweight skills. WorktreeManager for E2E test isolation with SHA-256 dedup. Modular resolver arch. Token budget dashboard. Issue #83 (tiered preamble). v0.11.12.0 PR #424: triple-voice multi-model review with cascading context + consensus tables + degradation matrix (evolution of #64). PR #359 (v0.11.6.0): dynamic skill discovery (filesystem scan), three-dot scope drift (our reviewer already uses this), --local install flag. v0.11.15.0 (SHA 6156122, PR #449): E2E tests for skill output verification (plan-review-report, codex-offered), gen:skill-docs template regeneration. Strengthens #68 quality direction.

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 1
- **Notes:** Large community repo. skill-comply (behavioral compliance), santa-method (multi-agent adversarial verification), Kiro IDE integration — interesting but not immediately adoptable. v2026-03-23: 6 gap-closing skills (safety-guard, canary-watch, benchmark, browser-qa, design-system, product-lens). safety-guard uses PreToolUse hooks for multi-mode guardrails (supports #67). canary-watch has structured alert thresholds (critical/warning/info). Kiro hooks include extract-patterns (agentStop → auto-extract lessons) — similar to feedback-learner. 18 Kiro SKILL.md files added. SHA df4f2df→2166d80: ECC 2.0 Rust TUI agentic IDE scaffold (session manager, worktree orchestration, SQLite mailbox for inter-agent communication, risk scoring for tool calls). Competitive landscape, not harness patterns.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0
- **Notes:** Categories: Skills, Workflows, Tooling, Hooks, Slash-Commands, CLAUDE.md Files, Status Lines, Alternative Clients. Recent additions: parry (prompt injection scanner), RIPER workflow, ccpm (project management). Value is cross-reference for HORIZON SCAN, not direct patterns. SHA 15a1693 deep-dived: all commits are automated ticker/SVG updates, 0 actionable entries. SHA b200e72: ticker-only (6th consecutive).

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Added:** 2026-03-21 (seed) | **Last deep:** 2026-03-24T14:11 | **Pattern hits:** 1
- **Notes:** Very active (5+ commits/day). GuardrailMiddleware covered by #67. Deep-dived 2026-03-24T14:11: symlink-aware skill scanning (#1292, followlinks=True in os.walk for custom skills dir — relevant to future #66 but not adoptable now) + subprocess security fix (#1289, os.system→subprocess, Python-specific). Latest SHA: 067b19a (was 6bf5267, queue for next PH).

### wshobson/agents
- **Why:** Agent framework patterns — autonomous agent architectures
- **Look for:** Retry patterns, memory management, tool selection, agent lifecycle
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0
- **Notes:** 32K stars, 3504 forks. Plugin/skill catalog for Claude Code (OCI awareness, gallery-researcher, deployment engineer). 5 open PRs (Mar 19-22) including block-no-verify hook (already covered by CLAUDE.md). Primarily a plugin catalog, not harness architecture. Last commit Mar 17. Approaching staleness (7 days inactive, 0 hits).

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24 | **Pattern hits:** 0
- **Notes:** Check releases, not just commits. Dependency bumps are usually noise. v2.333.0 (Mar 18). DAP server added (debugging protocol) — not actionable for our harness. SHA e17e7aa→9728019 (eslint dep bump, noise).

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-24T14:11 | **Pattern hits:** 0
- **Notes:** Only actionable for security fixes or features that affect our site build. Deep-dived 2026-03-24T14:11: head propagation refactor (#15999), StaticHtml React optimization (#14917), server island crash fix (#16048). All framework internals, 0 harness patterns. Latest SHA: ba58e0d (was 7f43fba, queue for next PH).

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Used during HORIZON SCAN for adoption tracking.

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

### thedotmack/claude-mem
- **Why:** Session memory plugin (40K stars) — auto-captures sessions, AI-compresses context, injects relevance-filtered memory into future sessions
- **Look for:** Compression strategies, relevance filtering, context injection patterns, memory lifecycle management
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 9 | **First seen:** 2026-03-23
- **Notes:** v10.6.2 active (Mar 21). SHA e2a2302 unchanged. Their compress-filter-inject pipeline is more sophisticated than our simple state/ read/write. Could improve how we manage project_state.md context.

### BloopAI/vibe-kanban
- **Why:** Agent management platform (24K stars) — PR-issue linking, multi-provider orchestration, kanban-style agent task management
- **Look for:** PR-issue linking automation, relay architecture, agent task queuing, multi-model coordination
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 10 | **First seen:** 2026-03-23
- **Notes:** v0.1.36+, very active (SHA da45800, was 8a0e4c9 — continued active dev). feat: link PRs to issues directly — interesting automation pattern. Rust+TS monorepo.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 10 | **First seen:** 2026-03-23
- **Notes:** Last commit Mar 17 (SHA 5c15f4f unchanged). 34 plugins with formal SKILL.md standard: YAML frontmatter (name, description, allowed-tools), structured sections (When to Use, When NOT to Use, Rationalizations to Reject, Anti-Patterns, Strictness Level). skill-improver: automated quality loop (Review->Categorize->Fix->Evaluate->Repeat) with Critical/Major/Minor severity. Codex compatibility layer. Pattern hit: SKILL.md quality standard (issue #68).

### sickn33/antigravity-awesome-skills
- **Why:** Largest skill catalog (27K stars, 1309+ skills) — installable via CLI, bundles, multi-platform (Claude Code, Codex, Gemini CLI, Cursor)
- **Look for:** Skill packaging/distribution model, CLI installer patterns, bundle organization, cross-platform skill format
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 11 | **First seen:** 2026-03-23
- **Notes:** v8.7.1 (Mar 23), SHA 2e12db8 (was 8f5b56a). NPX installer (`npx antigravity-awesome-skills`) installs to target directory. Bundles by role (Web Wizard, Security Engineer, Essentials). Registry sync metadata in README. Confirms direction of #66. Distribution model: npm package + GitHub catalog + curated bundles.

### volcengine/OpenViking
- **Why:** Self-evolving context database (18.4K stars) — unified context management (memory, resources, skills) via file system paradigm, hierarchical context delivery
- **Look for:** "ov doctor" diagnostic patterns, loop memory optimization, context/memory/loop separation, self-evolving architecture
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 12 | **First seen:** 2026-03-23
- **Notes:** Very active (5+ commits/day). SHA 08b278d (was df8ba97). Deep-dived 2026-03-24T14:11: tool pruning (-229 lines from ov_file.py, #929), actionable 422 error helper (#928), embedding dimension validation (#930), uninstall script (#933). Tool pruning good hygiene but premature for our 8-skill set. 0 harness patterns. Previous: circuit breaker (#772) validates #76, config validation (#904), "ov doctor" (#851).

### OthmanAdi/planning-with-files
- **Why:** Persistent markdown planning skill (16.9K stars) — Manus-style file-based planning for Claude Code
- **Look for:** SKILL.md format, planning file structure, state persistence patterns, i18n skill variants
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 8 | **First seen:** 2026-03-23
- **Notes:** v2.28.0. SHA 3b6c3ce unchanged. Uses SKILL.md format with i18n variants (zh-TW). Validates our state/ markdown approach for persistent planning. Active community (113+ PRs).

### ruvnet/ruflo
- **Why:** Agent orchestration platform (24.2K stars, v3.5.42) — multi-agent swarms, hive-mind coordination, RAG, native Claude Code integration
- **Look for:** Hive-mind real status reporting, agent coordination patterns, security audit responses, MCP resilience
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 8 | **First seen:** 2026-03-23
- **Notes:** SHA 0590bf2 unchanged. "hive-mind_status reads real agent state instead of hardcoded values" — agents report actual status. Security audit: SQL injection fixes in 9 queries. MCP server self-kill prevention on startup.

### SethGammon/Citadel
- **Why:** Agent orchestration harness (242 stars) — closest architecture to tokenman. Campaign persistence, parallel worktrees, circuit breaker, quality gate hooks
- **Look for:** Circuit breaker implementation, quality gate patterns, campaign persistence, fleet coordination, lifecycle hooks
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 8 | **First seen:** 2026-03-24
- **Notes:** SHA 9da7c72. New: external-action-gate PreToolUse hook (blocks push/PR/issue unless allowed) + hook smoke test. 24 skills, 3 agents, 8 lifecycle hooks. PostToolUseFailure circuit breaker (3 failures → suggest alternative, 5 trips → hard stop). PreCompact/Restore-Compact for context preservation. Protect-files on Edit/Write. Pattern hit: circuit breaker (issue #76). External-action-gate covered by #67.

### anthropics/claude-plugins-official
- **Why:** Official Anthropic plugin directory (14.3K stars) — distribution channel for Claude Code plugins with standard format
- **Look for:** Plugin format updates, new submission requirements, plugin.json schema changes, new official plugins relevant to harness patterns
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 9 | **First seen:** 2026-03-24
- **Notes:** SHA 79caa0d. Inline buttons for Telegram/Discord permission approval (#945) — UI, not harness. Standard format: .claude-plugin/plugin.json + commands/ + agents/ + skills/. Installation via `/plugin install`. External submission form. 15+ external plugins, 30+ internal (code-review, security-guidance, skill-creator, hookify). Distribution channel for #66.

### vibeeval/vibecosystem
- **Why:** Comprehensive agent team (275 stars) — 119 agents, 208 skills, 49 hooks, 21 rules. Self-learning pattern where errors auto-become rules
- **Look for:** Self-learning implementation, session evaluation patterns, skill gateway for external catalogs, workflow routing
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 7 | **First seen:** 2026-03-24
- **Notes:** SHA b3e8890 unchanged. v1.2 released with Skill Gateway + Pyxel integration. evaluate-session.sh quantifies session outcomes. "One-question rule" for workflow routing. CI validation workflow. Self-learning pattern similar to our feedback-learner.

### agent-sh/agnix
- **Why:** CLAUDE.md/SKILL.md linter and LSP (103 stars) — validates AI coding assistant config files, autofixes, IDE plugins
- **Look for:** Validation rules for CLAUDE.md, SKILL.md format standards, CI integration patterns, autofix capabilities
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 6 | **First seen:** 2026-03-24
- **Notes:** SHA 55adfcb. Rust. v0.16.5 (Mar 23). Active development (675+ PRs). Could validate our CLAUDE.md and SKILL.md files in CI or pre-commit hooks. Supports multiple formats: CLAUDE.md, AGENTS.md, SKILL.md, hooks, MCP configs.

### intertwine/hive-orchestrator
- **Why:** Markdown-native agent orchestration (14 stars) — closest architecture to tokenman. Git-native, GitHub Actions, markdown shared memory
- **Look for:** Markdown-as-memory patterns, vendor-agnostic coordination, hybrid retrieval, skills directory structure
- **Added:** 2026-03-24 (horizon scan) | **Observations:** 7 | **First seen:** 2026-03-24
- **Notes:** SHA 51494de. Python. v2.3.1. Very active (5 commits this week). Deep-dived: hybrid dense retrieval with LanceDB + FastEmbed + reciprocal rank fusion (#162) — not adoptable (no retrieval layer). Canonical skills/ dir with symlinks to .agents/.claude/.opencode (#159) — validates our #66 packaging. Corpus fingerprint guard (SHA-256 skip when docs unchanged). Sandbox propagation (#161). Low stars but architecturally most similar to tokenman.

## Dropped Sources
<!-- Removed sources with reason. Kept for history so we don't re-discover them. -->

### VoltAgent/awesome-claude-code-subagents
- **Dropped:** 2026-03-24 | **Reason:** 0 pattern hits over 11+ observation runs and multiple deep-dives. Content is framework-specific experts (Rails, Expo, FastAPI) — not harness patterns.

### godagoo/claude-code-always-on
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-02-03 (7+ weeks), no new patterns found

### humanlayer/humanlayer
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-01-07 (11+ weeks), no relevant patterns
