# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-23T21:47:50Z

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
- **Notes:** Most productive source so far. v0.9.7-v0.11.3 yielded adversarial review, structured tables, anti-sycophancy, pre-merge gate, security patterns. v0.9.9.1: cross-model outside voice (issue #64). v0.11.6.0: /cso v2 infrastructure-first security audit (covered by #17). v0.11.10.0: CI evals with parallel runners (no evals framework yet).

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Added:** 2026-03-20 (seed) | **Last deep:** 2026-03-23 | **Pattern hits:** 1
- **Notes:** Large community repo. skill-comply (behavioral compliance), santa-method (multi-agent adversarial verification), Kiro IDE integration — interesting but not immediately adoptable.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Good source for HORIZON SCAN cross-references.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Added:** 2026-03-21 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Active development. Enterprise-scale patterns may not be directly applicable but inform design.

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
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Check releases, not just commits. Dependency bumps are usually noise.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Only actionable for security fixes or features that affect our site build.

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
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 1 | **First seen:** 2026-03-23
- **Notes:** v10.6.2 active (Mar 21). Their compress-filter-inject pipeline is more sophisticated than our simple state/ read/write. Could improve how we manage project_state.md context.

### BloopAI/vibe-kanban
- **Why:** Agent management platform (24K stars) — PR-issue linking, multi-provider orchestration, kanban-style agent task management
- **Look for:** PR-issue linking automation, relay architecture, agent task queuing, multi-model coordination
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 2 | **First seen:** 2026-03-23
- **Notes:** v0.1.36+, very active (new SHA 83192b3, was fa00afc — confirmed ongoing dev). feat: link PRs to issues directly — interesting automation pattern. Rust+TS monorepo.

### trailofbits/skills
- **Why:** Security-focused Claude Code skills (4K stars) from top security firm — audit workflows, vulnerability detection, semgrep rules
- **Look for:** Security audit skill structure, semgrep rule patterns, skill-improver tooling, SKILL.md format conventions
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 1 | **First seen:** 2026-03-23
- **Notes:** Last commit Mar 17. Added Codex support (aab484c). skill-improver plugin, semgrep-rule-creator. Could inform our security posture and skill file format.

### sickn33/antigravity-awesome-skills
- **Why:** Largest skill catalog (27K stars, 1304+ skills) — installable via CLI, bundles, multi-platform (Claude Code, Codex, Gemini CLI, Cursor)
- **Look for:** Skill packaging/distribution model, CLI installer patterns, bundle organization, cross-platform skill format
- **Added:** 2026-03-23 (horizon scan) | **Observations:** 1 | **First seen:** 2026-03-23
- **Notes:** v8.7.1, very active (Mar 23). npm-based distribution. Massive catalog — useful for pattern discovery and understanding skill ecosystem conventions.

## Dropped Sources
<!-- Removed sources with reason. Kept for history so we don't re-discover them. -->

### godagoo/claude-code-always-on
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-02-03 (7+ weeks), no new patterns found

### humanlayer/humanlayer
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-01-07 (11+ weeks), no relevant patterns
