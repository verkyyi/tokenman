# `skills/` — bootstrap directory

Temporary. This directory is a **bootstrap posture**: `readme-maintainer`
lives in-tree during Phase 1.2b so the harness has a real skill to
invoke without depending on an external repository that doesn't exist
yet.

Spec §5.1 says tokenman **ships zero skills**. This directory violates
that principle on purpose and on a deadline: `readme-maintainer` must
be split out to a standalone repository before Phase 3 opens dogfood
runs against the library itself.

Do not add more skills here. Real skills live in their own repos and
are pinned in `recommended-skills.yaml` by URL.
