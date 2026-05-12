"""Balanced preset configuration."""

from dataclasses import dataclass
from ai.config.config_loader import get_preset


@dataclass(frozen=True)
class BalancedPreset:
    name: str = "Balanced"
    config: str = ""
    system: str = ""


def _load_balanced() -> BalancedPreset:
    preset_data = get_preset("balanced")
    if preset_data:
        return BalancedPreset(
            name=preset_data.get("name", "Balanced"),
            config=preset_data.get("config", ""),
            system=preset_data.get("system", ""),
        )
    return BalancedPreset()


BALANCED = _load_balanced()