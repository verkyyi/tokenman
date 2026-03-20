# Agentfolio

**A self-evolving scaffold for autonomous web projects.**
The repo is the system. The scaffold's first project is itself.

---

## What it is

Agentfolio is a harness of GitHub Actions workflows that make any web project
agent-powered. The agent triages feedback, fixes bugs, discovers new projects,
and evolves its own workflows and skills over time.

No server. No daemon. No database. GitHub IS the infrastructure.

---

## How it works

```
Push to main         → deploy.yml    → Astro build    → Pages live
Feedback issue       → triage.yml   → classify       → labels
agent-ready label    → coder.yml    → implement fix  → PR
Agent PR opened      → reviewer.yml → review         → merge/flag
Daily 3am UTC        → evolve.yml   → self-evolution → improvements
Monday 6am UTC       → analyze.yml  → weekly review  → priorities
New app folder       → discover.yml → infer stack    → generate rules
Your instruction     → claude-task  → Claude acts    → commit
```

---

## The eight workflows

| Workflow | Trigger | What it does |
|---|---|---|
| `deploy.yml` | push to main | Astro build → GitHub Pages |
| `discover.yml` | manual / evolve trigger | Scans apps/, infers stack, generates CLAUDE.md |
| `triage.yml` | feedback issue opened | Classifies bug/ux/positive, labels |
| `coder.yml` | agent-ready label added | Implements fix, opens PR |
| `reviewer.yml` | agent PR opened | Reviews diff, approves or flags |
| `evolve.yml` | daily 3am UTC | Analyzes failures + research, proposes improvements |
| `analyze.yml` | weekly Monday 6am UTC | Strategic analysis, identifies patterns |
| `claude-task.yml` | manual (anytime) | Your dev channel — type any instruction |

---

## Self-evolution

The scaffold improves itself daily:

1. **Research** — checks reference repos and changelogs for new patterns
2. **Analyze** — reads its own failure log and action history
3. **Act** — auto-commits safe fixes, opens PRs for structural changes
4. **Learn** — every mistake becomes a rule that prevents recurrence

The agent cannot promote its own autonomy. Structural changes always need
human review. The git log is the audit trail.

---

## Quick start

1. Fork this repo
2. Settings → Secrets → Add `CLAUDE_CODE_OAUTH_TOKEN`
3. Settings → Pages → Source: GitHub Actions
4. Drop your project in `apps/your-project/`
5. Run the "Discover Project" workflow
6. The scaffold generates rules for your project and starts maintaining it

---

## Adding a project

Create a folder in `apps/` with your code. Run `discover.yml`. The agent will:
- Scan your files and infer the stack
- Generate `apps/your-project/CLAUDE.md` with tailored rules
- Generate `apps/your-project/FEATURE_STATUS.md`
- Open a PR for your review

Or create `apps/your-project/CLAUDE.md` manually — see `apps/scaffold/CLAUDE.md`
for the format.

---

## Philosophy

> The model is the agent. The code is the harness.

Every agent mistake becomes a line in the failure log. The constitution grows
with the project. The git log is the audit trail. The Issues tab is the event
bus. The Actions tab is the dashboard.

---

## References

Built on patterns from:
- [godagoo/claude-code-always-on](https://godagoo.github.io/claude-code-always-on/)
- [mitchellh.com — harness engineering](https://mitchellh.com/writing/my-ai-adoption-journey)
- [Anthropic — Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [humanlayer/12-factor-agents](https://github.com/humanlayer/humanlayer)

---

## License

MIT — fork it, adapt it, build on it.
