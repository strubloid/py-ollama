"""Deepseek model configurations (coder, etc)."""

from .config import ModelConfig


class Deepseek:
    """Deepseek model configurations."""
    
    normal = ModelConfig(
        name="Normal (Recommended)",
        config="""PARAMETER num_ctx 8192
PARAMETER num_predict 1024
PARAMETER temperature 0.05
PARAMETER top_p 0.7
PARAMETER top_k 20
PARAMETER repeat_penalty 1.12""",
        system="""You are a code-focused AI assistant. Provide accurate, working code solutions.
Focus on:
- Correctness and best practices
- Clear, commented code
- Minimal, focused changes"""
    )
    
    tweak = ModelConfig(
        name="Tweak (Experimental)",
        config="""PARAMETER num_ctx 16384
PARAMETER num_predict 4096
PARAMETER temperature 0.1
PARAMETER top_p 0.85
PARAMETER top_k 30
PARAMETER repeat_penalty 1.08""",
        system="""You are an advanced code assistant. Provide comprehensive solutions with:
- Detailed explanations
- Multiple approaches when relevant
- Edge case handling
- Performance considerations"""
    )
    
    @staticmethod
    def get_all():
        return {
            "normal": Deepseek.normal,
            "tweak": Deepseek.tweak,
        }
