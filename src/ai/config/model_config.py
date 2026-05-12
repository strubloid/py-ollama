import re


def detect_model_family(model_name: str) -> str:

    name = model_name.lower().split(':')[0]

    patterns = {
        'llama': r'llama',
        'deepseek': r'deepseek',
        'qwen': r'qwen',
        'qwen3': r'qwen3',
        'gemma': r'gemma',
        'mistral': r'mistral|ministral',
        'devstral': r'devstral',
        'granite': r'granite',
    }

    for family, pattern in patterns.items():
        if re.search(pattern, name):
            return family

    return name


__all__ = [
    "detect_model_family",
]