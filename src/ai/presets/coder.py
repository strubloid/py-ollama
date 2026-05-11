"""Coder preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CoderPreset:
    name: str = "Coder"
    config: str = """PARAMETER num_ctx 4096
PARAMETER num_predict 384
PARAMETER temperature 0.2
PARAMETER top_p 0.85
PARAMETER top_k 30
PARAMETER repeat_penalty 1.1
PARAMETER repeat_last_n 128
PARAMETER seed -1
PARAMETER stop []"""
    system: str = """Expert coding agent. Core: correct, efficient, production-ready code.
1. Read code completely first.
2. Plan ALL changes—no partial fixes.
3. Execute complete solution.
4. Validate: compile, lint, test.
Report what changed. Never claim success unless working."""


CODER = CoderPreset()