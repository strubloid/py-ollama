"""
Interactive command-line interface for creating customized Ollama models.

Provides the main entry point and interactive flow for the tool with
model-specific configurations optimized for each model family.
"""

import sys

import helpers
import models
import ai.ollama
import ai.modelfile


def main() -> int:
    print("=" * 60)
    print("Ollama Tweak Advanced - Create Customized Models")
    print("=" * 60)

    try:

        available_models = helpers.validate_ollama()
        print("\n" + "=" * 60)

        selected_model = helpers.display_menu(available_models, title="Select base model:")
        print("\n" + "=" * 60)
        new_model_name = helpers.get_string_input("Enter new model name: ")
        model_configs = models.get_configs_for_model(selected_model)
        config_options = list(model_configs.keys())
        model_family = models.detect_model_family(selected_model)
        print(f"\n📍 Detected model family: {model_family}")

        config_names = [model_configs[opt].name for opt in config_options]
        selected_config_name = helpers.display_menu(config_names, title="Available configurations:")

        selected_config_key = helpers.validate_config_selection(model_configs, selected_config_name)

        selected_config = model_configs[selected_config_key]
        print(f"✓ Selected configuration: {selected_config.name}")

        modelfile_content = ai.modelfile.build_modelfile_content(
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

        with ai.modelfile.TemporaryModelfile(modelfile_content) as tmp_path:
            ai.ollama.create_model(new_model_name, tmp_path)

        print(
            f"\n✓ Model '{new_model_name}' created successfully!\n"
            f"Try it with: ollama run {new_model_name}"
        )

        return 0

    except ai.ollama.OllamaError as e:
        print(f"\nError: {e}")
        return 1
    except ai.modelfile.ModelfileError as e:
        print(f"\nError: {e}")
        return 1
    except helpers.UserCancelledError:
        print("\nCancelled. Exiting.")
        return 1
    except ValueError as e:
        print(f"\nError: {e}")
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())