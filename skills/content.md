---
name: content
description: >
  Use when reading, writing, or modifying content/ files: project cards,
  blog posts, profile.json, or llms.txt. Also use when working with
  Astro content collections, frontmatter schemas, or understanding
  how content flows from files to the rendered profile page.
---

# Content Management

## Content Collections

### content/projects/{slug}.md
One file per GitHub repository. Agent writes and updates these.

Required frontmatter (see src/content.config.ts for full schema):
```yaml
---
title: Project Name
status: active | maintained | archived | experiment
description: One sentence. What it does and why it matters.
longDescription: 2-3 sentences from README. Optional.
url: https://live-demo.com  # optional
github: https://github.com/user/repo  # required
stars: 0                    # synced daily by maintenance.yml
language: TypeScript         # primary language
tags: [mcp, typescript, aws] # from GitHub topics
featured: false              # owner sets this manually
agent_written: true
last_synced: 2026-03-20
---

Optional markdown body with more detail.
```

### content/posts/{slug}.md
Blog posts synced from RSS. Agent writes these.

Required frontmatter:
```yaml
---
title: Post Title
description: One sentence summary
published: 2026-03-15      # ISO date from RSS
url: https://blog.com/post # link to original
source: My Blog            # blog name
agent_synced: true
---
```

### content/profile.json
The single source of truth for profile data. Agent reads and updates.

```json
{
  "name": "Full Name",
  "username": "github-username",
  "role": "What you do",
  "bio": "1-2 sentences. Shown on profile.",
  "location": "City, Country",
  "site_url": "https://yourdomain.com",
  "availability": "open | busy | closed",
  "availability_note": "Short status message",
  "github": "https://github.com/username",
  "blog": "https://blog.com",
  "links": [{"label": "Twitter", "url": "https://..."}],
  "skills": ["MCP", "Agent Harness", "TypeScript"],
  "languages": ["TypeScript", "Python", "Go"],
  "last_updated": "2026-03-20T14:32:00Z",
  "updated_by": "agent"
}
```

### content/llms.txt
Plain text, structured for AI consumption. Served at /llms.txt.
Update whenever profile.json changes significantly.

## How Content Reaches the Page

1. Agent writes/updates content/ files
2. Workflow commits the changes
3. deploy.yml fires on push to main
4. Astro reads content/ at BUILD TIME via getCollection()
5. Static HTML generated and deployed to Pages
6. Visitors see the updated content

There is no CMS dashboard. Files ARE the CMS.

## Writing Good Project Descriptions

Good description (1 sentence):
"MCP-native email middleware that routes agent-to-agent messages
through a managed inbox, eliminating direct API coupling."

Bad description:
"A cool project that does stuff with AI and email."

The description should answer: what does it do + who is it for?

## Syncing Stars from GitHub API

In maintenance.yml, stars are synced like this:
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
- llms.txt must stay plain text — no markdown syntax
- profile.json is valid JSON — no trailing commas, no comments
