---
name: github-workflows
description: >
  Use when reading, writing, or debugging .github/workflows/ YAML files,
  understanding workflow triggers, using the GitHub API inside workflows,
  managing permissions, or understanding how GITHUB_TOKEN works.
  Also use when the agent needs to make GitHub API calls.
---

# GitHub Workflows & API

## GITHUB_TOKEN
Automatically injected into every workflow run. No setup needed.
Scopes depend on the permissions: block in the workflow YAML.

Common permission combinations:
```yaml
permissions:
  contents: write      # read/write repo files, commit, push
  issues: write        # create, label, comment, close issues
  pull-requests: write # create, review, merge PRs
  pages: write         # deploy to GitHub Pages
  id-token: write      # needed for Pages OIDC deployment
```

## GitHub API via curl
Always use Authorization header with GITHUB_TOKEN:
```bash
curl -s \
  -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/[endpoint]"
```

## Key Endpoints Used in Agentfolio

### User Profile
```bash
GET /users/{username}
# Returns: name, bio, location, blog, company, public_repos, etc.
```

### Repositories
```bash
GET /users/{username}/repos?sort=updated&per_page=100
# Returns: array of repos with stars, language, topics, etc.

GET /repos/{owner}/{repo}
# Single repo details

GET /repos/{owner}/{repo}/readme
# Returns: { content: base64_encoded_readme }
# Decode: base64 -d <<< "$CONTENT"

GET /repos/{owner}/{repo}/languages
# Returns: { TypeScript: 45231, CSS: 12034 }

GET /repos/{owner}/{repo}/topics
# Returns: { names: ["mcp", "typescript"] }

GET /repos/{owner}/{repo}/commits?per_page=5
# Returns: recent commits — used by evolve.yml to check reference repos
```

### Traffic (own repos only)
```bash
GET /repos/{owner}/{repo}/traffic/views
# Returns: { count: N, uniques: N, views: [...] }
# 14-day rolling window. Requires push access.

GET /repos/{owner}/{repo}/traffic/referrers
# Returns: top 10 referrers with counts

GET /repos/{owner}/{repo}/traffic/clones
# Returns: clone counts, 14-day window
```

### Issues & PRs (via gh CLI, simpler)
```bash
gh issue create --title "..." --label "..." --body "..."
gh issue edit N --add-label "..." --remove-label "..."
gh issue comment N --body "..."
gh issue close N

gh pr create --title "..." --body "..." --head branch --base main
gh pr merge N --auto --squash
gh pr edit N --add-label "..."
gh pr review N --approve --body "..."
```

## Workflow Triggers

### On push to main
```yaml
on:
  push:
    branches: [main]
```
Used by: deploy.yml

### On issue events
```yaml
on:
  issues:
    types: [opened, labeled]
# Access: github.event.issue.number, .title, .body, .labels
```
Used by: triage.yml, coder.yml

### On PR events
```yaml
on:
  pull_request:
    types: [opened, synchronize]
# Access: github.event.pull_request.number, .head.ref, .user.login
```
Used by: reviewer.yml

### Scheduled (cron)
```yaml
on:
  schedule:
    - cron: '0 3 * * *'  # 3am UTC daily (evolve.yml)
    - cron: '0 6 * * 1'  # 6am UTC Monday (analyze.yml)
```
Note: GitHub cron has ~15 min variance. Don't rely on exact timing.

### Manual dispatch with inputs
```yaml
on:
  workflow_dispatch:
    inputs:
      app_name:
        description: 'Target app in apps/ folder'
        required: false
        default: 'scaffold'
        type: string
```
Used by: discover.yml, claude-task.yml

## APP_NAME Dynamic Resolution
Workflows that need APP_NAME resolve it from context:

```yaml
# Issue/PR-triggered: extract from label
- name: Resolve APP_NAME
  id: app
  run: |
    APP=$(gh issue view ${{ github.event.issue.number }} \
      --json labels -q '.labels[].name' \
      | grep '^project:' | head -1 | sed 's/project://')
    echo "name=${APP:-scaffold}" >> "$GITHUB_OUTPUT"
```

```yaml
# Manual dispatch: use input directly
env:
  APP_NAME: ${{ github.event.inputs.app_name }}
```

```yaml
# Cron-triggered: iterate all apps/ folders
- name: List apps
  run: |
    for dir in apps/*/; do
      APP_NAME=$(basename "$dir")
      # ... process each app
    done
```

## Workflow Chaining Pattern
GITHUB_TOKEN cannot trigger other workflows directly.
Use `gh workflow run` for cross-workflow dispatch:

```bash
# evolve.yml triggering discover.yml when a new apps/ folder is found
gh workflow run discover.yml -f app_name="$APP"
```

Pattern used in evolve.yml:
1. Claude detects new apps/ folder without CLAUDE.md
2. Claude writes the folder name to .trigger-discovery.txt
3. Workflow step checks: `if: hashFiles('.trigger-discovery.txt') != ''`
4. Step runs: `gh workflow run discover.yml -f app_name="$(cat .trigger-discovery.txt)"`

## Conditional Execution
```yaml
# Only run if specific label was added
if: github.event.label.name == 'agent-ready'

# Only run for bot-authored PRs
if: github.event.pull_request.user.login == 'github-actions[bot]'

# Only on specific label
if: contains(github.event.issue.labels.*.name, 'feedback')

# Only if a file exists (used for conditional chaining)
if: hashFiles('.trigger-discovery.txt') != ''
```

## Passing Data Between Steps
```yaml
# Write to GITHUB_OUTPUT in one step
- id: my_step
  run: echo "MY_VAR=value" >> $GITHUB_OUTPUT

# Read in later step
- run: echo "Value is ${{ steps.my_step.outputs.MY_VAR }}"
```

## Multi-line Strings in GITHUB_OUTPUT
```bash
echo "CONTENT<<EOF" >> $GITHUB_OUTPUT
echo "line 1" >> $GITHUB_OUTPUT
echo "line 2" >> $GITHUB_OUTPUT
echo "EOF" >> $GITHUB_OUTPUT
```

## Gotchas
- GITHUB_TOKEN cannot trigger other workflow runs directly
  (use `gh workflow run` for chaining — e.g., evolve → discover)
- Workflow runs triggered by GITHUB_TOKEN don't trigger deploy.yml
  (that's why commits to main fire deploy — it's a push event)
- gh CLI is pre-installed on ubuntu-latest runners
- jq is pre-installed on ubuntu-latest runners
- node is NOT pre-installed — use actions/setup-node@v4
- Secrets are masked in logs — don't echo them
- concurrency groups prevent duplicate workflow runs
- Never modify .github/workflows/ files from inside a workflow run
