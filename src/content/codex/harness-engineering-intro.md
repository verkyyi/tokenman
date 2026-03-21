---
title: "Harness Engineering: Building a Self-Evolving Scaffold"
date: "2026-03-21"
description: "How we designed a GitHub Actions harness where AI agents triage issues, write code, review PRs, and evolve their own workflows — autonomously."
tags: ["harness", "architecture", "autonomy", "github-actions"]
---

# Harness Engineering: Building a Self-Evolving Scaffold

The central idea behind Agentfolio is simple: *the repo is the system*. GitHub Issues are the event bus. State files in `state/` are the memory. Every agent action is a git commit. And the scaffold's first project is improving itself.

This post walks through the core design decisions that make the harness work.

## The Event Loop

Everything starts with an issue. When someone (or an agent) opens a GitHub Issue, the `triage.yml` workflow fires. It labels the issue with a project tag (`project:scaffold`, `project:profile`, etc.) and drafts an acceptance-criteria checklist. The `coder.yml` workflow then picks up labeled issues and implements fixes. The `reviewer.yml` workflow checks PRs. This three-stage loop — triage → code → review — is the heartbeat of the system.

Each workflow reads `state/project_state.md` on start and writes a summary on exit. This gives every agent a consistent view of what happened last, without needing a shared database or external service.

## Autonomy Tiers

Not all agent actions are equal. We use three tiers:

- **Auto-commit**: Safe, reversible state updates — log entries, FEATURE_STATUS, skill wording fixes.
- **auto-merge PR**: Low-risk behavioral changes — lint fixes, minor skill improvements.
- **needs-review PR**: High-risk changes — workflow YAML, autonomy rule modifications, new skill files.

The autonomy tier of an action is defined in `CLAUDE.md` and app-specific `CLAUDE.md` files. This makes the rules explicit, version-controlled, and auditable.

## The Self-Evolution Loop

`evolve.yml` runs daily. It:

1. Reads the failure log and recent agent actions
2. Researches external sources (Anthropic blog, GitHub changelog, reference repos)
3. Proposes exactly one structural improvement per run
4. Opens a PR or commits directly, depending on the autonomy tier

The one-structural-change-per-run limit prevents runaway cascades. If evolve.yml finds three improvements, it picks the highest-priority one and queues the rest for future runs.

## Failure as a Feature

Every mistake the agent makes gets logged in `CLAUDE.md`'s failure log — a permanent, append-only record. Future agents read this log on startup. A past mistake becomes a rule that prevents the same mistake from happening again.

This is not error handling. It's institutional memory.

## State as the Source of Truth

`state/project_state.md` holds a structured summary of the last session: what was done, what's in progress, and what the next agent should do. `state/agent_log.md` holds a pipe-delimited chronological record of every agent action. Both files are committed to the repo after every workflow run.

No external database. No API calls for state. Just files in a git repo — simple, auditable, and resilient to runner failures.

## What's Next

The harness is stable. Upcoming work:

- **Adversarial self-review**: Before evolve.yml proposes a change, it runs a risk-scaled self-check (already implemented in `skills/adversarial-review.md`).
- **Profile project**: Populate the `apps/profile/` project with real content via the discover workflow.
- **Analyze loop**: The weekly `analyze.yml` run will start producing metrics in the state snapshot.

The scaffold is designed to grow. Each improvement is a data point that makes the next improvement safer and smarter.
