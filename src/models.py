"""
Model-specific configurations for Ollama models.

Each model has two configuration profiles:
- normal: Stable, recommended settings for production use
- tweak: Experimental settings for testing and optimization
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    """Configuration for a specific model variant."""
    name: str
    config: str  # PARAMETER settings
    system: str  # System prompt


class OllamaModelConfigs:
    """Base class for model-specific configurations."""
    
    @staticmethod
    def detect_model_family(model_name: str) -> str:
        """
        Detect model family from model name.
        
        Args:
            model_name: Model name (e.g., 'llama2:latest', 'deepseek-coder')
            
        Returns:
            Model family name (lowercase)
        """
        base = model_name.lower().split(':')[0]
        return base
    
    @staticmethod
    def get_configs_for_model(model_name: str) -> dict:
        """
        Get normal and tweak configs for a model.
        
        Args:
            model_name: Model name
            
        Returns:
            Dictionary with 'normal' and 'tweak' configs
        """
        family = OllamaModelConfigs.detect_model_family(model_name)
        
        # Map model families to their config classes
        if 'llama' in family:
            return LlamaConfigs.get_all()
        elif 'deepseek' in family:
            return DeepseekConfigs.get_all()
        elif 'qwen' in family:
            return QwenConfigs.get_all()
        elif 'gemma' in family:
            return GemmaConfigs.get_all()
        elif 'devstral' in family or 'mistral' in family:
            return MistralConfigs.get_all()
        else:
            # Default balanced config for unknown models
            return DefaultConfigs.get_all()


class LlamaConfigs:
    """Llama model configurations (2, 2.7b, 3, etc)."""
    
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
            "normal": LlamaConfigs.normal,
            "tweak": LlamaConfigs.tweak,
        }


class DeepseekConfigs:
    """Deepseek model configurations (coder, etc)."""
    
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
            "normal": DeepseekConfigs.normal,
            "tweak": DeepseekConfigs.tweak,
        }


class QwenConfigs:
    """Qwen model configurations (2.5-coder, etc)."""
    
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
            "normal": QwenConfigs.normal,
            "tweak": QwenConfigs.tweak,
        }


class GemmaConfigs:
    """Gemma model configurations (2, 7b, etc)."""
    
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
            "normal": GemmaConfigs.normal,
            "tweak": GemmaConfigs.tweak,
        }


class MistralConfigs:
    """Mistral/Devstral model configurations."""
    
    normal = ModelConfig(
        name="Normal (Recommended)",
        config="""PARAMETER num_ctx 4096
PARAMETER num_predict 512
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1""",
        system="""You are a helpful assistant. Provide concise and accurate responses."""
    )
    
    tweak = ModelConfig(
        name="Tweak (Experimental)",
        config="""PARAMETER num_ctx 8192
PARAMETER num_predict 1024
PARAMETER temperature 0.8
PARAMETER top_p 0.95
PARAMETER top_k 50
PARAMETER repeat_penalty 1.05""",
        system="""You are a comprehensive assistant. Provide detailed explanations and consider all relevant aspects."""
    )
    
    @staticmethod
    def get_all():
        return {
            "normal": MistralConfigs.normal,
            "tweak": MistralConfigs.tweak,
        }


class DefaultConfigs:
    """Default balanced configurations for unknown models."""
    
    normal = ModelConfig(
        name="Normal (Balanced)",
        config="""PARAMETER num_ctx 4096
PARAMETER num_predict 512
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1""",
        system="""You are a helpful assistant. Provide clear, accurate, and thoughtful responses."""
    )
    
    tweak = ModelConfig(
        name="Tweak (Creative)",
        config="""PARAMETER num_ctx 8192
PARAMETER num_predict 1024
PARAMETER temperature 0.9
PARAMETER top_p 0.95
PARAMETER top_k 50
PARAMETER repeat_penalty 1.05""",
        system="""You are a creative assistant. Think outside the box, be innovative, and explore unconventional approaches."""
    )
    
    @staticmethod
    def get_all():
        return {
            "normal": DefaultConfigs.normal,
            "tweak": DefaultConfigs.tweak,
        }
