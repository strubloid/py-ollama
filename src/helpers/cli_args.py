"""CLI argument parsing and resolution for inline mode."""

import subprocess
import sys
from typing import NamedTuple

import ai
from ai.models import get_configs_for_model


class CliArgs(NamedTuple):
    """Parsed command-line arguments."""
    model: str
    new_name: str
    config: str


def is_inline_mode() -> bool:
    """Check if CLI is running in inline/non-interactive mode."""
    return len(sys.argv) > 1


def parse_arguments() -> CliArgs:
    """Parse CLI arguments and return CliArgs instance."""
    if len(sys.argv) != 4:
        raise ValueError(
            f"Expected 3 arguments (model, name, config), got {len(sys.argv) - 1}\n"
            f"Usage: py-ollama <model> <name> <config>\n"
            f"  model: model name or index (e.g., gemma2, llama3, 1)\n"
            f"  name:  new model name\n"
            f"  config: config name or index (e.g., normal, coder, 1)"
        )

    return CliArgs(
        model=sys.argv[1],
        new_name=sys.argv[2],
        config=sys.argv[3],
    )


def get_available_models() -> list[str]:
    """Get list of installed models from ollama list."""
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ai.OllamaCommandError("Failed to get model list")

    models = []
    for line in result.stdout.split("\n"):
        line = line.strip()
        if not line or line.startswith("NAME") or line.startswith("---"):
            continue
        name = line.split()[0]
        if name:
            models.append(name)
    return models


def resolve_model(model_input: str, available_models: list[str]) -> str:
    """Resolve model input to actual model name (index or partial match)."""
    if model_input.isdigit():
        index = int(model_input) - 1
        if 0 <= index < len(available_models):
            return available_models[index]
        raise ValueError(f"Invalid model index: {model_input}")

    # Exact match
    if model_input in available_models:
        return model_input

    # Partial match (e.g., "gemma2" matches "gemma2:latest")
    for model in available_models:
        if model.startswith(model_input) or model_input in model:
            return model

    # Not found - return as-is for pull attempt
    return model_input


def resolve_config(config_input: str, model_name: str) -> str:
    """Resolve config input to config key (index or name)."""
    # Derive numeric indices from actual config keys
    configs = get_configs_for_model(model_name, "temp")
    config_keys = list(configs.keys())

    # Numeric index
    if config_input.isdigit():
        index = int(config_input) - 1
        if 0 <= index < len(config_keys):
            return config_keys[index]
        raise ValueError(
            f"Invalid config index: {config_input}\n"
            f"Valid indices: 1-{len(config_keys)}"
        )

    # Direct name match
    if config_input.lower() in config_keys:
        return config_input.lower()

    raise ValueError(
        f"Invalid config: {config_input}\n"
        f"Valid: {', '.join(config_keys)}, or 1-{len(config_keys)}"
    )


def ensure_model_installed(model: str) -> None:
    """Ensure model is installed, pull if needed."""
    available = ai.ollama.get_available_models()
    if model in available:
        return

    print(f"Model '{model}' not found locally.")
    response = input(f"Pull '{model}' from Ollama? (yes/no): ").strip().lower()
    if response not in ("yes", "y"):
        raise ValueError("Model not available")

    print(f"Pulling '{model}'...")
    result = subprocess.run(
        ["ollama", "pull", model],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ai.OllamaCommandError(f"Failed to pull model: {result.stderr}")
    print(f"✓ Successfully pulled '{model}'")


def run_inline(args: CliArgs) -> int:
    """Run CLI in inline/non-interactive mode."""
    print("=" * 60)
    print("Ollama Tweak Advanced V2.0 - Inline Mode")
    print("=" * 60)

    import helpers
    available_models = helpers.validate_ollama()

    resolved_model = resolve_model(args.model, available_models)
    print(f"==> Using model: {resolved_model}")

    if resolved_model not in available_models:
        print(f"Model '{resolved_model}' not found locally. Pulling...")
        result = subprocess.run(
            ["ollama", "pull", resolved_model],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise ai.OllamaCommandError(f"Failed to pull model: {result.stderr}")
        print(f"✓ Successfully pulled '{resolved_model}'")

    config_key = resolve_config(args.config, resolved_model)
    print(f"==> Using config: {config_key}")

    model_configs = get_configs_for_model(resolved_model, args.new_name)
    selected_config = model_configs[config_key]

    modelfile_content = ai.build_modelfile_content(
        base_model=resolved_model,
        config_params=selected_config.config,
        system_prompt=selected_config.system,
    )

    print("\n" + "=" * 60 + "\nGenerated modelfile content:\n" + "=" * 60 + "\n")
    print(modelfile_content)
    print()

    print(f"Creating model '{args.new_name}'...")
    with ai.TemporaryModelfile(modelfile_content) as tmp_path:
        ai.create_model(args.new_name, tmp_path)

    print(f"\n✓ Model '{args.new_name}' created successfully!\n")
    print(f"Try it with: ollama run {args.new_name}")

    return 0