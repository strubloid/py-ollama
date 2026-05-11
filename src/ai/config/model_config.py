"""Model family detection and configuration lookup."""

import re


def detect_model_family(model_name: str) -> str:
    """
    Detect model family from model name.

    Args:
        model_name: Model name (e.g., 'llama2:latest', 'deepseek-coder')

    Returns:
        Model family name (lowercase)
    """
    name = model_name.lower().split(':')[0]

    patterns = {
        'llama': r'llama',
        'deepseek': r'deepseek',
        'qwen': r'qwen',
        'gemma': r'gemma',
        'mistral': r'mistral',
        'devstral': r'devstral',
    }

    for family, pattern in patterns.items():
        if re.search(pattern, name):
            return family

    return name


__all__ = [
    "detect_model_family",
]