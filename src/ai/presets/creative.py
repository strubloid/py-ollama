"""Creative preset configuration."""

from dataclasses import dataclass
from ai.config.config_loader import get_preset


@dataclass(frozen=True)
class CreativePreset:
    name: str = "Creative"
    config: str = ""
    system: str = ""


def _load_creative() -> CreativePreset:
    preset_data = get_preset("creative")
    if preset_data:
        return CreativePreset(
            name=preset_data.get("name", "Creative"),
            config=preset_data.get("config", ""),
            system=preset_data.get("system", ""),
        )
    return CreativePreset()


CREATIVE = _load_creative()