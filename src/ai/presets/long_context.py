"""Long Context preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LongContextPreset:
    name: str = "Long Context"
    config: str = """PARAMETER num_ctx 4096
PARAMETER num_predict 512
PARAMETER temperature 0.1
PARAMETER top_p 0.8
PARAMETER top_k 20
PARAMETER repeat_penalty 1.05
PARAMETER repeat_last_n 128
PARAMETER seed -1
PARAMETER stop []"""
    system: str = """You are a coding teacher. Be practical and concise. Explain key decisions and trade-offs. Focus on root causes, not symptoms. Show working code with brief reasoning."""


LONG_CONTEXT = LongContextPreset()