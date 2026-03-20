# Portfolio — Project Constitution
# Written by onboard.yml. You should review and customize.
# Scaffold-level harness rules live in the root CLAUDE.md.
# This file is loaded by every workflow as additional context.

## This Project
A living personal portfolio — public profile + proof-of-work showcase.
Maintained autonomously by the Agentfolio harness.

Owner: (set by onboard.yml)
GitHub: (set by onboard.yml)
Live URL: (set by onboard.yml)
Stack: Astro + Tailwind + GitHub Pages

## Content Rules

AUTO — agent updates without asking:
- Project stars synced from GitHub API
- Blog posts added when new RSS items found
- Broken links in content/ patched
- llms.txt updated when profile changes
- sitemap.xml regenerated on deploy

NEEDS APPROVAL (PR with label: needs-review):
- New project cards added to featured list
- Bio or hero copy changes
- Skills list modifications
- Availability status changes
- New sections added to profile

NEVER auto-execute:
- Deleting existing project cards
- Changing the profile name or identity
- Publishing draft content to external platforms

## Autonomy Overrides
# These override the scaffold defaults for this project specifically.

# Example: if you want skills to auto-update without review:
# skills_update: auto

# Example: if you always want featured projects to need review:
# featured_changes: needs-review

## Deploy
build: npm run build
output: dist/
pages: GitHub Pages via deploy.yml

## Failure Log
# Add a line every time the agent makes a mistake.
# Format: # DATE: what went wrong → what rule prevents it now
# (empty — grows with your project)
