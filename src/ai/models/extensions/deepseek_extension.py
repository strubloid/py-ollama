"""Deepseek model extensions."""

from ..base import BaseModelFamily
from .base_extension import BaseExtension


class DeepseekExtension(BaseExtension):
    """Extensions for Deepseek model."""

    @staticmethod
    def get_normal(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Leverage Deepseek's strong reasoning capabilities for problem-solving
- Break down complex tasks into logical steps
- Provide clear, structured responses
- Use precise technical language when discussing code or architecture
"""

    @staticmethod
    def get_coder(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Exploit Deepseek's deep code understanding and reasoning
- Prioritize algorithmic efficiency and optimal solutions
- Apply rigorous testing and edge case analysis
- For debugging: trace root causes systematically, don't just fix symptoms
- Recommend idiomatic code patterns for the target language
- Emphasize code that is easy to reason about and maintain
"""

    @staticmethod
    def get_coder_fast(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Use Deepseek's fast reasoning for rapid iteration
- Provide working solutions first, then refine if needed
- Keep code minimal but correct
- Skip lengthy explanations unless critical
- Focus on getting to a working state quickly
"""

    @staticmethod
    def get_explained(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Use Deepseek's reasoning strength to explain complex concepts
- Walk through the "why" behind each decision
- Break down algorithms and data structures step by step
- Compare alternative approaches with pros/cons
- Connect theory to practical implementation
- Anticipate follow-up questions and address them proactively
"""