# Ollama Tweak Advanced

A clean Python CLI tool that replaces the Bash `ollama-tweak-advanced` function. Create customized Ollama models from preset configurations with an interactive, user-friendly interface.

## Features

- 🎯 **Interactive CLI**: Easy-to-use numbered menus for selecting base models and presets
- 🔧 **Preset Configurations**: Seven built-in presets optimized for different use cases:
  - **Balanced**: General-purpose tasks with moderate creativity and accuracy
  - **Coder**: Optimized for code generation with deterministic, focused output
  - **CoderFast**: Fast code generation with good quality (threading + batch optimization)
  - **CoderBalanced**: Balanced code generation with larger context window
  - **Creative**: Content generation with high temperature and diversity
  - **Precise**: Analytical and mathematical tasks with very low temperature
  - **Long Context**: Multi-file changes and complex reasoning with large context
- 📋 **System Prompts**: Each preset includes a specialized system prompt to guide model behavior
- ✅ **Error Handling**: Graceful error messages for missing Ollama, no models, or invalid selections
- 🛡️ **Type-Safe**: Full type hints for better code quality and IDE support
- 🧪 **Well-Tested**: Comprehensive test suite for presets and Modelfile generation
- 📦 **Clean Architecture**: Modular design with separation of concerns

## Installation

### From Source

```bash
git clone https://github.com/yourusername/ollama-tweak-advanced.git
cd ollama-tweak-advanced
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Usage

### Basic Usage

Run the interactive CLI:

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

This will regenerate the directory tree in the documentation.

## Module Documentation

### `presets.py`

Defines all available configuration presets. Each preset is a frozen dataclass containing:
- `name`: Display name (e.g., "Balanced", "Coder")
- `config`: Multi-line string with PARAMETER directives
- `system`: System prompt for the model

**Key Functions:**
- `get_preset_by_name(name: str)`: Get a preset by name
- `list_preset_names()`: Get all available preset names

### `ollama.py`

Handles interaction with the Ollama CLI tool.

**Key Functions:**
- `check_ollama_installed()`: Check if Ollama is installed
- `get_available_models()`: Run `ollama ls` and parse model names
- `create_model(model_name, modelfile_path)`: Create a new model

**Exceptions:**
- `OllamaError`: Base exception for Ollama-related errors
- `OllamaNotFoundError`: Ollama command not found
- `OllamaCommandError`: Ollama command execution failed

### `modelfile.py`

Generates and manages Ollama Modelfiles with temporary file handling.

**Key Functions:**
- `build_modelfile_content(base_model, config_params, system_prompt)`: Build Modelfile content
- `write_temporary_modelfile(content)`: Write content to a temporary file
- `cleanup_modelfile(file_path)`: Delete a temporary Modelfile

**Classes:**
- `TemporaryModelfile`: Context manager for automatic cleanup

**Exceptions:**
- `ModelfileError`: Modelfile-related errors

### `cli.py`

Provides the interactive command-line interface.

**Key Functions:**
- `display_menu(items, title)`: Display a numbered menu and get user selection
- `get_string_input(prompt, allow_empty)`: Get validated string input
- `main()`: Main entry point

## Development

### Running Tests

```bash
pytest tests/
```

Run with coverage:

```bash
pytest tests/ --cov=src/ollama_tweak_advanced
```

### Code Quality

Format code with Black:

```bash
black src/ tests/
```

Lint with Ruff:

```bash
ruff check src/ tests/
```

Type check with mypy:

```bash
mypy src/ollama_tweak_advanced
```

## Requirements

- Python 3.9 or higher
- Ollama installed and running ([Download](https://ollama.ai))
- At least one Ollama model available (`ollama pull <model>`)

## How It Works

1. **Detect Ollama**: Verify `ollama` command is available
2. **List Models**: Run `ollama ls` and parse model names
3. **Interactive Selection**: Show numbered menus for user choice
4. **Build Modelfile**: Combine base model + preset config + system prompt
5. **Display for Review**: Show generated Modelfile content
6. **Create Model**: Run `ollama create <name> -f <modelfile>`
7. **Cleanup**: Remove temporary Modelfile
8. **Confirm Success**: Tell user how to use the new model

## Differences from Bash Version

- **No external dependencies**: Doesn't require `jq` or Bash-specific tools
- **Better error messages**: Descriptive, actionable error handling
- **Type safety**: Full type hints throughout
- **Modular design**: Reusable modules for importation in other projects
- **Cross-platform**: Works on Linux, macOS, and Windows (with Ollama installed)
- **Testable**: Comprehensive test suite ensures reliability

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! See CONTRIBUTING.md for details.

---

**Built with Python 3.9+** | **MIT License**
