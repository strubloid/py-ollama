# Agents

## Coding Preferences

Always read [`AGENTS.PREFERENCES.md`](AGENTS.PREFERENCES.md) for:

- SOLID principles and design patterns
- Code organization and naming conventions
- Testing best practices
- Project-specific patterns and structure

---

## This Project - py-ollama

### Package Layout

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

### Directory Structure

Run `py-ollama-refresh` to update this structure.

```
src/
├── ai
│   ├── config
│   │   ├── __init__.py
│   │   ├── model_config.py
│   │   └── ollama_config.py
│   ├── modelfile
│   │   ├── __init__.py
│   │   ├── error.py
│   │   ├── modelfile.py
│   │   └── temporary.py
│   ├── models
│   │   ├── extensions
│   │   │   ├── base_extension.py
│   │   │   ├── deepseek_extension.py
│   │   │   ├── default_extension.py
│   │   │   ├── gemma_extension.py
│   │   │   ├── llama_extension.py
│   │   │   ├── mistral_extension.py
│   │   │   └── qwen_extension.py
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── deepseek.py
│   │   ├── default.py
│   │   ├── gemma.py
│   │   ├── llama.py
│   │   ├── mistral.py
│   │   └── qwen.py
│   ├── ollama
│   │   ├── __init__.py
│   │   ├── check.py
│   │   ├── client.py
│   │   ├── exceptions.py
│   │   └── ollama.py
│   ├── presets
│   │   ├── __init__.py
│   │   ├── balanced.py
│   │   ├── coder.py
│   │   ├── coder_balanced.py
│   │   ├── coder_fast.py
│   │   ├── creative.py
│   │   ├── long_context.py
│   │   └── model.py
│   └── __init__.py
├── helpers
│   ├── __init__.py
│   └── default_helpers.py
├── scripts
│   └── __init__.py
└── cli.py
```

### SOLID Package Patterns

Each package follows these rules:

- **One class/concept per file** - Each file has a single responsibility
- **`__init__.py` with public API** - Re-export from submodules for clean interface
- **Backwards-compatible wrapper** - Keep flat imports working (e.g., `ollama/ollama.py`)
- **Relative imports inside packages** - Use `from .exceptions import ...`
- **Separate files for** - Exceptions, helpers, main logic

### Import Patterns

| Pattern          | Example                                                            |
| ---------------- | ------------------------------------------------------------------ |
| Package import   | `from ai.ollama import OllamaClient`                               |
| Submodule import | `from ai.ollama.client import OllamaClient`                        |
| Direct function  | `from ai.ollama.check import check_ollama_installed`               |
| Via ai module    | `from ai import ollama; ollama.check_ollama_installed()`           |
| Model import     | `from ai.models import get_configs_for_model, detect_model_family` |
| Preset import    | `from ai.presets import PRESETS, list_preset_names`                |

### Naming Conventions

- **Avoid redundant suffixes** - Use `balanced.py` not `balanced_preset.py`, `model.py` not `model_presets.py`
- **Package folders** - Use singular (e.g., `ollama/`, `modelfile/`, not `ollamas/`, `modelfiles/`)
- **Dataclasses for data** - Use `@dataclass(frozen=True)` for immutable config objects
- **Abstract base classes** - Use ABC for interfaces (e.g., `BaseExtension`)

### Configuration System

- Each model family (Llama, Deepseek, Qwen, Gemma, Mistral, Default) has: `normal`, `coder`, `coder_fast`, `explained`
- Models use extensions for customizable behavior (via `_build_system` method)
- Extensions follow `BaseExtension` abstract class with: `get_normal()`, `get_coder()`, `get_coder_fast()`, `get_explained()`
- `get_configs_for_model()` merges base configs with presets
- Model detection via `detect_model_family()` in `ai/config/`

### Dev Commands

```bash
pytest tests/        # Test
ruff check src/       # Lint
black src/            # Format
mypy src/             # Type check
```

### Test Status

All tests passing (71 tests). Run `pytest tests/` to verify.

### Verification Commands

```bash
pytest tests/        # 71 tests
ruff check src/ tests/  # Lint
```
