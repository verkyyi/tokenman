# Onboarding Guide

A step-by-step walkthrough for setting up your autonomous project portfolio on agentfolio. For the high-level overview, see the [README](../README.md).

---

## Prerequisites

- A **GitHub account** with permissions to fork repositories and configure Actions
- An **Anthropic API key** (get one at [console.anthropic.com](https://console.anthropic.com))
- Basic familiarity with **GitHub Actions** (knowing how to trigger workflows and read logs is enough)

---

## Setup (5 Steps)

### 1. Fork the Repo

Fork [agentfolio](https://github.com/your-org/agentfolio) into your own GitHub account. This gives you a personal copy where the agents will run.

### 2. Add Your API Key to Repo Secrets

Go to **Settings → Secrets and variables → Actions** in your forked repo and add:

| Name | Value |
|------|-------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

### 3. Enable GitHub Pages

Go to **Settings → Pages** and set:

- **Source:** `GitHub Actions`

The portfolio site will be published automatically after the first successful workflow run.

### 4. Add Your Project

Create a directory for your project under `apps/`:

```
apps/
  your-project/
    CLAUDE.md          # Agent rules and autonomy settings
    project_state.md   # Auto-generated; tracks current goals and status
    agent_log.md       # Auto-generated; running log of agent actions
    research_log.md    # Auto-generated; external research findings
```

Start by creating `CLAUDE.md` with your project description and any constraints. The other state files will be created automatically when you run the first workflow.

### 5. Run the "Discover Project" Workflow

Go to **Actions → Discover Project** and trigger it manually. This bootstraps your project by analyzing the `CLAUDE.md` you wrote and generating initial state files.

---

## How It Works

Eight workflows keep your project portfolio up to date autonomously:

| Workflow | Trigger | What It Does |
|----------|---------|--------------|
| `discover.yml` | Manual | Bootstraps a new project; reads `CLAUDE.md`, creates initial state files |
| `plan.yml` | Daily / Manual | Generates or updates the project roadmap in `project_state.md` |
| `execute.yml` | Daily / Manual | Works on the current goal; commits code, docs, or content changes |
| `review.yml` | On PR | Reviews pull requests and leaves structured feedback |
| `research.yml` | Daily | Fetches external articles, papers, and trends; appends to `research_log.md` |
| `publish.yml` | On push to `main` | Rebuilds and deploys the Astro portfolio site to GitHub Pages |
| `evolve.yml` | Daily | Self-improvement loop (see below) |
| `health.yml` | Daily | Checks for stale goals, broken links, and missing state files |

---

## Understanding the Self-Evolution Loop

`evolve.yml` runs daily and closes the feedback loop:

1. **Analyze failures** — Scans recent Action run logs for errors and repeated failures.
2. **Fetch external research** — Pulls the latest entries from `research_log.md` as context.
3. **Propose improvements** — Asks Claude to suggest edits to workflows, prompts, or rules.
4. **Open a PR** — Changes land as a pull request for you to review before merging.

You stay in control: the agent proposes, you decide.

---

## Customizing Rules

Each project's behavior is governed by `apps/your-project/CLAUDE.md`. Edit this file to tune the agent:

```markdown
# My Project

## What This Is
A CLI tool for ...

## Autonomy
- The agent MAY commit directly to `main` for documentation changes.
- The agent MUST open a PR for any code changes.
- The agent MUST NOT modify files outside `apps/my-project/`.

## Style
- Use TypeScript with strict mode enabled.
- Prefer functional patterns over classes.
```

Key knobs:
- **MAY / MUST / MUST NOT** — set permission boundaries
- **Scope constraints** — limit which directories the agent can touch
- **Style guides** — enforce coding conventions without manual review

---

## State Files

| File | Purpose |
|------|---------|
| `project_state.md` | Current goals, milestones, and project health summary. Updated by `plan.yml` and `execute.yml`. |
| `agent_log.md` | Chronological log of every action the agent took. Useful for auditing decisions. |
| `research_log.md` | Summaries of external research fetched by `research.yml`. Feeds into planning and evolution. |

These files live in your project directory and are committed to the repo, so the full history is in git.

---

## Monitoring

Watch what the agent is doing through three channels:

**Git log** — Every agent action produces a commit with a structured message:
```bash
git log --oneline apps/your-project/
```

**Actions tab** — See live workflow runs, logs, and any failures at `github.com/<you>/agentfolio/actions`.

**State files** — Read `agent_log.md` for a plain-English narrative of what happened and why:
```bash
cat apps/your-project/agent_log.md
```

If something looks wrong, edit `CLAUDE.md` to add a constraint and the agent will respect it on the next run.
