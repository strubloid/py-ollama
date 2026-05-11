"""AI Config package."""

from .model_config import detect_model_family
from .ollama_config import ModelConfig


__all__ = [
    "detect_model_family",
    "ModelConfig",
]