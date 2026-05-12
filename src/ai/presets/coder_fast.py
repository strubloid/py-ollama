"""Coder Fast preset configuration."""

from dataclasses import dataclass
from ai.config.config_loader import get_preset


@dataclass(frozen=True)
class CoderFastPreset:
    name: str = "CoderFast"
    config: str = ""
    system: str = ""


def _load_coder_fast() -> CoderFastPreset:
    preset_data = get_preset("coder_fast")
    if preset_data:
        return CoderFastPreset(
            name=preset_data.get("name", "CoderFast"),
            config=preset_data.get("config", ""),
            system=preset_data.get("system", ""),
        )
    return CoderFastPreset()


CODER_FAST = _load_coder_fast()