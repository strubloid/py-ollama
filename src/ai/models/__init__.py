"""AI Models package."""

from .default import Default
from .deepseek import Deepseek
from .gemma import Gemma
from .llama import Llama
from .mistral import Mistral
from .qwen import Qwen
from .granite import Granite
from .devstral import Devstral
from .base import BaseModelFamily
from ..config import ModelConfig
from ..config.model_config import detect_model_family

MODEL_FAMILIES = {
    "llama": Llama,
    "deepseek": Deepseek,
    "qwen": Qwen,
    "qwen3": Qwen,
    "gemma": Gemma,
    "mistral": Mistral,
    "granite": Granite,
    "devstral": Devstral,
}


def get_configs_for_model(model_name: str, custom_name: str = "") -> dict:
    family_key = detect_model_family(model_name)

    family_class = Default
    for key, cls in MODEL_FAMILIES.items():
        if key in family_key:
            family_class = cls
            break

    return family_class().get_all(custom_name)


def get_normal_mode(model_name: str, custom_name: str = "") -> ModelConfig:
    return get_configs_for_model(model_name, custom_name).get("normal")


def get_coder_mode(model_name: str, custom_name: str = "") -> ModelConfig:
    return get_configs_for_model(model_name, custom_name).get("coder")


def get_coder_fast_mode(model_name: str, custom_name: str = "") -> ModelConfig:
    return get_configs_for_model(model_name, custom_name).get("coder_fast")


def get_explained_mode(model_name: str, custom_name: str = "") -> ModelConfig:
    return get_configs_for_model(model_name, custom_name).get("explained")


__all__ = [
    "Default",
    "Deepseek",
    "Gemma",
    "Llama",
    "Mistral",
    "Qwen",
    "Granite",
    "Devstral",
    "BaseModelFamily",
    "MODEL_FAMILIES",
    "get_configs_for_model",
    "get_normal_mode",
    "get_coder_mode",
    "get_coder_fast_mode",
    "get_explained_mode",
    "detect_model_family",
    "ModelConfig",
]