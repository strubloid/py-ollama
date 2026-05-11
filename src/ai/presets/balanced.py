"""Balanced preset configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class BalancedPreset:
    name: str = "Balanced"
    config: str = """PARAMETER num_ctx 4096
PARAMETER num_predict 512
PARAMETER temperature 0.1
PARAMETER top_p 0.8
PARAMETER top_k 20
PARAMETER repeat_penalty 1.05
PARAMETER repeat_last_n 128
PARAMETER seed -1
PARAMETER stop []"""
    system: str = """You are a helpful assistant. Be direct. Complete tasks efficiently with minimal explanation. Never assume—read context first. Use tools when needed. Success means: task done and verified."""


BALANCED = BalancedPreset()