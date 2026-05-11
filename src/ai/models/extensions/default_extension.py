"""Default model extensions."""

from ..base import BaseModelFamily
from .base_extension import BaseExtension


class DefaultExtension(BaseExtension):
    """Extensions for Default model."""

    @staticmethod
    def get_normal(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Be helpful and practical
- Follow user instructions
- Provide clear responses
"""

    @staticmethod
    def get_coder(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Write correct, maintainable code
- Apply best practices
- Handle errors properly
- Test edge cases
"""

    @staticmethod
    def get_coder_fast(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Quick, working solutions
- Keep it simple
"""

    @staticmethod
    def get_explained(custom_name: str = "") -> str:
        identity = BaseModelFamily().getModelName(custom_name)
        return f"""[{identity}]
- Clear explanations
- Step-by-step reasoning
- Practical examples
"""