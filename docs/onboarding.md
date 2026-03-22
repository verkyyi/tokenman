# Agentfolio Onboarding

Add an autonomous dev pipeline to your existing GitHub repo. These instructions are designed to be followed by Claude Code — run them in a CLI session.

## Prerequisites

- Your repo is on GitHub with Actions enabled
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- A Claude Code OAuth token (`claude setup-token`)

## Steps

### 1. Copy workflow files

Clone the agentfolio repo and copy its workflow files into the target repo:

```bash
# In your target repo
git clone --depth=1 https://github.com/verkyyi/agentfolio.git /tmp/agentfolio
cp -r /tmp/agentfolio/.github/workflows/ .github/workflows/
cp -r /tmp/agentfolio/state/ state/
cp -r /tmp/agentfolio/skills/ skills/
mkdir -p apps/scaffold
cp /tmp/agentfolio/apps/scaffold/CLAUDE.md apps/scaffold/CLAUDE.md
cp /tmp/agentfolio/apps/scaffold/FEATURE_STATUS.md apps/scaffold/FEATURE_STATUS.md
cp /tmp/agentfolio/CLAUDE.md CLAUDE.md
rm -rf /tmp/agentfolio
```

### 2. Create project CLAUDE.md

Create `apps/<your-project>/CLAUDE.md` describing your project. This tells the agents what your project is, what rules to follow, and what autonomy they have. Example:

```markdown
# My Project

## What This Is
A brief description of your project.

## Autonomy
- The agent MAY commit directly to main for documentation and state changes.
- The agent MUST open a PR for any code changes.
- The agent MUST NOT delete files without confirmation.
```

### 3. Initialize state files

Reset state files to start fresh for your repo:

```bash
cat > state/project_state.md << 'EOF'
# Project State
Last updated: (will be written by first workflow run)
Updated by: (pending)

## Last Session
Action: Initial setup — agentfolio scaffold installed

## Open Items
(none yet — evolve.yml will populate on first run)
EOF

cat > state/agent_log.md << 'EOF'
# Agent Log
# Append-only. One line per agent action.
# Format: ISO_DATETIME | workflow | action | outcome

## Log

<!-- entries appended below by workflows -->
EOF

cat > state/research_log.md << 'EOF'
# Research Log
# Append-only. Written by evolve.yml during research phase.
# Format: ISO_TIMESTAMP | source | finding_summary | action_taken
EOF

cat > state/learned_rules.md << 'EOF'
# Learned Rules
# Rules learned from human feedback. Read by all workflows before acting.
# Add rules here and agents will follow them on every run.
EOF
```

### 4. Add the secret

Using the GitHub CLI:

```bash
# Generate a token if you haven't already
claude setup-token

# Add it to your repo (paste when prompted)
gh secret set CLAUDE_CODE_OAUTH_TOKEN
```

### 5. Enable GitHub Pages (optional)

If you want the auto-deploying profile site:

```bash
gh api repos/{owner}/{repo}/pages -X POST -f source='{"branch":"main","path":"/"}' 2>/dev/null || true
```

Or manually: Settings → Pages → Source: GitHub Actions.

### 6. Commit and push

```bash
git add .github/ state/ skills/ apps/ CLAUDE.md
git commit -m "feat: add agentfolio autonomous pipeline"
git push
```

The pipeline starts on the next hourly cron cycle. To start immediately:

```bash
gh workflow run evolve.yml
```

## What happens next

- `evolve.yml` runs hourly — researches improvements, checks pipeline health, creates issues
- `triage.yml` fires on new issues — labels and routes them
- `coder.yml` picks up `agent-ready` issues — writes code, opens PRs
- `reviewer.yml` reviews and merges PRs — closes linked issues
- `watcher.yml` runs every 30 min — self-heals broken chains
- `feedback-learner.yml` learns from human corrections — updates rules

Create an issue describing a change you want. Watch the pipeline handle it.

## Customization

Edit `CLAUDE.md` (harness rules) and `apps/<project>/CLAUDE.md` (project rules) to control agent behavior. Use MAY / MUST / MUST NOT to set boundaries. Changes take effect on the next workflow run.
