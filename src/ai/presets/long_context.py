"""Long Context preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LongContextPreset:
    name: str = "Long Context"
    config: str = """PARAMETER num_ctx 512
PARAMETER num_predict 16
PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER top_k 5
PARAMETER repeat_penalty 1.0
PARAMETER repeat_last_n 0
PARAMETER seed 42
PARAMETER num_gpu 128
PARAMETER num_batch 512
PARAMETER use_mlock true
PARAMETER use_mmap true
PARAMETER f16_kv true
PARAMETER stop []"""
    system: str = """Coding teacher. For each task:
1. Explain problem and assumptions.
2. Walk through approach with trade-offs.
3. Show code with reasoning.
4. Note edge cases and testing.

Be concise but thorough."""


LONG_CONTEXT = LongContextPreset()