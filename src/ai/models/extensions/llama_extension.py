from ..base import BaseModelFamily
from .base_extension import BaseExtension

"""Llama model extensions."""
class LlamaExtension(BaseExtension):

    @staticmethod
    def get_normal(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Be direct and practical in responses
- Use Llama's strong reasoning to break down problems
- Provide clear, actionable answers
"""

    @staticmethod
    def get_coder(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Write idiomatic code following best practices
- Use modern language features and patterns
- Prioritize correctness and efficiency
- Apply proper error handling and edge cases
- Write self-documenting code
"""

    @staticmethod
    def get_coder_fast(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Provide quick, working solutions
- Keep it simple and functional
- Minimal explanation, maximum results
"""

    @staticmethod
    def get_explained(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Explain reasoning step by step
- Connect concepts logically
- Provide practical examples
- Make complex ideas accessible
"""