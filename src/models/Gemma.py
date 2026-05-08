"""Gemma model configurations (2, 7b, etc)."""

from .config import ModelConfig


class Gemma:
    """Gemma model configurations."""
    
    normal = ModelConfig(
        name="Normal (Recommended)",
        config="""PARAMETER num_ctx 8192
PARAMETER num_predict 512
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1""",
        system="""You are a friendly and helpful assistant. Provide clear, thoughtful responses."""
    )
    
    tweak = ModelConfig(
        name="Tweak (Experimental)",
        config="""PARAMETER num_ctx 16384
PARAMETER num_predict 2048
PARAMETER temperature 0.5
PARAMETER top_p 0.95
PARAMETER top_k 50
PARAMETER repeat_penalty 1.05""",
        system="""You are a knowledgeable assistant with deep expertise. Provide comprehensive, nuanced responses."""
    )
    
    @staticmethod
    def get_all():
        return {
            "normal": Gemma.normal,
            "tweak": Gemma.tweak,
        }
