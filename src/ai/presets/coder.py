"""Coder preset configuration."""

from dataclasses import dataclass
from ai.config.config_loader import get_preset


@dataclass(frozen=True)
class CoderPreset:
    name: str = "Coder"
    config: str = ""
    system: str = ""


def _load_coder() -> CoderPreset:
    preset_data = get_preset("coder")
    if preset_data:
        return CoderPreset(
            name=preset_data.get("name", "Coder"),
            config=preset_data.get("config", ""),
            system=preset_data.get("system", ""),
        )
    return CoderPreset()


CODER = _load_coder()