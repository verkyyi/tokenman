# Profile — Repo Profile Page Constitution
# Rules for the scaffold's public-facing profile page.
# Root harness rules live in the root CLAUDE.md.

## This Project
A live dashboard of the scaffold's own activity and capabilities.
Replaces the personal portfolio. Built with Astro, served from GitHub Pages.

Owner: autonomous (layout changes reviewed by human)
Scope: src/pages/index.astro, src/layouts/Base.astro, content/

## Content Sources
The profile page reads these files at BUILD TIME (no runtime fetches):
- state/agent_log.md → activity feed, commit stats
- state/research_log.md → recent research findings
- skills/*.md → capabilities inventory
- CLAUDE.md failure log → "mistakes it won't make again"

## Content Rules

AUTO — agent updates without asking:
- Stat regeneration from agent_log.md
- Activity feed updates
- Capabilities list sync from skills/

NEEDS APPROVAL (PR with label: needs-review):
- Layout or structural changes to index.astro
- New sections added to the profile
- Hero tagline or copy changes
- Styling changes

NEVER auto-execute:
- Removing sections from the profile
- Changing the repo name or identity
- Adding external tracking or analytics

## Deploy
build: npm run build
output: dist/
pages: GitHub Pages via deploy.yml

## Failure Log
# Format: # DATE: what went wrong → what rule prevents it now
