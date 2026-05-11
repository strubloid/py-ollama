"""Model family detection and configuration lookup."""

from .config import ModelConfig
from .Llama import Llama
from .Deepseek import Deepseek
from .Qwen import Qwen
from .Gemma import Gemma
from .Mistral import Mistral
from .Default import Default
from .OllamaModelConfig import detect_model_family


MODEL_FAMILIES = {
    "llama": Llama,
    "deepseek": Deepseek,
    "qwen": Qwen,
    "gemma": Gemma,
    "mistral": Mistral,
    "devstral": Mistral,
}


def _get_family_instance(model_name: str):
    """Get the model family instance for a given model name."""
    family_key = detect_model_family(model_name)

    family_class = Default
    for key, cls in MODEL_FAMILIES.items():
        if key in family_key:
            family_class = cls
            break

    return family_class()


def get_configs_for_model(model_name: str) -> dict:
    """
    Get all configs for a model.

    Args:
        model_name: Model name

    Returns:
        Dictionary with all config options (normal, coder, coder_fast, explained)
    """
    return _get_family_instance(model_name).get_all()


def get_normal_mode(model_name: str) -> ModelConfig:
    """Get the normal mode config for a model."""
    return _get_family_instance(model_name).normal()


def get_coder_mode(model_name: str) -> ModelConfig:
    """Get the coder mode config for a model."""
    return _get_family_instance(model_name).coder()


def get_coder_fast_mode(model_name: str) -> ModelConfig:
    """Get the coder_fast mode config for a model."""
    return _get_family_instance(model_name).coder_fast()


def get_explained_mode(model_name: str) -> ModelConfig:
    """Get the explained mode config for a model."""
    return _get_family_instance(model_name).explained()


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
    "get_normal_mode",
    "get_coder_mode",
    "get_coder_fast_mode",
    "get_explained_mode",
    "MODEL_FAMILIES",
]