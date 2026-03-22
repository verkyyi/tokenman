# Site Content Evaluation for All Site Types

Closes #43.

## Problem

Step 2b of evolve.yml (lines 129-148) skips entirely when the Evolve Config Stack does not include a frontend framework (Astro, Next.js, React, Vue). This means static HTML sites — like GitHub Pages portfolios — never receive content or design feedback, even when the agent could evaluate their HTML directly.

## Design

Replace the binary skip condition with a three-tier detection system based on information already present in the Evolve Config.

### Tier Detection

The agent reads the Evolve Config's `Stack` and `deploy` fields to determine which tier applies:

| Tier | Condition | Action |
|------|-----------|--------|
| **Framework site** | Stack includes Astro, Next.js, React, or Vue | Read framework-specific files (e.g., `src/pages/index.astro`, `src/layouts/Base.astro`). Evaluate design language, responsiveness, polish. This is the current behavior. |
| **Static HTML site** | `deploy` field mentions a web host (GitHub Pages, Netlify, Vercel, Cloudflare Pages) OR `index.html` exists in repo root | Find HTML files (`index.html`, `*.html` in root and common dirs). Evaluate content completeness, SEO basics, structure, responsiveness indicators. |
| **No web presence** | None of the above | Skip Step 2b entirely. |

### Evaluation Criteria by Tier

**Framework sites** (unchanged from current):
- Visual consistency, readability, responsiveness, polish, content presentation
- Design language evaluation (e.g., Cosmic theme for agentfolio)

**Static HTML sites** (new):
- Content completeness: bio/about, projects/work, contact info
- Site structure: root index links to subpages
- SEO basics: `<title>`, `<meta name="description">`, `<meta name="viewport">`
- Responsiveness indicators: viewport meta tag, media queries or responsive framework
- Content gaps prioritized over visual polish

**Both tiers share:** Content completeness and SEO basics evaluation. The difference is where the agent looks for files and whether it evaluates framework-specific design patterns.

### Action Rules

Same as current Step 2b:
- Minor fixes (missing meta tags, broken links, content typos): write directly
- Structural changes (new sections, layout overhaul): create a GitHub Issue via Step 5
- Respect existing autonomy rules in CLAUDE.md

## Affected Files

| File | Change |
|------|--------|
| `.github/workflows/evolve.yml` | Replace Step 2b prompt text (lines 129-148) with tiered evaluation |
| `docs/superpowers/specs/2026-03-22-generic-evolve-design.md` | Update line 126 to reflect new behavior |
| `docs/superpowers/plans/2026-03-22-generic-evolve-plan.md` | Update Step 4 conditional description |

## What This Does NOT Do

- Does not add new workflow steps or bash logic — only prompt text changes
- Does not change the Evolve Config format
- Does not evaluate non-web repos (CLI tools, libraries without a site)
- Does not change the action rules (what gets written vs. what becomes an issue)
