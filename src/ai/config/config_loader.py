"""
Configuration loader for py-ollama.
Loads configurations from JSON files in the configs/ directory.
"""

import json
from pathlib import Path
from functools import lru_cache
from typing import Optional

_CONFIG_DIR = Path(__file__).parent.parent.parent.parent / "configs"


@lru_cache(maxsize=1)
def load_model_config() -> dict:
    """Load model configurations from JSON file."""
    config_path = _CONFIG_DIR / "model_config.json"
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


@lru_cache(maxsize=1)
def load_presets_config() -> dict:
    """Load presets configurations from JSON file."""
    config_path = _CONFIG_DIR / "presets.json"
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def get_model_params(mode: str) -> dict:
    """Get model parameters for a specific mode."""
    config = load_model_config()
    return config.get("model_params", {}).get(mode, {})


def get_system_prompt(mode: str) -> str:
    """Get system prompt for a specific mode."""
    config = load_model_config()
    return config.get("system_prompts", {}).get(mode, "")


def get_preset(preset_name: str) -> Optional[dict]:
    """Get preset configuration by name."""
    config = load_presets_config()
    return config.get("presets", {}).get(preset_name)


def get_all_presets() -> dict:
    """Get all presets configurations."""
    config = load_presets_config()
    return config.get("presets", {})


def reload_configs() -> None:
    """Clear cached configurations to force reload."""
    load_model_config.cache_clear()
    load_presets_config.cache_clear()


_EXCLUDED_KEYS = frozenset({"name", "description"})


def config_to_string(config: dict) -> str:
    """Convert config dict to PARAMETER string."""
    lines = []
    for key, value in sorted(config.items()):
        if key in _EXCLUDED_KEYS:
            continue
        if key == 'stop':
            lines.append(f"PARAMETER {key} []")
        elif isinstance(value, bool):
            lines.append(f"PARAMETER {key} {str(value).lower()}")
        elif isinstance(value, list):
            lines.append(f"PARAMETER {key} {value}")
        else:
            lines.append(f"PARAMETER {key} {value}")
    return "\n".join(lines)