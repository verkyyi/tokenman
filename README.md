# Agentfolio

**A Claude Code scaffold for autonomous web projects.**
The repo is the system. Zero dedicated infrastructure.

[![Deploy](https://github.com/yourusername/agentfolio/actions/workflows/deploy.yml/badge.svg)](https://github.com/yourusername/agentfolio/actions/workflows/deploy.yml)

---

## What it is

Agentfolio is two things in one repo:

**1. The scaffold** — a harness of 7 GitHub Actions workflows that make any web project agent-powered. The agent triages feedback, fixes bugs, syncs content, audits SEO, and maintains itself. All triggered by GitHub events and cron. No server, no daemon, no database.

**2. The demo** — a living personal portfolio that runs inside the scaffold. Public profile + private activity log. Maintained by the agent. The git history is the proof of work.

---

## How it works

```
Your GitHub repos    → onboard.yml   → content/ files → Astro build → GitHub Pages
Visitor feedback     → GitHub Issue  → triage.yml    → coder.yml   → fix PR → merged
Push to main         → deploy.yml    → Astro build   → Pages live
Daily 3am            → maintenance.yml → sync repos, check links, GC
Weekly Monday        → growth.yml    → traffic report, SEO audit, drafts
Your instruction     → claude-task.yml → Claude acts → commit
```

---

## Quick start

**~5 minutes. No terminal required.**

1. Click **"Use this template"** → create repo
2. Settings → Secrets → Add `ANTHROPIC_API_KEY`
3. Settings → Pages → Source: GitHub Actions
4. Actions → "Onboard" → Run workflow → enter your GitHub username
5. Your profile is live at `yourusername.github.io/agentfolio`

Full guide: [docs/onboarding.md](docs/onboarding.md)

---

## The seven workflows

| Workflow | Trigger | What it does |
|---|---|---|
| `deploy.yml` | push to main | Astro build → GitHub Pages |
| `onboard.yml` | manual (once) | Fetches GitHub profile, writes all content |
| `triage.yml` | feedback issue opened | Classifies bug/ux/positive, labels |
| `coder.yml` | agent-ready label added | Implements fix, opens PR |
| `reviewer.yml` | agent PR opened | Reviews diff, approves or flags |
| `maintenance.yml` | daily 3am UTC | Sync repos, fix broken links, GC |
| `growth.yml` | weekly Monday 6am UTC | Traffic report, SEO, drafts |
| `claude-task.yml` | manual (anytime) | Your dev channel — type any instruction |

---

## The living portfolio demo

The portfolio shipped inside this scaffold demonstrates every harness capability:

- **`/`** — Public profile. Projects, writing, skills, availability badge, agent badge.
- **`/api/profile.json`** — Structured JSON for agents querying your profile.
- **`/llms.txt`** — AI-readable plain text profile.
- **`state/growth_report.md`** — Weekly metrics snapshot.
- **`state/drafts/`** — Agent-written distribution content.

The "last updated by agent" badge on the profile reads `state/agent_log.md` at build time. The badge links to this repo's commit history — the visible proof of work.

---

## Using the plugin in your existing project

```bash
npx @agentfolio/plugin
```

Copies all 7 workflows, 6 skill files, and issue templates into your project. Bring your own Astro app. Create `apps/[your-app]/CLAUDE.md` and run `onboard.yml`.

---

## Philosophy

> The model is the agent. The code is the harness.

Every agent mistake becomes a line in `apps/portfolio/CLAUDE.md`. The constitution grows with the project. After 3 months, it's a compressed history of everything that went wrong and was fixed permanently.

The git log is the audit trail. The Issues tab is the event bus. The Actions tab is the dashboard. GitHub IS the infrastructure.

---

## References

Built on patterns from:
- [godagoo/claude-code-always-on](https://godagoo.github.io/claude-code-always-on/) — always-on Claude architecture
- [mitchellh.com — harness engineering](https://mitchellh.com/writing/my-ai-adoption-journey) — CLAUDE.md as failure log
- [Anthropic — Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — FEATURE_STATUS.md pattern
- [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) — hooks and skills patterns
- [humanlayer/12-factor-agents](https://github.com/humanlayer/humanlayer) — context firewall pattern

---

## License

MIT — fork it, adapt it, build on it.
