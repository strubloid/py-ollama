# Contributing

Thank you for your interest in contributing to Ollama Tweak Advanced!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ollama-tweak-advanced.git
   cd ollama-tweak-advanced
   ```

2. Install in development mode with dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Verify your setup:
   ```bash
   pytest tests/
   ```

## Code Quality Standards

We follow these standards:

- **Type Hints**: All functions must have type annotations
- **Docstrings**: All modules, classes, and public functions must have docstrings
- **Code Style**: Black formatting (100-char line length)
- **Linting**: Ruff checks
- **Testing**: Comprehensive test coverage

## Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes and add tests for new functionality

3. Run the full test suite:
   ```bash
   pytest tests/ -v
   ```

4. Run code quality checks:
   ```bash
   black src/ tests/
   ruff check src/ tests/
   mypy src/ollama_tweak_advanced
   ```

5. Commit with clear messages:
   ```bash
   git commit -m "Add my feature with clear description"
   ```

6. Push and create a pull request

## Testing

Run tests with:

```bash
pytest tests/
```

Run with coverage report:

```bash
pytest tests/ --cov=src/ollama_tweak_advanced --cov-report=html
```

## Guidelines

- Keep changes focused and atomic
- Update documentation for new features
- Add tests for all new code
- Follow the existing code style
- Write clear commit messages
- Be respectful and collaborative

## Code Organization

- **presets.py**: Preset definitions (add new presets here)
- **ollama.py**: Ollama CLI interaction
- **modelfile.py**: Modelfile generation and file handling
- **cli.py**: Interactive CLI flow
- **tests/**: All test files

## Questions?

Open an issue or start a discussion. We're happy to help!

---

Thank you for contributing!
