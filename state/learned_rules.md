# Learned Rules
# Append-only. Extracted from human feedback on PRs and issues.
# Every agent reads this file. Rules here override default behavior.
# Format: each rule is a ## heading with date, source, and the lesson.

# Rules below this line are added automatically by the feedback-learner workflow.

## QUALITY Adversarial self-review before submitting agent output
**Date:** 2026-03-21 | **Source:** issue #4: [evolve] Add adversarial self-review step to evolve.yml agent output

The evolve agent (and agents in general) should include an adversarial self-review step that critically challenges its own proposed changes before submitting — checking for regressions, unintended side effects, and quality gaps.

## PROCESS Use WORKFLOW_PAT when pushing workflow YAML changes
**Date:** 2026-03-22 | **Source:** issue #12: [pipeline] Coder blocked from pushing workflow YAML — token lacks workflows permission

When an agent needs to push or commit changes to `.github/workflows/` YAML files, it must use the `WORKFLOW_PAT` token (which has the `workflows` permission), not the standard `GITHUB_TOKEN`, which lacks that permission and will be rejected by GitHub.

## AVOID Set --fallback-model to same value as main model in workflows
**Date:** 2026-03-22 | **Source:** issue #36: [pipeline] --fallback-model same as main model breaks watcher.yml and feedback-learner.yml

In workflow configurations, ensure `--fallback-model` differs from the main model value. Setting them identically breaks watcher.yml and feedback-learner.yml workflows.

## PROCESS Check target branch before creating PRs to avoid redundant work
**Date:** 2026-03-22 | **Source:** issue #37: fix: [pipeline] Avoid CLI/pipeline conflicts — detect human activity and prevent duplicated work (closes #35)

Before opening a PR or starting work on an issue, check the target branch (e.g., main) for recent commits that already implement the fix or feature. CLI sessions and other agents may have already landed the change directly, making a new PR redundant and conflict-prone.

## STYLE Use human-friendly relative time for all user-facing timestamps
**Date:** 2026-03-22 | **Source:** issue #10: [feedback] last updated by badge should use user friendly time descriptions

When displaying time information to users (badges, labels, metadata), use human-friendly relative descriptions (e.g., "2 hours ago", "yesterday", "3 days ago") instead of raw dates or absolute timestamps.
