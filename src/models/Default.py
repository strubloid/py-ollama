"""Default balanced configuration for unknown models."""

from .config import ModelConfig


class Default:
    """Default balanced configuration for unknown models."""
    
    normal = ModelConfig(
        name="Normal (Recommended)",
        config="""PARAMETER num_ctx 4096
PARAMETER num_predict 512
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1""",
        system="""You are a helpful assistant. Provide clear and useful responses."""
    )
    
    tweak = ModelConfig(
        name="Tweak (Experimental)",
        config="""PARAMETER num_ctx 8192
PARAMETER num_predict 1024
PARAMETER temperature 0.5
PARAMETER top_p 0.95
PARAMETER top_k 50
PARAMETER repeat_penalty 1.05""",
        system="""You are an advanced assistant. Provide detailed and thoughtful responses."""
    )
    
    @staticmethod
    def get_all():
        return {
            "normal": Default.normal,
            "tweak": Default.tweak,
        }
