"""Coder Fast preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CoderFastPreset:
    name: str = "CoderFast"
    config: str = """PARAMETER num_ctx 512
PARAMETER num_predict 64
PARAMETER temperature 0.1
PARAMETER top_p 0.7
PARAMETER top_k 10
PARAMETER repeat_penalty 1.1
PARAMETER repeat_last_n 32
PARAMETER seed -1
PARAMETER stop []"""
    system: str = """Quick coding assistant. Correctness first. Minimal changes. No invented APIs. Provide working code only."""


CODER_FAST = CoderFastPreset()