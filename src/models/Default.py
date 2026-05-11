"""Default balanced configurations for unknown models."""

from .config import ModelConfig
from .base import BaseModelFamily, NORMAL_CONFIG, NORMAL_SYSTEM, CODER_CONFIG, CODER_SYSTEM, CODER_FAST_CONFIG, CODER_FAST_SYSTEM, EXPLAINED_CONFIG, EXPLAINED_SYSTEM


class Default(BaseModelFamily):
    """Default balanced configurations for unknown models."""

    family_name = "Default"
    model_name = "No Name"

    def model_profile(self) -> str:
        return "General-purpose configuration suitable for most Ollama models."

    def _build_system(self, base_system: str, extension: str) -> str:
        if not extension:
            return base_system
        return f"{base_system}\n\n---\n\n{extension}"

    def normal(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Be helpful and practical
- Follow user instructions
- Provide clear responses
"""
        return ModelConfig(
            mode="normal",
            name="Normal (Recommended)",
            config=NORMAL_CONFIG,
            system=self._build_system(NORMAL_SYSTEM, extension),
        )

    def coder(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Write correct, maintainable code
- Apply best practices
- Handle errors properly
- Test edge cases
"""
        return ModelConfig(
            mode="coder",
            name="Coder",
            config=CODER_CONFIG,
            system=self._build_system(CODER_SYSTEM, extension),
        )

    def coder_fast(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Quick, working solutions
- Keep it simple
"""
        return ModelConfig(
            mode="coder_fast",
            name="Coder Fast",
            config=CODER_FAST_CONFIG,
            system=self._build_system(CODER_FAST_SYSTEM, extension),
        )

    def explained(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Clear explanations
- Step-by-step reasoning
- Practical examples
"""
        return ModelConfig(
            mode="explained",
            name="Explained",
            config=EXPLAINED_CONFIG,
            system=self._build_system(EXPLAINED_SYSTEM, extension),
        )