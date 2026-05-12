"""Coder Fast preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CoderFastPreset:
    name: str = "CoderFast"
    config: str = """PARAMETER num_ctx 128
PARAMETER num_predict 4
PARAMETER temperature 0.0
PARAMETER top_p 1.0
PARAMETER top_k 1
PARAMETER repeat_penalty 1.0
PARAMETER repeat_last_n 0
PARAMETER seed 42
PARAMETER num_gpu 128
PARAMETER num_batch 512
PARAMETER use_mlock true
PARAMETER use_mmap true
PARAMETER f16_kv true
PARAMETER stop []"""
    system: str = """Quick coding assistant. Correctness first. Minimal changes. No invented APIs. Provide working code only."""


CODER_FAST = CoderFastPreset()