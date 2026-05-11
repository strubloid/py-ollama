"""Deepseek model configurations (coder, etc)."""

from .config import ModelConfig
from .base import BaseModelFamily, NORMAL_CONFIG, NORMAL_SYSTEM, CODER_CONFIG, CODER_SYSTEM, CODER_FAST_CONFIG, CODER_FAST_SYSTEM, EXPLAINED_CONFIG, EXPLAINED_SYSTEM


class Deepseek(BaseModelFamily):
    """Deepseek model configurations."""

    family_name = "Deepseek"
    model_name = "XingLing"

    def model_profile(self) -> str:
        return "Deepseek excels at reasoning, mathematics, and complex coding tasks. It has strong chain-of-thought capabilities."

    def _build_system(self, base_system: str, extension: str) -> str:
        if not extension:
            return base_system
        return f"{base_system}\n\n---\n\n{extension}"

    def normal(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Leverage Deepseek's strong reasoning capabilities for problem-solving
- Break down complex tasks into logical steps
- Provide clear, structured responses
- Use precise technical language when discussing code or architecture
"""
        return ModelConfig(
            mode="normal",
            name="Normal (Recommended)",
            config=NORMAL_CONFIG,
            system=self._build_system(NORMAL_SYSTEM, extension),
        )

    def coder(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Exploit Deepseek's deep code understanding and reasoning
- Prioritize algorithmic efficiency and optimal solutions
- Apply rigorous testing and edge case analysis
- For debugging: trace root causes systematically, don't just fix symptoms
- Recommend idiomatic code patterns for the target language
- Emphasize code that is easy to reason about and maintain
"""
        return ModelConfig(
            mode="coder",
            name="Coder",
            config=CODER_CONFIG,
            system=self._build_system(CODER_SYSTEM, extension),
        )

    def coder_fast(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Use Deepseek's fast reasoning for rapid iteration
- Provide working solutions first, then refine if needed
- Keep code minimal but correct
- Skip lengthy explanations unless critical
- Focus on getting to a working state quickly
"""
        return ModelConfig(
            mode="coder_fast",
            name="Coder Fast",
            config=CODER_FAST_CONFIG,
            system=self._build_system(CODER_FAST_SYSTEM, extension),
        )

    def explained(self, custom_name: str = ""):
        extension = f"""[{self.getModelName(custom_name)}]
- Use Deepseek's reasoning strength to explain complex concepts
- Walk through the "why" behind each decision
- Break down algorithms and data structures step by step
- Compare alternative approaches with pros/cons
- Connect theory to practical implementation
- Anticipate follow-up questions and address them proactively
"""
        return ModelConfig(
            mode="explained",
            name="Explained",
            config=EXPLAINED_CONFIG,
            system=self._build_system(EXPLAINED_SYSTEM, extension),
        )