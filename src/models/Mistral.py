"""Mistral/Devstral model configurations."""

from .config import ModelConfig


class Mistral:
    """Mistral/Devstral model configurations."""
    
    normal = ModelConfig(
        name="Normal (Recommended)",
        config="""PARAMETER num_ctx 8192
PARAMETER num_predict 512
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER top_k 30
PARAMETER repeat_penalty 1.1""",
        system="""You are a precise and efficient assistant. Provide accurate, concise responses."""
    )
    
    tweak = ModelConfig(
        name="Tweak (Experimental)",
        config="""PARAMETER num_ctx 16384
PARAMETER num_predict 2048
PARAMETER temperature 0.2
PARAMETER top_p 0.95
PARAMETER top_k 40
PARAMETER repeat_penalty 1.05""",
        system="""You are an advanced assistant with high accuracy. Provide detailed, well-reasoned responses."""
    )
    
    @staticmethod
    def get_all():
        return {
            "normal": Mistral.normal,
            "tweak": Mistral.tweak,
        }
