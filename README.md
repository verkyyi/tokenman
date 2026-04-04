# Tokenman

**A self-evolving scaffold for autonomous web projects.**
The repo is the system. The scaffold's first project is itself.

[![Deploy](https://github.com/verkyyi/tokenman/actions/workflows/deploy.yml/badge.svg)](https://github.com/verkyyi/tokenman/actions/workflows/deploy.yml)
[![Self-Evolve](https://github.com/verkyyi/tokenman/actions/workflows/evolve.yml/badge.svg)](https://github.com/verkyyi/tokenman/actions/workflows/evolve.yml)
[![Pipeline Watcher](https://github.com/verkyyi/tokenman/actions/workflows/watcher.yml/badge.svg)](https://github.com/verkyyi/tokenman/actions/workflows/watcher.yml)

**[Live site](https://verkyyi.github.io/tokenman/)** · **[Agent log](https://github.com/verkyyi/tokenman/blob/main/state/agent_log.md)**

---

## What it is

Tokenman is a harness of GitHub Actions workflows that make any web project
fully autonomous. The agent researches improvements, triages issues, writes code,
reviews PRs, and deploys — all without human intervention.

No server. No daemon. No database. GitHub IS the infrastructure.

### Key features

- **Self-evolution every 3 hours** — researches 10 external sources across rotating tiers, creates issues for actionable improvements
- **Full autonomous pipeline** — evolve → triage → coder → reviewer → deploy, with explicit workflow chaining
- **Self-healing watcher** — monitors the pipeline every 2 hours, re-triggers broken chains, creates fix issues
- **Feedback learning loop** — human corrections are extracted into persistent rules that shape all future agent behavior
- **Blacklist policy** — agents can modify anything (including their own workflows) unless it's a hard block (secrets, infinite loops, build failures)
- **Smart triage** — elaborates vague issues into structured specs with acceptance criteria and affected files

---

## How it works

```
Every 3h            → evolve.yml   → research + ideas  → create issues
Issue created       → triage.yml   → classify + elaborate → label
agent-ready label   → coder.yml    → implement          → open PR
PR opened           → reviewer.yml → review + merge     → deploy
Every 2h            → watcher.yml  → health check       → self-heal
Human feedback      → feedback-learner.yml → extract lesson → permanent rule
Every 6 hours       → analyze.yml  → strategic review   → priorities
Your instruction    → claude-task  → Claude acts         → commit
```

Each link in the chain is an explicit `gh workflow run` call — no reliance on GitHub event propagation.

---

## Interacting with the pipeline

You can steer the agent at any time using these actions:

| Action | What happens |
|---|---|
| Comment on an issue | Feedback learner extracts lessons; if actionable, re-triggers coder |
| Close a PR without merging | Rejection detected — `agent-ready` re-added to linked issue, coder re-triggered with rejection context |
| Close an issue as "not planned" | Feedback learner records an AVOID rule — agent won't create similar issues |
| Write "Always do X" or "Never do Y" in a comment | Extracted as a permanent learned rule that shapes all future agent behavior |
| Add `agent-ready` label to an issue | Coder picks it up on next run |
| Run `claude-task.yml` manually | Your dev channel — type any instruction |

Human corrections compound. Say it once and the system remembers permanently.

---

## The fourteen workflows

| Workflow | Trigger | What it does |
|---|---|---|
| `evolve.yml` | Every 3 hours | Researches 10 repos (rotating tiers), tracks adopters, creates improvement issues |
| `triage.yml` | Issue opened / dispatched | Classifies, elaborates with acceptance criteria, routes to coder |
| `coder.yml` | agent-ready label / dispatched | Implements fix on feature branch, opens PR |
| `reviewer.yml` | PR opened / dispatched | Reviews code, runs build, merges or blocks |
| `watcher.yml` | Every 2 hours | Monitors pipeline health, re-triggers broken chains |
| `growth.yml` | Twice daily | Discovers distribution opportunities, creates releases, measures impact |
| `feedback-learner.yml` | Human comment/review | Extracts lasting lessons into learned rules |
| `deploy.yml` | Source files pushed to main | Astro build → GitHub Pages |
| `analyze.yml` | Every 6 hours | Strategic analysis of past activity |
| `discover.yml` | Manual dispatch | Scans apps/ folders, generates project CLAUDE.md |
| `claude-task.yml` | Manual dispatch | Your dev channel — type any instruction |
| `test-evolve.yml` | Issue event | Test Evolve |
| `sync-labels.yml` | Issue event | Sync Labels |
| `security-scan.yml` | PR event | Security Scan — Workflow YAML |

---

## Self-evolution

The scaffold improves itself continuously:

1. **Research** — checks Claude Code, gstack, trending repos, and 7 other sources every 3 hours
2. **Detect** — pipeline watcher catches failures and broken chains every 2 hours
3. **Act** — creates issues that flow through the full triage → code → review → deploy pipeline
4. **Learn** — every human correction becomes a permanent rule that shapes future behavior
5. **Heal** — watcher re-triggers stalled workflows, coder fixes pipeline bugs

The system can modify its own workflows, skills, and rules. Only hard blocks
(secrets in code, infinite loops, build failures) stop a merge.

---

## Quick start

1. Fork this repo
2. Settings → Secrets → Add `CLAUDE_CODE_OAUTH_TOKEN` ([get one](https://console.anthropic.com))
3. Settings → Pages → Source: GitHub Actions
4. Settings → Actions → General → Allow GitHub Actions to create and approve pull requests
5. The scaffold starts evolving itself immediately

---

## Adding a project

Create a folder in `apps/` with your code. Run `discover.yml`. The agent will:
- Scan your files and infer the stack
- Generate `apps/your-project/CLAUDE.md` with tailored rules
- Generate `apps/your-project/FEATURE_STATUS.md`
- Open a PR for your review

---

## Architecture

```
state/                    # Committed state (read/write every run)
├── project_state.md      # Current priorities (overwritten each run)
├── agent_log.md          # Append-only action log
├── research_log.md       # Append-only research findings
└── learned_rules.md      # Human feedback → permanent rules

apps/                     # Projects managed by the scaffold
├── scaffold/             # The scaffold manages itself
└── profile/              # Additional projects

.github/workflows/        # The fourteen autonomous workflows
skills/                   # Agent skill files (markdown prompts)
src/                      # Astro site source
```

---

## Philosophy

> The model is the agent. The code is the harness. The git log is the audit trail.

Every agent mistake becomes a learned rule. The constitution grows with the project.
The Issues tab is the event bus. The Actions tab is the dashboard.
Human corrections compound — say it once, never repeat it.

---

## Research sources

The evolve agent monitors external repos using a posture-based rotation across four modes: **PATTERN_HUNT** (deep-dive Active sources), **PIPELINE_WATCH** (CI health), **HORIZON_SCAN** (discover new repos), and **SYNTHESIS** (cross-reference findings). See [`state/research_sources.md`](state/research_sources.md) for the full, Claude-managed source portfolio.

**Active sources:** [anthropics/claude-code](https://github.com/anthropics/claude-code) · [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) · [SethGammon/Citadel](https://github.com/SethGammon/Citadel) · [actions/runner](https://github.com/actions/runner) · [withastro/astro](https://github.com/withastro/astro) · [verkyyi/tokenman](https://github.com/verkyyi/tokenman) (self)

Plus 12 repos on the **Watch List** under evaluation for promotion or removal.

---

## References

Built on patterns from:
- [garrytan/gstack](https://github.com/garrytan/gstack) — Garry Tan's Claude Code harness
- [godagoo/claude-code-always-on](https://godagoo.github.io/claude-code-always-on/)
- [mitchellh.com — harness engineering](https://mitchellh.com/writing/my-ai-adoption-journey)
- [Anthropic — Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [humanlayer/12-factor-agents](https://github.com/humanlayer/humanlayer)

---

## License

MIT — fork it, adapt it, build on it.
