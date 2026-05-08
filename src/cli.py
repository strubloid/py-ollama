"""
Interactive command-line interface for creating customized Ollama models.

Provides the main entry point and interactive flow for the tool with
model-specific configurations optimized for each model family.
"""

import sys

import helpers
import models
import ollama
import modelfile


def main() -> int:
    print("=" * 60)
    print("Ollama Tweak Advanced - Create Customized Models")
    print("=" * 60)

    try:
        if not ollama.check_ollama_installed():
            print(
                "\nError: 'ollama' command not found.\n"
                "Please install Ollama from https://ollama.ai"
            )
            return 1

        available_models = ollama.get_available_models()

        if not available_models:
            print("\nNo models found. Please pull a model first with: ollama pull <model>")
            return 1

        print("\n" + "=" * 60)
        selected_model = helpers.display_menu(available_models, title="Select base model:")
        if not selected_model:
            print("No model selected. Exiting.")
            return 1

        print(f"\n✓ Selected base model: {selected_model}")

        print("\n" + "=" * 60)
        new_model_name = helpers.get_string_input("Enter new model name: ")
        print(f"✓ New model name: {new_model_name}")

        print("\n" + "=" * 60)
        model_configs = models.OllamaModelConfigs.get_configs_for_model(selected_model)
        config_options = list(model_configs.keys())
        model_family = models.OllamaModelConfigs.detect_model_family(selected_model)
        print(f"\n📍 Detected model family: {model_family}")
        print("Available configurations for this model:")

        config_names = [model_configs[opt].name for opt in config_options]
        selected_config_name = helpers.display_menu(config_names)

        if not selected_config_name:
            print("No configuration selected. Exiting.")
            return 1

        selected_config_key = next(
            (key for key, config in model_configs.items() if config.name == selected_config_name),
            None
        )

        if not selected_config_key:
            print("Error: Configuration not found.")
            return 1

        selected_config = model_configs[selected_config_key]
        print(f"✓ Selected configuration: {selected_config.name}")

        modelfile_content = modelfile.build_modelfile_content(
            base_model=selected_model,
            config_params=selected_config.config,
            system_prompt=selected_config.system,
        )

        print("\n" + "=" * 60)
        print("Generated Modelfile:")
        print("=" * 60)
        print(modelfile_content)
        print("=" * 60)

        confirm = input(
            f"\nProceed to create model '{new_model_name}'? (yes/no): "
        ).strip().lower()
        if confirm not in ("yes", "y"):
            print("Cancelled. Exiting.")
            return 0

        print(f"\nCreating model '{new_model_name}'...")

        with modelfile.TemporaryModelfile(modelfile_content) as tmp_path:
            ollama.create_model(new_model_name, tmp_path)

        print(
            f"\n✓ Model '{new_model_name}' created successfully!\n"
            f"Try it with: ollama run {new_model_name}"
        )

        return 0

    except ollama.OllamaError as e:
        print(f"\nError: {e}")
        return 1
    except modelfile.ModelfileError as e:
        print(f"\nError: {e}")
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())