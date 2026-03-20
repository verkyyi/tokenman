---
name: content
description: >
  Use when reading, writing, or modifying content/ files for any project.
  Also use when working with Astro content collections, frontmatter schemas,
  or understanding how content flows from files to the rendered pages.
  Covers both scaffold-level content and per-project content management.
---

# Content Management

## Role of content/ in the Scaffold

The content/ folder is a file-based CMS. There is no dashboard.
Files ARE the CMS. The agent writes and updates them; Astro reads
them at build time via content collections.

Content can serve any project that Agentfolio manages. Each project
decides its own content structure by declaring collections in
src/content.config.ts.

## Content Collections

### content/projects/{slug}.md
One file per discovered repository or project. Agent writes and updates these.

Required frontmatter (see src/content.config.ts for full schema):
```yaml
---
title: Project Name
status: active | maintained | archived | experiment
description: One sentence. What it does and why it matters.
longDescription: 2-3 sentences from README. Optional.
url: https://live-demo.com  # optional
github: https://github.com/user/repo  # required
stars: 0                    # synced by analyze.yml
language: TypeScript         # primary language
tags: [mcp, typescript, aws] # from GitHub topics
featured: false              # owner sets this manually
agent_written: true
last_synced: 2026-03-20
---

Optional markdown body with more detail.
```

## Repo Profile Page

The repo profile page (src/pages/index.astro) is the scaffold's own
public face. It reads state files directly at build time using
`fs.readFileSync`, not via Astro content collections:

- `state/agent_log.md` — last agent action (powers the activity badge)
- `skills/*.md` — skill list rendered as capability tags
- `CLAUDE.md` — failure log section shown as transparency feed

This means the profile page reflects the scaffold's live state
automatically on every deploy — no separate content files needed.

## How Content Reaches the Page

1. Agent writes/updates content/ files
2. Workflow commits the changes
3. deploy.yml fires on push to main
4. Astro reads content/ at BUILD TIME via getCollection()
5. Static HTML generated and deployed to Pages
6. Visitors see the updated content

There is no runtime data fetching. All content is baked in at build time.

## Writing Good Project Descriptions

Good description (1 sentence):
"MCP-native email middleware that routes agent-to-agent messages
through a managed inbox, eliminating direct API coupling."

Bad description:
"A cool project that does stuff with AI and email."

The description should answer: what does it do + who is it for?

## Syncing Stars from GitHub API

In analyze.yml, stars are synced like this:
1. Fetch /repos/{owner}/{repo} from GitHub API
2. Read stargazers_count
3. Update frontmatter: stars: N
4. Update last_synced date

Always update last_synced when you touch a project file.

## Gotchas
- Astro rebuilds ALL pages on every deploy — static files only
- featured: true should be set by the owner, not the agent
  (unless specifically instructed)
- Do not delete project files — set status: archived instead
- Content collections only work inside Astro files (not .ts files)
- State files read via fs.readFileSync are NOT content collections —
  they are read directly from the filesystem at build time
