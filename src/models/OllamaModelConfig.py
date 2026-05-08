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


def get_configs_for_model(model_name: str) -> dict:
    """
    Get normal and tweak configs for a model.

    Args:
        model_name: Model name

    Returns:
        Dictionary with 'normal' and 'tweak' configs
    """
    family = detect_model_family(model_name)

    if 'llama' in family:
        return Llama.get_all()
    elif 'deepseek' in family:
        return Deepseek.get_all()
    elif 'qwen' in family:
        return Qwen.get_all()
    elif 'gemma' in family:
        return Gemma.get_all()
    elif 'devstral' in family or 'mistral' in family:
        return Mistral.get_all()
    else:
        return Default.get_all()


__all__ = [
    "ModelConfig",
    "Llama",
    "Deepseek",
    "Qwen",
    "Gemma",
    "Mistral",
    "Default",
    "detect_model_family",
    "get_configs_for_model",
]