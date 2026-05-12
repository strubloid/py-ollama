"""Long Context preset configuration."""

from dataclasses import dataclass
from ai.config.config_loader import get_preset


@dataclass(frozen=True)
class LongContextPreset:
    name: str = "Long Context"
    config: str = ""
    system: str = ""


def _load_long_context() -> LongContextPreset:
    preset_data = get_preset("long_context")
    if preset_data:
        return LongContextPreset(
            name=preset_data.get("name", "Long Context"),
            config=preset_data.get("config", ""),
            system=preset_data.get("system", ""),
        )
    return LongContextPreset()


LONG_CONTEXT = _load_long_context()