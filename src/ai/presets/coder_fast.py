"""Coder Fast preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CoderFastPreset:
    name: str = "CoderFast"
    config: str = """PARAMETER num_ctx 512
PARAMETER num_predict 32
PARAMETER temperature 0.05
PARAMETER top_p 0.6
PARAMETER top_k 5
PARAMETER repeat_penalty 1.2
PARAMETER repeat_last_n 16
PARAMETER seed -1
PARAMETER stop []"""
    system: str = """Quick coding assistant. Correctness first. Minimal changes. No invented APIs. Provide working code only."""


CODER_FAST = CoderFastPreset()