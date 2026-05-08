# Agents

## Package Layout

Source is in `src/`, but the package has **no namespace package** — modules are imported directly:
```python
import cli
import models
import presets
import helpers
import ai.ollama
import ai.modelfile
```
Do NOT use `from ollama_tweak_advanced import ...`.

Entrypoint: `py-ollama = "cli:main"` (defined in `pyproject.toml`).

## Directory Structure

```
src/
├── cli.py              # Entry point, interactive flow
├── presets.py          # Preset configurations (Balanced, Coder, etc.)
├── helpers/
│   ├── __init__.py
│   └── default_helpers.py  # display_menu, display_config_options, validate_ollama, etc.
├── models/
│   ├── __init__.py     # Exports detect_model_family, get_configs_for_model
│   ├── config.py       # ModelConfig dataclass with get_params_table()
│   ├── OllamaModelConfig.py
│   ├── Llama.py        # normal, tweak configs
│   ├── Deepseek.py
│   ├── Qwen.py
│   ├── Gemma.py
│   ├── Mistral.py      # Also handles Devstral
│   └── Default.py
└── ai/
    ├── ollama/__init__.py    # check_ollama_installed, get_available_models, create_model
    └── modelfile/__init__.py  # build_modelfile_content, TemporaryModelfile
```

## Dev Commands

```bash
# Test
pytest tests/

# Lint
ruff check src/ tests/

# Format (line-length 100)
black src/ tests/

# Type check (targets py39)
mypy src/
```

## Configuration System

- Each model family (Llama, Deepseek, Qwen, Gemma, Mistral, Default) has `normal` and `tweak` configs
- `get_configs_for_model()` merges base configs with presets from `presets.py`
- `display_config_options()` shows a table with: #, Name, num_ctx, temperature, num_predict

## Test Setup

`tests/conftest.py` manually adds `src/` to `sys.path` to resolve the flat module imports.