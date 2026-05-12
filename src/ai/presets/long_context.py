"""Long Context preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LongContextPreset:
    name: str = "Long Context"
    config: str = """PARAMETER num_ctx 1024
PARAMETER num_predict 128
PARAMETER temperature 0.2
PARAMETER top_p 0.8
PARAMETER top_k 20
PARAMETER repeat_penalty 1.1
PARAMETER repeat_last_n 64
PARAMETER seed -1
PARAMETER stop []"""
    system: str = """Coding teacher. For each task:
1. Explain problem and assumptions.
2. Walk through approach with trade-offs.
3. Show code with reasoning.
4. Note edge cases and testing.

Be concise but thorough."""


LONG_CONTEXT = LongContextPreset()