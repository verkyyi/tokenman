# Feature Status
# Written by onboard.yml. Updated by coder.yml and reviewer.yml.
# Every feature starts as [ ] failing.
# The agent cannot declare a task "done" without updating this file.
# Checked [x] means: built AND tested in production.

## Public Profile

### Hero Section
- [ ] Name and role display correctly
- [ ] Bio renders from profile.json
- [ ] Availability badge shows correct status
- [ ] GitHub link works
- [ ] Agent badge shows last update time

### Projects Section
- [ ] Project cards render from content/projects/
- [ ] Stars count displays and is current
- [ ] GitHub link per project works
- [ ] Featured projects appear at top
- [ ] Status badge (active/archived) displays
- [ ] Tags render correctly
- [ ] Empty state handles zero projects

### Writing / Posts Section
- [ ] Posts render from content/posts/
- [ ] Links open to original post URL
- [ ] Date formatting correct
- [ ] Empty state handles no posts

### Skills Section
- [ ] Skills list renders from profile.json
- [ ] Languages list renders from profile.json

### Contact / Feedback
- [ ] Feedback link generates correct pre-filled issue URL
- [ ] Link opens GitHub issue template correctly
- [ ] Contact info visible

### SEO & Discovery
- [ ] Page title and meta description set correctly
- [ ] OG tags present and correct
- [ ] JSON-LD Person schema valid
- [ ] JSON-LD ItemList for projects valid
- [ ] sitemap.xml generated and reachable
- [ ] robots.txt present
- [ ] llms.txt reachable at /llms.txt
- [ ] /api/profile.json returns valid JSON
- [ ] Lighthouse performance score >= 90
- [ ] Lighthouse accessibility score >= 95

### Agent Badge
- [ ] Badge renders on profile page
- [ ] Timestamp reads from state/agent_log.md at build time
- [ ] Links to repo commits

## Autonomous Workflows

### onboard.yml
- [ ] Fetches GitHub user profile correctly
- [ ] Writes content/projects/ from repos
- [ ] Writes content/profile.json
- [ ] Writes apps/portfolio/CLAUDE.md
- [ ] Commits and triggers deploy

### triage.yml
- [ ] Fires on issues labeled 'feedback'
- [ ] Classifies: bug / ux-request / positive / spam
- [ ] Applies correct label
- [ ] Posts triage comment on issue
- [ ] Adds 'agent-ready' to bugs

### coder.yml
- [ ] Fires on issues labeled 'agent-ready'
- [ ] Reads issue body correctly
- [ ] Opens PR with fix
- [ ] Labels PR: auto-merge or needs-review
- [ ] Updates state/project_state.md

### reviewer.yml
- [ ] Fires on agent-opened PRs
- [ ] Classifies safe vs needs-review correctly
- [ ] Approves and enables auto-merge for safe PRs
- [ ] Requests review for flagged PRs

### maintenance.yml
- [ ] Runs daily at 3am UTC
- [ ] Syncs project data from GitHub API
- [ ] Runs link checker
- [ ] Opens issues for broken links
- [ ] Updates state/agent_log.md
- [ ] Commits state changes

### growth.yml
- [ ] Runs weekly Monday 6am UTC
- [ ] Reads GitHub Traffic API
- [ ] Writes state/growth_report.md
- [ ] Writes distribution drafts to state/drafts/
- [ ] Updates state/agent_log.md
