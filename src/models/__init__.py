"""
Model-specific configurations for Ollama models.

Each model has two configuration profiles:
- normal: Stable, recommended settings for production use
- tweak: Experimental settings for testing and optimization
"""

from .config import ModelConfig
from .Llama import Llama
from .Deepseek import Deepseek
from .Qwen import Qwen
from .Gemma import Gemma
from .Mistral import Mistral
from .Default import Default

__all__ = [
    "ModelConfig",
    "Llama",
    "Deepseek",
    "Qwen",
    "Gemma",
    "Mistral",
    "Default",
    "OllamaModelConfigs",
]


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
            return Llama.get_all()
        elif 'deepseek' in family:
            return Deepseek.get_all()
        elif 'qwen' in family:
            return Qwen.get_all()
        elif 'gemma' in family:
            return Gemma.get_all()
        elif 'devstral' in family or 'mistral' in family:
            return Mistral.get_all()
        else:
            # Default balanced config for unknown models
            return Default.get_all()
