"""Mistral/Devstral model configurations."""

from ..config import ModelConfig
from .base import BaseModelFamily, NORMAL_CONFIG, NORMAL_SYSTEM, CODER_CONFIG, CODER_SYSTEM, CODER_FAST_CONFIG, CODER_FAST_SYSTEM, EXPLAINED_CONFIG, EXPLAINED_SYSTEM


class Mistral(BaseModelFamily):
    """Mistral/Devstral model configurations."""

    family_name = "Mistral"
    model_name = "Macumba"

    def model_profile(self) -> str:
        return "Mistral excels at reasoning and code generation with efficient context handling. Devstral is optimized for developer productivity."

    def _build_system(self, base_system: str, extension: str) -> str:
        if not extension:
            return base_system
        return f"{base_system}\n\n---\n\n{extension}"

    def normal(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Use efficient, direct communication
- Leverage Mistral's strong reasoning
- Provide practical solutions
"""
        return ModelConfig(
            mode="normal",
            name="Normal (Recommended)",
            config=NORMAL_CONFIG,
            system=self._build_system(NORMAL_SYSTEM, extension),
        )

    def coder(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Write optimized, efficient code
- Use Mistral's context efficiency for large codebases
- Prioritize performance when needed
- Apply proper error handling
- Follow language idioms
"""
        return ModelConfig(
            mode="coder",
            name="Coder",
            config=CODER_CONFIG,
            system=self._build_system(CODER_SYSTEM, extension),
        )

    def coder_fast(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Fast, efficient responses
- Minimal but correct solutions
- Quick iteration
"""
        return ModelConfig(
            mode="coder_fast",
            name="Coder Fast",
            config=CODER_FAST_CONFIG,
            system=self._build_system(CODER_FAST_SYSTEM, extension),
        )

    def explained(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Clear technical explanations
- Connect reasoning to implementation
- Practical examples
- Efficient communication
"""
        return ModelConfig(
            mode="explained",
            name="Explained",
            config=EXPLAINED_CONFIG,
            system=self._build_system(EXPLAINED_SYSTEM, extension),
        )