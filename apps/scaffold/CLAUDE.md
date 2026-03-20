# Scaffold — Self-Evolution Constitution
# Rules for how the harness improves itself.
# Root harness rules live in the root CLAUDE.md.

## This Project
The scaffold's first project is itself. The agent analyzes its own
workflows, skills, and failure log to propose improvements.
This file governs HOW the agent evolves the harness.

Owner: autonomous (reviewed by human)
Scope: all files in repo root (.github/, skills/, state/, CLAUDE.md)

## Self-Evolution Rules

ANALYZE — what the agent examines:
- CLAUDE.md failure log for repeated patterns
- Workflow run history for inefficiencies
- Skill files for gaps or outdated guidance
- External research (Anthropic blog, GitHub changelog, reference repos)
- state/agent_log.md for action patterns

PROPOSE — how improvements are suggested:
- One structural PR per evolve.yml run maximum
- Each PR must cite the failure or inefficiency that triggered it
- Research-inspired changes always need human review

FORBIDDEN — the agent must never:
- Promote its own autonomy (move needs-review to auto-commit)
- Modify workflow YAML without human review
- Chain multiple structural changes in one run
- Delete skill files or state files

## Autonomy Overrides
# These override root CLAUDE.md defaults for scaffold self-evolution.

failure_log_entries: auto
skill_wording_clarity: auto
skill_behavioral_changes: auto-merge
workflow_yaml_changes: needs-review
claude_md_autonomy_rules: needs-review
new_skill_files: needs-review

## Failure Log
# Add a line every time the agent makes a mistake evolving itself.
# Format: # DATE: what went wrong → what rule prevents it now
