"""Preset configurations for Ollama models."""

from dataclasses import dataclass

from .balanced_preset import BALANCED
from .coder_preset import CODER
from .coder_fast_preset import CODER_FAST
from .coder_balanced_preset import CODER_BALANCED
from .creative_preset import CREATIVE
from .long_context_preset import LONG_CONTEXT


@dataclass(frozen=True)
class OllamaPreset:
    name: str
    config: str
    system: str


PRESETS: list[OllamaPreset] = [
    OllamaPreset(name=BALANCED.name, config=BALANCED.config, system=BALANCED.system),
    OllamaPreset(name=CODER.name, config=CODER.config, system=CODER.system),
    OllamaPreset(name=CODER_FAST.name, config=CODER_FAST.config, system=CODER_FAST.system),
    OllamaPreset(name=CODER_BALANCED.name, config=CODER_BALANCED.config, system=CODER_BALANCED.system),
    OllamaPreset(name=CREATIVE.name, config=CREATIVE.config, system=CREATIVE.system),
    OllamaPreset(name=LONG_CONTEXT.name, config=LONG_CONTEXT.config, system=LONG_CONTEXT.system),
]


def list_preset_names() -> list[str]:
    return [preset.name for preset in PRESETS]