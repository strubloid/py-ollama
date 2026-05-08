"""
Interactive command-line interface for creating customized Ollama models.

Provides the main entry point and interactive flow for the tool.
"""

import sys
from typing import Optional

from . import presets as presets_module
from . import ollama
from . import modelfile


def display_menu(items: list[str], title: str = "") -> Optional[str]:
    """
    Display a numbered menu and get user selection.

    Args:
        items: List of items to display.
        title: Optional title to display above the menu.

    Returns:
        The selected item, or None if user cancels.
    """
    if title:
        print(f"\n{title}")

    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")

    while True:
        try:
            choice = input("\nEnter your choice (number): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(items):
                return items[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(items)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_string_input(prompt: str, allow_empty: bool = False) -> str:
    """
    Get string input from user with validation.

    Args:
        prompt: The prompt to display.
        allow_empty: If False, reject empty input.

    Returns:
        The user's input (stripped).
    """
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Input cannot be empty. Please try again.")


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    print("=" * 60)
    print("Ollama Tweak Advanced - Create Customized Models")
    print("=" * 60)

    # Step 1: Check if ollama is installed
    try:
        if not ollama.check_ollama_installed():
            print(
                "\nError: 'ollama' command not found.\n"
                "Please install Ollama from https://ollama.ai"
            )
            return 1
    except Exception as e:
        print(f"\nError checking Ollama installation: {e}")
        return 1

    # Step 2: Get available models
    try:
        available_models = ollama.get_available_models()
    except ollama.OllamaError as e:
        print(f"\nError: {e}")
        return 1

    if not available_models:
        print("\nNo models found. Please pull a model first with: ollama pull <model>")
        return 1

    # Step 3: Select base model
    print("\n" + "=" * 60)
    selected_model = display_menu(available_models, title="Select base model:")
    if not selected_model:
        print("No model selected. Exiting.")
        return 1

    print(f"\n✓ Selected base model: {selected_model}")

    # Step 4: Get new model name
    print("\n" + "=" * 60)
    new_model_name = get_string_input("Enter new model name: ")
    print(f"✓ New model name: {new_model_name}")

    # Step 5: Select configuration preset
    preset_names = presets_module.list_preset_names()
    print("\n" + "=" * 60)
    selected_preset_name = display_menu(
        preset_names,
        title="Select configuration preset:",
    )
    if not selected_preset_name:
        print("No preset selected. Exiting.")
        return 1

    selected_preset = presets_module.get_preset_by_name(selected_preset_name)
    if not selected_preset:
        print(f"Error: Preset '{selected_preset_name}' not found.")
        return 1

    print(f"✓ Selected preset: {selected_preset.name}")

    # Step 6: Build Modelfile content
    try:
        modelfile_content = modelfile.build_modelfile_content(
            base_model=selected_model,
            config_params=selected_preset.config,
            system_prompt=selected_preset.system,
        )
    except modelfile.ModelfileError as e:
        print(f"\nError building Modelfile: {e}")
        return 1

    # Step 7: Display Modelfile for review
    print("\n" + "=" * 60)
    print("Generated Modelfile:")
    print("=" * 60)
    print(modelfile_content)
    print("=" * 60)

    # Step 8: Confirm before creating
    confirm = input(
        f"\nProceed to create model '{new_model_name}'? (yes/no): "
    ).strip().lower()
    if confirm not in ("yes", "y"):
        print("Cancelled. Exiting.")
        return 0

    # Step 9: Create the model
    print(f"\nCreating model '{new_model_name}'...")
    try:
        with modelfile.TemporaryModelfile(modelfile_content) as tmp_path:
            ollama.create_model(new_model_name, tmp_path)
        # Modelfile is automatically cleaned up when exiting the with block
        print(
            f"\n✓ Model '{new_model_name}' created successfully!\n"
            f"Try it with: ollama run {new_model_name}"
        )
        return 0
    except ollama.OllamaError as e:
        print(f"\nError creating model: {e}")
        return 1
    except modelfile.ModelfileError as e:
        print(f"\nError managing temporary file: {e}")
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
