from ..base import BaseModelFamily
from .base_extension import BaseExtension

"""Gemma model extensions."""
class GemmaExtension(BaseExtension):

    @staticmethod
    def get_normal(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Follow instructions precisely
- Be concise but complete
- Use structured responses when helpful
"""

    @staticmethod
    def get_coder(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Write efficient, clean code
- Use modern best practices
- Prioritize readability
- Apply proper error handling
- Leverage Gemma's instruction-following strength
"""

    @staticmethod
    def get_coder_fast(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Quick, working solutions
- Minimal complexity
- Focus on correctness
"""

    @staticmethod
    def get_explained(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Clear, structured explanations
- Step-by-step reasoning
- Practical examples
"""