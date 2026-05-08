"""Llama model configurations (2, 2.7b, 3, etc)."""

from .config import ModelConfig


class Llama:
    """Llama model configurations."""
    
    normal = ModelConfig(
        name="Normal (Recommended)",
        config="""PARAMETER num_ctx 4096
PARAMETER num_predict 512
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1""",
        system="""You are a helpful assistant. Provide clear, concise responses."""
    )
    
    tweak = ModelConfig(
        name="Tweak (Experimental)",
        config="""PARAMETER num_ctx 8192
PARAMETER num_predict 2048
PARAMETER temperature 0.5
PARAMETER top_p 0.95
PARAMETER top_k 50
PARAMETER repeat_penalty 1.05""",
        system="""You are an advanced assistant. Provide detailed, thoughtful responses with thorough explanations."""
    )
    
    @staticmethod
    def get_all():
        return {
            "normal": Llama.normal,
            "tweak": Llama.tweak,
        }
