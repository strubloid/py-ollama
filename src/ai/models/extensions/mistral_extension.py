"""Mistral model extensions."""

from ..base import BaseModelFamily
from .base_extension import BaseExtension


class MistralExtension(BaseExtension):
    """Extensions for Mistral model."""

    @staticmethod
    def get_normal(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Use efficient, direct communication
- Leverage Mistral's strong reasoning
- Provide practical solutions
"""

    @staticmethod
    def get_coder(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Write optimized, efficient code
- Use Mistral's context efficiency for large codebases
- Prioritize performance when needed
- Apply proper error handling
- Follow language idioms
"""

    @staticmethod
    def get_coder_fast(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Fast, efficient responses
- Minimal but correct solutions
- Quick iteration
"""

    @staticmethod
    def get_explained(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Clear technical explanations
- Connect reasoning to implementation
- Practical examples
- Efficient communication
"""