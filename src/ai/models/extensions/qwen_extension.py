"""Qwen model extensions."""

from ..base import BaseModelFamily
from .base_extension import BaseExtension


class QwenExtension(BaseExtension):
    """Extensions for Qwen model."""

    @staticmethod
    def get_normal(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Follow user instructions precisely and completely
- Use clear, conversational language
- Handle multilingual requests gracefully
- Provide structured output when appropriate
"""

    @staticmethod
    def get_coder(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Write clean, well-documented code
- Use Qwen's multilingual strength for international codebases
- Prioritize readable, maintainable solutions
- Add helpful inline comments for complex logic
- Follow language-specific best practices and idioms
- Ensure code works across different environments
"""

    @staticmethod
    def get_coder_fast(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Provide concise, working solutions quickly
- Skip unnecessary documentation
- Focus on getting the job done efficiently
- Use standard patterns without over-engineering
"""

    @staticmethod
    def get_explained(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Explain concepts clearly in accessible language
- Use examples to illustrate abstract ideas
- Break down complex problems into digestible parts
- Provide context that helps understanding
- Be patient and thorough in explanations
"""