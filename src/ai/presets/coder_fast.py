"""Coder Fast preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CoderFastPreset:
    name: str = "CoderFast"
    config: str = """PARAMETER num_ctx 4096
PARAMETER num_predict 256
PARAMETER temperature 0.1
PARAMETER top_p 0.8
PARAMETER top_k 20
PARAMETER repeat_penalty 1.05
PARAMETER repeat_last_n 128
PARAMETER seed -1
PARAMETER stop []"""
    system: str = """Quick coding assistant. Write minimal working code. No explanation unless requested. Provide only what solves the problem."""


CODER_FAST = CoderFastPreset()