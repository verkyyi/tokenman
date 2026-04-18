"""Onboarding orchestrator — loops runner.run_skill across enabled skills,
tracks token budget, synthesises skipped_budget entries on ceiling breach.

See docs/superpowers/specs/2026-04-18-phase-1-4-onboarding-mode-design.md.
"""
from __future__ import annotations
