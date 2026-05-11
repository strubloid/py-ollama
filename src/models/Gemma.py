"""Gemma model configurations (2, 7b, etc)."""

from .config import ModelConfig
from .base import BaseModelFamily, NORMAL_CONFIG, NORMAL_SYSTEM, CODER_CONFIG, CODER_SYSTEM, CODER_FAST_CONFIG, CODER_FAST_SYSTEM, EXPLAINED_CONFIG, EXPLAINED_SYSTEM


class Gemma(BaseModelFamily):
    """Gemma model configurations."""

    family_name = "Gemma"
    model_name = "Eggy"

    def model_profile(self) -> str:
        return "Gemma is Google's compact but powerful model optimized for efficiency and instruction following."

    def _build_system(self, base_system: str, extension: str) -> str:
        if not extension:
            return base_system
        return f"{base_system}\n\n---\n\n{extension}"

    def normal(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Follow instructions precisely
- Be concise but complete
- Use structured responses when helpful
"""
        return ModelConfig(
            mode="normal",
            name="Normal (Recommended)",
            config=NORMAL_CONFIG,
            system=self._build_system(NORMAL_SYSTEM, extension),
        )

    def coder(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Write efficient, clean code
- Use modern best practices
- Prioritize readability
- Apply proper error handling
- Leverage Gemma's instruction-following strength
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
- Minimal complexity
- Focus on correctness
"""
        return ModelConfig(
            mode="coder_fast",
            name="Coder Fast",
            config=CODER_FAST_CONFIG,
            system=self._build_system(CODER_FAST_SYSTEM, extension),
        )

    def explained(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Clear, structured explanations
- Step-by-step reasoning
- Practical examples
"""
        return ModelConfig(
            mode="explained",
            name="Explained",
            config=EXPLAINED_CONFIG,
            system=self._build_system(EXPLAINED_SYSTEM, extension),
        )