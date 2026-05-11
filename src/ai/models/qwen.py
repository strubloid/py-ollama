"""Qwen model configurations (2.5-coder, etc)."""

from ..config import ModelConfig
from .base import BaseModelFamily, NORMAL_CONFIG, NORMAL_SYSTEM, CODER_CONFIG, CODER_SYSTEM, CODER_FAST_CONFIG, CODER_FAST_SYSTEM, EXPLAINED_CONFIG, EXPLAINED_SYSTEM
from .extensions.qwen_extension import QwenExtension


class Qwen(BaseModelFamily):
    """Qwen model configurations."""

    family_name = "Qwen"
    model_name = "Alibaba"

    def model_profile(self) -> str:
        return "Qwen excels at multilingual and coding tasks. It has strong instruction-following and chat capabilities."

    def _build_system(self, base_system: str, extension: str) -> str:
        if not extension:
            return base_system
        return f"{base_system}\n\n---\n\n{extension}"

    def normal(self, custom_name: str = ""):
        extension = QwenExtension.get_normal(custom_name)
        return ModelConfig(
            mode="normal",
            name="Normal (Recommended)",
            config=NORMAL_CONFIG,
            system=self._build_system(NORMAL_SYSTEM, extension),
        )

    def coder(self, custom_name: str = ""):
        extension = QwenExtension.get_coder(custom_name)
        return ModelConfig(
            mode="coder",
            name="Coder",
            config=CODER_CONFIG,
            system=self._build_system(CODER_SYSTEM, extension),
        )

    def coder_fast(self, custom_name: str = ""):
        extension = QwenExtension.get_coder_fast(custom_name)
        return ModelConfig(
            mode="coder_fast",
            name="Coder Fast",
            config=CODER_FAST_CONFIG,
            system=self._build_system(CODER_FAST_SYSTEM, extension),
        )

    def explained(self, custom_name: str = ""):
        extension = QwenExtension.get_explained(custom_name)
        return ModelConfig(
            mode="explained",
            name="Explained",
            config=EXPLAINED_CONFIG,
            system=self._build_system(EXPLAINED_SYSTEM, extension),
        )