# Landing Page Redesign — Design Spec

**Date:** 2026-03-22
**Status:** Draft

## Goal

Replace the current self-referential agent dashboard with a clear, developer-tool-minimal landing page that explains what Agentfolio is and motivates users to adopt it on their own repo.

## Audience

Mix of three personas:
1. **Open-source maintainers** — want their project to self-evolve (auto-triage, auto-research, auto-deploy)
2. **Developers** — want an autonomous agent harness for any GitHub repo
3. **Personal site builders** — want an "agent-maintained" website

## Primary CTA

"Use Claude Code to apply our workflows to your repo." The onboarding path is: open Claude Code in your repo → paste a prompt → Claude applies the workflows.

## Design Principles

- **Mobile-first** — base styles target ~375px, wider layouts via `min-width` media queries
- **Developer-tool minimal** — clean, technical, GitHub-README-like (Turborepo, Biome)
- **Single-page scroll** — no routing, no navigation complexity
- **No dashboard** — remove all live stats, agent badge, GitHub API calls
- **No emojis** — monospace labels, text-only iconography

## Tech Stack

- Astro 4.16 (existing)
- Tailwind CSS (existing, expand usage)
- Static build → GitHub Pages (existing pipeline)
- No client-side JavaScript required (pure static)

## Page Structure

Six sections, top to bottom:

### 1. Hero (centered)

- "Agentfolio" as text wordmark (no image/logo)
- Tagline: "Self-evolving GitHub Actions for any repo"
- Subtitle: ~20 words — "11 workflows that research, triage, code, review, and deploy — autonomously. Add to your project with Claude Code."
- Primary CTA button: "Get Started" (anchor link to section 5)
- Secondary text link: "View on GitHub" (links to repo)
- Mobile: full-width, stacked buttons, generous vertical padding

### 2. What It Does

Four capabilities, each as a compact labeled row:

| Label | Description |
|-------|-------------|
| Evolve | Researches your ecosystem hourly, opens issues |
| Triage | Classifies and routes every new issue |
| Code + Review | Implements on branches, reviews its own PRs |
| Deploy | Builds and ships on merge |

- Desktop: 2x2 grid or single column — keep it compact
- Mobile: single column, each item is a row with bold label + description

### 3. How It Works

Horizontal pipeline visualization:

```
Evolve → Triage → Code → Review → Deploy
```

- Each step is a labeled node
- Connected by arrows or lines
- Desktop: horizontal flow
- Mobile: vertical stack with downward arrows
- Minimal decoration — just the flow

### 4. Use Cases

Three compact cards:

1. **Open-source project** — Auto-triage issues, research your ecosystem, ship fixes
2. **Personal website** — Content updates, self-healing deploys, zero maintenance
3. **Any GitHub repo** — Add autonomous CI to what you already have

- Desktop: 3-column row
- Mobile: single column, cards stack vertically

### 5. Get Started

The onboarding steps:

1. Open Claude Code in your repo
2. Tell Claude to apply Agentfolio workflows
3. Claude writes config, copies workflows
4. Push and enable GitHub Actions

Include a code block showing the Claude Code prompt/command. Code block scrolls horizontally on mobile if needed.

Best use cases to highlight:
- Public repos that deploy to GitHub Pages
- Open-source projects
- Personal profile websites

### 6. Footer

Single line: GitHub repo link | MIT license | "Built with Astro"

## What Gets Removed

Everything from the current page:
- Cosmic gradient background and glowing effects
- Live GitHub API stats (commits, issues, PRs)
- Live pipeline visualization with emojis
- "Latest Action" indicator
- Agent badge (fixed bottom-right corner)
- All client-side JavaScript (timestamp updates, API fetches)
- State file reads at build time

## Visual Direction

- Dark background (#0d1117 or similar GitHub-dark tone)
- Light text, high contrast
- System-ui font stack
- Monochrome with one accent color (green — GitHub's action color)
- Generous whitespace
- No gradients, no glowing effects, no animations
- Code blocks styled like GitHub's dark code blocks

## Mobile-First Implementation

- Base CSS targets narrow screens (~375px)
- Wider layouts activated via `min-width` media queries (640px, 768px, 1024px)
- No horizontal scrolling except code blocks
- Touch-friendly tap targets (minimum 44px)
- Buttons: full-width on mobile, inline on desktop
- Pipeline: vertical on mobile, horizontal on desktop
- Use case cards: stacked on mobile, row on desktop

## File Changes

- **Replace:** `src/pages/index.astro` — complete rewrite
- **Simplify:** `src/layouts/Base.astro` — remove agent badge, remove client-side JS
- **No new files needed** — single page, inline scoped styles via Tailwind
- **Remove:** any state/ file reads from the build

## Out of Scope

- Multi-page site or routing
- Documentation section
- Blog or changelog
- Search functionality
- Analytics or tracking
- Dark/light theme toggle (dark only)
