"""`python -m harness.onboard` — runs all enabled skills back-to-back
in one session, opens a PR per skill, writes
.tokenman/onboarding-summary.md.

See docs/superpowers/specs/2026-04-18-phase-1-4-onboarding-mode-design.md.
"""
from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    raise NotImplementedError("harness.onboard CLI lands in Task 10")


if __name__ == "__main__":
    sys.exit(main())
