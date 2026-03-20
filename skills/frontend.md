---
name: frontend
description: >
  Use when modifying src/ files: Astro pages, components, layouts,
  or styles. Also use when working with Tailwind CSS classes,
  Astro content collections in pages, or debugging build issues.
---

# Frontend — Astro + Tailwind

## Stack
- Astro 4.x (static output mode)
- Tailwind CSS (utility classes only, no custom CSS files)
- No JavaScript framework (Astro islands not used in base scaffold)
- GitHub Pages deployment (static HTML/CSS only)

## Key Constraint: Static Only
No API routes that execute at runtime. No server-side rendering.
Everything is computed at BUILD TIME during `npm run build`.

This means:
- Content is read from files at build time (not runtime)
- Agent badge timestamp comes from state/agent_log.md (read at build)
- Skills list comes from skills/*.md (read at build via fs.readFileSync)
- Cannot fetch live data at page load time

## Repo Profile Page Structure

The scaffold exposes a single public page: src/pages/index.astro.
This is the repo's profile page — it shows the scaffold's own state.

It reads three sources at build time using `fs.readFileSync`:
1. `state/agent_log.md` — last pipe-delimited line → activity badge
2. `skills/*.md` — frontmatter name/description → capability grid
3. `CLAUDE.md` — failure log section → transparency feed

It does NOT use Astro content collections for its own data.
Content collections (content/projects/, etc.) are for project content.

## File Structure
```
src/
  layouts/
    Base.astro         ← HTML shell, meta tags, agent badge
  pages/
    index.astro        ← repo profile page (reads state/ via fs)
    projects/
      [slug].astro     ← individual project pages (uses getCollection)
  components/
    (add as needed)
  content.config.ts    ← collection schemas
```

## Astro Component Pattern
```astro
---
// Frontmatter = TypeScript, runs at BUILD TIME only
import { readFileSync } from 'fs';
import { join } from 'path';
import Base from '../layouts/Base.astro';

// Read state files directly — not via content collections
const agentLog = readFileSync(join(process.cwd(), 'state/agent_log.md'), 'utf-8');
const lastLine = agentLog.trim().split('\n').at(-1) ?? '';
---

<!-- Template = HTML with Astro expressions -->
<Base>
  <p>Last agent action: {lastLine}</p>
</Base>
```

## Reading Content Collections in Pages
```astro
---
import { getCollection } from 'astro:content';

// Get all items in a collection
const projects = await getCollection('projects');

// Filter
const active = projects.filter(p => p.data.status === 'active');

// Sort by stars
const sorted = projects.sort((a, b) => b.data.stars - a.data.stars);

// Render markdown content (for pages with body)
const { Content } = await project.render();
---

<Content />
```

## Reading Files at Build Time
```astro
---
import { readFileSync } from 'fs';
import { join } from 'path';

// Always use join(process.cwd(), ...) for reliable paths
const raw = readFileSync(join(process.cwd(), 'state/agent_log.md'), 'utf-8');
---
```

## Tailwind Conventions
- Use utility classes directly in templates (no @apply)
- Color palette: gray-* for text, specific colors for status badges
- Spacing: consistent 6 (24px) horizontal padding on main
- Max width: max-w-2xl for content (readable line length)
- Interactive: hover:text-* transition-colors for links

Status badge colors:
```
active:     bg-green-50 text-green-600 border-green-100
archived:   bg-gray-50 text-gray-400 border-gray-100
experiment: bg-blue-50 text-blue-600 border-blue-100
maintained: bg-yellow-50 text-yellow-600 border-yellow-100
```

## Build Command
```bash
npm run build
# Output: dist/
# Must succeed before any PR is opened
```

Common build failures:
- Missing required frontmatter fields → check src/content.config.ts schema
- Import path errors → use relative imports or @/ alias
- TypeScript errors → run npx tsc --noEmit first
- fs.readFileSync path errors → use join(process.cwd(), ...) not relative paths

## Gotchas
- Astro requires explicit .astro extension on imports
- Cannot use browser APIs (localStorage, etc.) in frontmatter
- getCollection() only works in Astro files, not .ts files
- readFileSync() with process.cwd() works in Astro frontmatter
- Static paths must be defined in getStaticPaths() for dynamic routes
- Client-side JS must be in <script> tags or explicit client: directives
- State files are read with fs, not getCollection — they are not in content/
