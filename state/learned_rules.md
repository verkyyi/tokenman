# Learned Rules
# Append-only. Extracted from human feedback on PRs and issues.
# Every agent reads this file. Rules here override default behavior.
# Format: each rule is a ## heading with date, source, and the lesson.

# Rules below this line are added automatically by the feedback-learner workflow.

## QUALITY Adversarial self-review before submitting agent output
**Date:** 2026-03-21 | **Source:** issue #4: [evolve] Add adversarial self-review step to evolve.yml agent output

The evolve agent (and agents in general) should include an adversarial self-review step that critically challenges its own proposed changes before submitting — checking for regressions, unintended side effects, and quality gaps.
