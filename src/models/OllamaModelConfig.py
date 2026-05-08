"""Model family detection and configuration lookup."""

from .config import ModelConfig
from .Llama import Llama
from .Deepseek import Deepseek
from .Qwen import Qwen
from .Gemma import Gemma
from .Mistral import Mistral
from .Default import Default


def detect_model_family(model_name: str) -> str:
    """
    Detect model family from model name.

    Args:
        model_name: Model name (e.g., 'llama2:latest', 'deepseek-coder')

    Returns:
        Model family name (lowercase)
    """
    base = model_name.lower().split(':')[0]
    return base


__all__ = [
    "ModelConfig",
    "Llama",
    "Deepseek",
    "Qwen",
    "Gemma",
    "Mistral",
    "Default",
    "detect_model_family",
]