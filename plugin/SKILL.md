---
name: agentfolio
description: >
  Install when you want to add autonomous agent infrastructure to
  any web project. Provides: 7 GitHub Actions workflows for autonomous
  development (triage, coder, reviewer, maintenance, growth, deploy,
  manual task), skill files for Astro/Tailwind/SEO/harness/content,
  GitHub Issue templates for feedback intake, and the root CLAUDE.md
  harness constitution. Works with any Astro or static-site project.
  After installing, create your own apps/[project]/CLAUDE.md with
  project-specific rules and run the onboard workflow.
---

# Agentfolio Plugin

Claude Code plugin that brings always-on autonomous agent infrastructure
to your web project using only GitHub Actions and GitHub Pages.
Zero dedicated infrastructure. Zero external services.

## What gets installed

### Workflows (.github/workflows/)
- deploy.yml       — push → Astro build → GitHub Pages
- onboard.yml      — one-time setup via workflow_dispatch
- triage.yml       — feedback issues → classify → label
- coder.yml        — agent-ready issues → implement → PR
- reviewer.yml     — agent PRs → review → auto-merge or flag
- maintenance.yml  — daily: content sync, link check, GC
- growth.yml       — weekly: traffic report, SEO audit, drafts
- claude-task.yml  — manual: workflow_dispatch dev channel

### Skills (skills/)
- harness.md       — harness architecture and patterns
- content.md       — content collections, profile.json, llms.txt
- frontend.md      — Astro + Tailwind patterns
- seo.md           — structured data, llms.txt, Lighthouse
- feedback-intake.md — parse feedback → GitHub Issue
- github-workflows.md — GitHub API, workflow patterns

### Issue Templates (.github/ISSUE_TEMPLATE/)
- feedback.yml     — pre-filled visitor feedback form
- config.yml       — disables blank issues

### Root files
- CLAUDE.md        — scaffold harness constitution
- state/           — state file templates

## Quick Start

1. Install plugin:
   /plugin install agentfolio

2. Create your app folder:
   mkdir -p apps/myapp
   # Create apps/myapp/CLAUDE.md with project-specific rules
   # Create apps/myapp/FEATURE_STATUS.md
   # Create apps/myapp/growth_goals.md

3. Set APP_NAME in your workflows:
   # Each workflow has: env: APP_NAME: portfolio
   # Change 'portfolio' to your app name

4. Add secret to your repo:
   # ANTHROPIC_API_KEY in Settings → Secrets → Actions

5. Run onboard.yml:
   # Actions → Onboard → Run workflow → enter your GitHub username

## Requirements
- GitHub repository (public or private)
- Anthropic API key (as repository secret)
- GitHub Pages enabled (Settings → Pages → Source: GitHub Actions)
- Astro project in your repository (or use the portfolio demo)

## Compatibility
- Works with any Astro project
- Workflows are generic — coder/reviewer/maintenance work for any content
- SEO skill targets Astro patterns but concepts apply to any static site

## Source
https://github.com/yourusername/agentfolio
