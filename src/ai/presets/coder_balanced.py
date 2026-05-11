"""Coder Balanced preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CoderBalancedPreset:
    name: str = "CoderBalanced"
    config: str = """PARAMETER num_ctx 1024
PARAMETER num_predict 64
PARAMETER temperature 0.1
PARAMETER top_p 0.7
PARAMETER top_k 10
PARAMETER repeat_penalty 1.15
PARAMETER repeat_last_n 32
PARAMETER seed -1
PARAMETER stop []"""
    system: str = """Expert coding agent. Core: correct, efficient, production-ready code.
1. Read code completely first.
2. Plan ALL changes—no partial fixes.
3. Execute complete solution.
4. Validate: compile, lint, test.
Report what changed. Never claim success unless working."""


CODER_BALANCED = CoderBalancedPreset()