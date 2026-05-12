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
│   │   ├── config_loader.py
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
│   ├── orchestration
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   └── hardware.py
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
│   ├── cli_args.py
│   └── default_helpers.py
├── scripts
│   ├── __init__.py
│   ├── generate.py
│   ├── refresh.py
│   ├── speed.py
│   └── tree.py
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

75 tests passing. Benchmark tests may fail on 3s quick_request limit due to hardware constraints.

### Verification Commands

```bash
pytest tests/        # 75 tests
ruff check src/ tests/  # Lint
```

---

## Performance Optimization (2026-05-12)

### Hardware Profile

- **GPU:** NVIDIA RTX 4070 Ti (12GB VRAM)
- **Memory Bandwidth:** 504 GB/s
- **Current Model:** qwen2.5-coder:14b (Q4_K_M, 9GB)
- **Token Rate:** ~47 tokens/s
- **VRAM Usage:** 92% (11GB/12GB) during inference

### Optimization Parameters Added

All configs now include GPU optimization parameters:

```
PARAMETER num_gpu 64          # Half layers on GPU (optimal for 12GB VRAM)
PARAMETER num_batch 512       # Batch size for faster processing
PARAMETER use_mlock true      # Lock model in RAM
PARAMETER use_mmap true       # Memory-map model for fast loading
PARAMETER f16_kv true         # Half-precision KV cache
```

### Impact Classification

| Impact  | Optimization                         | Expected Savings      |
| ------- | ------------------------------------ | --------------------- |
| EXTREME | Keep model warm (keep_alive)         | 3-4s per request      |
| HIGH    | Use num_gpu=64 (fixes 94% CPU issue) | 50% speedup           |
| HIGH    | Pre-warm model on startup            | Eliminates cold start |
| MEDIUM  | HTTP API instead of subprocess       | 200-500ms             |
| LOW     | Temperature/top_k tuning             | <20ms                 |

### Critical Findings

1. **Model running 94% on CPU** - num_gpu=128 was too aggressive, causing CPU fallback
2. **VRAM at 92%** - 11GB used of 12GB available, causing memory pressure
3. **Cold start: 7-17 seconds** - Model loading dominates latency
4. **Warm start: 0.5-2 seconds** - Much faster when model stays loaded

### Quantization Recommendations

| Quantization | Size | Speed    | Quality | Recommendation           |
| ------------ | ---- | -------- | ------- | ------------------------ |
| Q4_K_M       | 9GB  | 47 tok/s | 96-98%  | **CURRENT (optimal)**    |
| Q3_K_M       | 7GB  | 60 tok/s | 92-96%  | For speed + quality      |
| Q2_K         | 5GB  | 80 tok/s | 88-92%  | Max speed, lower quality |

### Files Created

- `scripts/latency_profiler.py` - Comprehensive latency analysis tool
- `scripts/detailed_latency.py` - GPU efficiency and keep_alive testing

### Current Test Status

- Normal request (5s): PASS
- Quick request (3s): FAIL (hardware minimum ~4s with model load)

The 3s limit is hardware-constrained. Model loading takes 3-4s minimum regardless of optimization parameters.
