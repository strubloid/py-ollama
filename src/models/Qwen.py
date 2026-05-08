"""Qwen model configurations (2.5-coder, etc)."""

from .config import ModelConfig


class Qwen:
    """Qwen model configurations."""
    
    normal = ModelConfig(
        name="Normal (Recommended)",
        config="""PARAMETER num_ctx 8192
PARAMETER num_predict 1024
PARAMETER temperature 0.3
PARAMETER top_p 0.8
PARAMETER top_k 25
PARAMETER repeat_penalty 1.1""",
        system="""You are a helpful code assistant. Provide practical solutions with explanations."""
    )
    
    tweak = ModelConfig(
        name="Tweak (Experimental)",
        config="""PARAMETER num_ctx 12288
PARAMETER num_predict 2048
PARAMETER temperature 0.15
PARAMETER top_p 0.9
PARAMETER top_k 35
PARAMETER repeat_penalty 1.05""",
        system="""You are an expert code assistant. Provide in-depth solutions with best practices and alternative approaches."""
    )
    
    @staticmethod
    def get_all():
        return {
            "normal": Qwen.normal,
            "tweak": Qwen.tweak,
        }
