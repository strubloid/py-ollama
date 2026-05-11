"""Creative preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreativePreset:
    name: str = "Creative"
    config: str = """PARAMETER num_ctx 4096
PARAMETER num_predict 512
PARAMETER temperature 0.1
PARAMETER top_p 0.8
PARAMETER top_k 20
PARAMETER repeat_penalty 1.05
PARAMETER repeat_last_n 128
PARAMETER seed -1
PARAMETER stop []"""
    system: str = """You are a creative assistant. Generate multiple approaches. Evaluate impact and feasibility. Choose the strongest direction. Deliver working solutions ready to use."""


CREATIVE = CreativePreset()