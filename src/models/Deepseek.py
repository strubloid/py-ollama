"""Deepseek model configurations (coder, etc)."""

from .config import ModelConfig
from .base import (
    BASE_CONFIG, BASE_SYSTEM,
    CODER_CONFIG, CODER_SYSTEM,
    CODER_FAST_CONFIG, CODER_FAST_SYSTEM,
    CODER_BALANCED_CONFIG, CODER_BALANCED_SYSTEM,
    CREATIVE_CONFIG, CREATIVE_SYSTEM,
    PRECISE_CONFIG, PRECISE_SYSTEM,
    LONG_CONTEXT_CONFIG, LONG_CONTEXT_SYSTEM,
)


class Deepseek:
    """Deepseek model configurations."""

    normal = ModelConfig(name="Normal (Recommended)", config=BASE_CONFIG, system=BASE_SYSTEM)
    coder = ModelConfig(name="Coder", config=CODER_CONFIG, system=CODER_SYSTEM)
    coder_fast = ModelConfig(name="CoderFast", config=CODER_FAST_CONFIG, system=CODER_FAST_SYSTEM)
    coder_balanced = ModelConfig(name="CoderBalanced", config=CODER_BALANCED_CONFIG, system=CODER_BALANCED_SYSTEM)
    creative = ModelConfig(name="Creative", config=CREATIVE_CONFIG, system=CREATIVE_SYSTEM)
    precise = ModelConfig(name="Precise", config=PRECISE_CONFIG, system=PRECISE_SYSTEM)
    long_context = ModelConfig(name="Long Context", config=LONG_CONTEXT_CONFIG, system=LONG_CONTEXT_SYSTEM)

    @staticmethod
    def get_all():
        return {
            "normal": Deepseek.normal,
            "coder": Deepseek.coder,
            "coder_fast": Deepseek.coder_fast,
            "coder_balanced": Deepseek.coder_balanced,
            "creative": Deepseek.creative,
            "precise": Deepseek.precise,
            "long_context": Deepseek.long_context,
        }