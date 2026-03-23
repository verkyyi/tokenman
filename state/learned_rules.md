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

## AVOID Don't propose micro-optimizations that add complexity for trivial savings
**Date:** 2026-03-22 | **Source:** issue #31: [evolve] Cache research source checksums to skip unchanged sources

Don't propose optimizations where the added complexity (e.g., caching layers, checksum management) outweighs the savings (e.g., ~$0.30/month in tokens). Token cost is not a concern when running high-tier models. Cosmetic issues (like duplicate log entries) are not functional problems and don't warrant architectural changes.

## AVOID Don't duplicate periodic checks into every workflow run
**Date:** 2026-03-22 | **Source:** issue #38: Readme content shall be kept consistent along repo changes, automatically maintained by the workflow and pipeline itself

When a dedicated periodic check already handles a concern (e.g., daily evolve SEO/discoverability step for README consistency), don't scatter the same check into every workflow run. A daily check is sufficient for files that change infrequently — adding it everywhere is over-engineering.

## PROCESS Use incremental exploration, not full repo scans every run
**Date:** 2026-03-22 | **Source:** issue #44: Reduce workflow run time: agent re-explores entire repo every run

Agents must not re-explore the entire repository from scratch on every workflow run. Instead, read state files (project_state.md, FEATURE_STATUS.md) and use targeted file reads for the task at hand. Reserve broad codebase exploration for genuinely new or unfamiliar contexts.

## PROCESS Handle pre-existing branches when creating CI branches
**Date:** 2026-03-23 | **Source:** issue #59: [pipeline] Weekly Analysis fails on stale branch — date-based branch name collision

When a workflow creates a branch (especially date-based names like `analyze/20260323-47`), the branch may already exist locally or on the remote from a prior run. Use `git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"` or `git checkout -B` to handle collisions gracefully, and delete stale remote branches after PR merge. Never assume a generated branch name is unused.
