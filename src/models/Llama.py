"""Llama model configurations (2, 2.7b, 3, etc)."""

from .config import ModelConfig
from .base import BaseModelFamily, NORMAL_CONFIG, NORMAL_SYSTEM, CODER_CONFIG, CODER_SYSTEM, CODER_FAST_CONFIG, CODER_FAST_SYSTEM, EXPLAINED_CONFIG, EXPLAINED_SYSTEM


class Llama(BaseModelFamily):
    """Llama model configurations."""

    family_name = "Llama"

    def model_profile(self) -> str:
        return "Llama by Meta is a versatile open-source model with strong general reasoning capabilities."

    def _build_system(self, base_system: str, extension: str) -> str:
        if not extension:
            return base_system
        return f"{base_system}\n\n---\n\n{extension}"

    def normal(self):
        extension = """[Llama Normal Mode]
- Be direct and practical in responses
- Use Llama's strong reasoning to break down problems
- Provide clear, actionable answers
"""
        return ModelConfig(
            mode="normal",
            name="Normal (Recommended)",
            config=NORMAL_CONFIG,
            system=self._build_system(NORMAL_SYSTEM, extension),
        )

    def coder(self):
        extension = """[Llama Coder Mode]
- Write idiomatic code following best practices
- Use modern language features and patterns
- Prioritize correctness and efficiency
- Apply proper error handling and edge cases
- Write self-documenting code
"""
        return ModelConfig(
            mode="coder",
            name="Coder",
            config=CODER_CONFIG,
            system=self._build_system(CODER_SYSTEM, extension),
        )

    def coder_fast(self):
        extension = """[Llama Coder Fast Mode]
- Provide quick, working solutions
- Keep it simple and functional
- Minimal explanation, maximum results
"""
        return ModelConfig(
            mode="coder_fast",
            name="Coder Fast",
            config=CODER_FAST_CONFIG,
            system=self._build_system(CODER_FAST_SYSTEM, extension),
        )

    def explained(self):
        extension = """[Llama Explained Mode]
- Explain reasoning step by step
- Connect concepts logically
- Provide practical examples
- Make complex ideas accessible
"""
        return ModelConfig(
            mode="explained",
            name="Explained",
            config=EXPLAINED_CONFIG,
            system=self._build_system(EXPLAINED_SYSTEM, extension),
        )