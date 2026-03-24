# Tokenman Skills

Reusable Claude Code skill patterns extracted from the Tokenman self-evolving agent harness.

## Standalone Skills (installable)

These skills are self-contained with no repo-specific dependencies. Each lives in its own directory with a `SKILL.md` file following the ecosystem standard format.

| Skill | Description | Install |
|-------|-------------|---------|
| [adversarial-review](./adversarial-review/) | Risk-tiered self-review protocol with pre-merge gate and cross-model outside voice | Copy `SKILL.md` to your project's skills directory |
| [session-protocol](./session-protocol/) | Start/stop state management for persistent agent context across sessions | Copy `SKILL.md` to your project's skills directory |
| [harness](./harness/) | Self-evolution loop architecture for autonomous agent systems | Copy `SKILL.md` to your project's skills directory |
| [feedback-intake](./feedback-intake/) | Convert unstructured user feedback into structured issue tracker entries | Copy `SKILL.md` to your project's skills directory |

## Project-Specific Skills

These skills contain Tokenman-specific references and are useful as templates but need adaptation for other projects.

| Skill | Description |
|-------|-------------|
| [content.md](./content.md) | Astro content collections and file-based CMS management |
| [frontend.md](./frontend.md) | Astro + Tailwind static site development patterns |
| [seo.md](./seo.md) | SEO, structured data, and AI discoverability |
| [github-workflows.md](./github-workflows.md) | GitHub Actions workflow patterns and API usage |
| [readme-sync.md](./readme-sync.md) | Automated README consistency with repo structure |

## Installation

### Manual (any project)

1. Copy the desired `SKILL.md` file into your project
2. Reference it from your `CLAUDE.md` or agent configuration
3. The skill's frontmatter (`name`, `description`, `tags`) is used by Claude Code for automatic activation

```bash
# Example: install adversarial-review
mkdir -p skills/adversarial-review
cp /path/to/tokenman/skills/adversarial-review/SKILL.md skills/adversarial-review/
```

### From GitHub (direct download)

```bash
# Download a single skill
mkdir -p skills/adversarial-review
curl -sL https://raw.githubusercontent.com/verkyyi/tokenman/main/skills/adversarial-review/SKILL.md \
  -o skills/adversarial-review/SKILL.md
```

### Compatible formats

These skills follow the SKILL.md convention used by the Claude Code ecosystem. They are compatible with:
- Direct file copy into any Claude Code project
- The [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) catalog format
- Any tool that reads YAML frontmatter metadata from skill files

## SKILL.md Format

Each skill uses YAML frontmatter for metadata:

```yaml
---
name: skill-name
version: 1.0.0
description: >
  What this skill does and when to activate it.
author: tokenman
tags: [tag1, tag2, tag3]
requires: []
preamble-tier: 2
---

# Skill Content

Instructions, protocols, and examples follow here.
```

## Preamble Tiers

The `preamble-tier` field controls how much context a workflow injects into its prompt. Lower tiers get less context, reducing token consumption for lightweight workflows.

| Tier | Context included | Assigned to |
|------|-----------------|-------------|
| T1 (minimal) | `learned_rules` + `evolve_config` | `feedback-intake` skill, feedback-learner workflow |
| T2 (standard) | T1 + `project_state` | `session-protocol`, `harness` skills; triage, reviewer workflows |
| T3 (extended) | T2 + full `CLAUDE.md` + project `CLAUDE.md` + `agent_log` | `adversarial-review` skill; coder, watcher workflows |
| T4 (full) | T3 + `research_sources` + `research_log` + `last_evolve_summary` | Evolve workflow |

Use `scripts/build-preamble.sh <tier>` to generate the context block for a given tier. See the script header for usage details.

## Community Catalogs

To register these skills in community catalogs:

- **antigravity-awesome-skills**: Submit a PR adding skill entries to the catalog
- **awesome-claude-code**: Submit when skills reach maturity

## License

These skills are part of the [Tokenman](https://github.com/verkyyi/tokenman) project and are available under the same license.
