"""Coder Balanced preset configuration."""

from dataclasses import dataclass
from ai.config.config_loader import get_preset


@dataclass(frozen=True)
class CoderBalancedPreset:
    name: str = "CoderBalanced"
    config: str = ""
    system: str = ""


def _load_coder_balanced() -> CoderBalancedPreset:
    preset_data = get_preset("coder_balanced")
    if preset_data:
        return CoderBalancedPreset(
            name=preset_data.get("name", "CoderBalanced"),
            config=preset_data.get("config", ""),
            system=preset_data.get("system", ""),
        )
    return CoderBalancedPreset()


CODER_BALANCED = _load_coder_balanced()