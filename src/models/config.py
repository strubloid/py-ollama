"""Shared ModelConfig dataclass for all models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    """Configuration for a specific model variant."""
    name: str
    config: str  # PARAMETER settings
    system: str  # System prompt
