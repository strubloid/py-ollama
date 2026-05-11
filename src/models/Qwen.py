"""Qwen model configurations (2.5-coder, etc)."""

from .config import ModelConfig
from .base import BaseModelFamily, NORMAL_CONFIG, NORMAL_SYSTEM, CODER_CONFIG, CODER_SYSTEM, CODER_FAST_CONFIG, CODER_FAST_SYSTEM, EXPLAINED_CONFIG, EXPLAINED_SYSTEM


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
        extension = f"""[{self.getModelName(custom_name)}]
- Follow user instructions precisely and completely
- Use clear, conversational language
- Handle multilingual requests gracefully
- Provide structured output when appropriate
"""
        return ModelConfig(
            mode="normal",
            name="Normal (Recommended)",
            config=NORMAL_CONFIG,
            system=self._build_system(NORMAL_SYSTEM, extension),
        )

    def coder(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Write clean, well-documented code
- Use Qwen's multilingual strength for international codebases
- Prioritize readable, maintainable solutions
- Add helpful inline comments for complex logic
- Follow language-specific best practices and idioms
- Ensure code works across different environments
"""
        return ModelConfig(
            mode="coder",
            name="Coder",
            config=CODER_CONFIG,
            system=self._build_system(CODER_SYSTEM, extension),
        )

    def coder_fast(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Provide concise, working solutions quickly
- Skip unnecessary documentation
- Focus on getting the job done efficiently
- Use standard patterns without over-engineering
"""
        return ModelConfig(
            mode="coder_fast",
            name="Coder Fast",
            config=CODER_FAST_CONFIG,
            system=self._build_system(CODER_FAST_SYSTEM, extension),
        )

    def explained(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Explain concepts clearly in accessible language
- Use examples to illustrate abstract ideas
- Break down complex problems into digestible parts
- Provide context that helps understanding
- Be patient and thorough in explanations
"""
        return ModelConfig(
            mode="explained",
            name="Explained",
            config=EXPLAINED_CONFIG,
            system=self._build_system(EXPLAINED_SYSTEM, extension),
        )