# Agents

## Package Layout

Source is in `src/`, but the package has **no namespace package** — modules are imported directly:
```python
import cli
import ollama
import modelfile
import models
```
Do NOT use `from ollama_tweak_advanced import ...`.

Entrypoint: `py-ollama = "cli:main"` (defined in `pyproject.toml`).

## Dev Commands

```bash
# Test
pytest tests/

# Lint
ruff check src/ tests/

# Format (line-length 100)
black src/ tests/

# Type check (targets py39)
mypy src/ollama_tweak_advanced
```

## Architecture

- `cli.py`: Entry point, interactive flow (menu, input, confirmation)
- `models.py`: Model-family detection and configs (Llama, Deepseek, Qwen, Gemma, Mistral/Devstral, Default). Each family has `normal` and `tweak` configs.
- `modelfile.py`: Builds Modelfile content + `TemporaryModelfile` context manager
- `ollama.py`: Runs `ollama ls` and `ollama create`, parses output
- `presets.py`: Legacy preset definitions (original README docs reference these, but current flow uses `models.py`)

## Test Setup

`tests/conftest.py` manually adds `src/` to `sys.path` to resolve the flat module imports.

## Adding a New Model Family

1. Add a new `<Name>Configs` class in `src/models.py` with `normal` and `tweak` `ModelConfig` dataclasses
2. Add the detection case in `OllamaModelConfigs.get_configs_for_model()`
3. Configs follow this structure:
   - `config`: Multi-line string with `PARAMETER` directives
   - `system`: System prompt string
