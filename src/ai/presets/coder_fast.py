"""Coder Fast preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CoderFastPreset:
    name: str = "CoderFast"
    config: str = """PARAMETER num_ctx 2048
PARAMETER num_predict 192
PARAMETER temperature 0.15
PARAMETER top_p 0.85
PARAMETER top_k 20
PARAMETER repeat_penalty 1.1
PARAMETER repeat_last_n 96
PARAMETER seed -1
PARAMETER stop []"""
    system: str = """Quick coding assistant. Correctness first. Minimal changes. No invented APIs. Provide working code only."""


CODER_FAST = CoderFastPreset()