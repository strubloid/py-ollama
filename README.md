# py-ollama

A clean Python CLI tool to create customized Ollama models from preset configurations with an interactive, user-friendly interface.

## Features

- 🎯 **Interactive CLI**: Easy-to-use numbered menus for selecting base models and presets
- 🔧 **Preset Configurations**: Six built-in presets optimized for different use cases:
  - **Balanced**: General-purpose tasks with moderate creativity and accuracy
  - **Coder**: Optimized for code generation with deterministic, focused output
  - **CoderFast**: Fast code generation with good quality (threading + batch optimization)
  - **CoderBalanced**: Balanced code generation with larger context window
  - **Creative**: Content generation with high temperature and diversity
  - **Long Context**: Multi-file changes and complex reasoning with large context
- 📋 **System Prompts**: Each preset includes a specialized system prompt to guide model behavior
- ✅ **Error Handling**: Graceful error messages for missing Ollama, no models, or invalid selections
- 🛡️ **Type-Safe**: Full type hints for better code quality and IDE support
- 🧪 **Well-Tested**: Comprehensive test suite (71 tests)
- 📦 **Clean Architecture**: Modular SOLID design with separation of concerns

## Installation

```bash
git clone https://github.com/yourusername/py-ollama.git
cd py-ollama
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Usage

### Basic Usage

```bash
py-ollama
```

The tool will guide you through:
1. Selecting a base model from `ollama ls`
2. Entering a name for your new customized model
3. Choosing a configuration preset
4. Reviewing the generated Modelfile
5. Confirming creation

## Project Structure

The current directory structure is maintained in [`AGENTS.md`](AGENTS.md). To update it after making changes:

```bash
py-ollama-refresh
```

## Package Architecture

The project follows SOLID principles with package-based architecture:

### `ai.ollama` - Ollama CLI Interaction

```python
from ai.ollama import check_ollama_installed, get_available_models, create_model
from ai.ollama import OllamaClient, OllamaError, OllamaNotFoundError, OllamaCommandError
```

### `ai.modelfile` - Modelfile Generation

```python
from ai.modelfile import build_modelfile_content, TemporaryModelfile, ModelfileError
```

### `ai.presets` - Preset Configurations

```python
from ai.presets import PRESETS, list_preset_names, get_preset_by_name
```

### `ai.models` - Model Configuration

```python
from ai.models import get_configs_for_model, detect_model_family
```

### `ai.config` - Configuration Helpers

```python
from ai.config import detect_model_family, ModelConfig
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
ruff check src/ tests/
black src/ tests/
mypy src/
```

### Refreshing Documentation

```bash
py-ollama-refresh  # Updates AGENTS.md with current directory structure
```

## Requirements

- Python 3.10 or higher
- Ollama installed and running ([Download](https://ollama.ai))
- At least one Ollama model available (`ollama pull <model>`)

## How It Works

1. **Detect Ollama**: Verify `ollama` command is available
2. **List Models**: Run `ollama ls` and parse model names
3. **Select Model**: Choose base model for customization
4. **Choose Preset**: Select from 6 preset configurations (Balanced, Coder, CoderFast, CoderBalanced, Creative, Long Context)
5. **Build Modelfile**: Combine base model + preset config + system prompt
6. **Create Model**: Run `ollama create <name> -f <modelfile>`
7. **Cleanup**: Remove temporary Modelfile
8. **Confirm Success**: Tell user how to use the new model

## Architecture

The project uses a package-based architecture following SOLID principles:
- Each package has `__init__.py` with public API re-exports
- Relative imports inside packages
- Separate files for exceptions, helpers, main logic
- Backwards-compatible wrapper modules for flat imports

## License

MIT License - see LICENSE file for details

---

**Built with Python 3.10+** | **MIT License**