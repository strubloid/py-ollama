"""AI Presets package."""

from .model import OllamaPreset, PRESETS, list_preset_names, get_preset_by_name


__all__ = [
    "OllamaPreset",
    "PRESETS",
    "list_preset_names",
    "get_preset_by_name",
]