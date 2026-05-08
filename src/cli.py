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
        
        ## loading the available models from 'ollama ls' and validating Ollama installation
        available_models = helpers.validate_ollama()

        ## getting the model and the name of it
        print("\n" + "=" * 60)
        selected_model = helpers.display_menu(available_models, title="Select base model:")
        print("\n" + "=" * 60)
        new_model_name = helpers.get_string_input("Enter new model name: ")
        # Get the model configurations for the selected model and detect the model family.
        model_configs = models.OllamaModelConfigs.get_configs_for_model(selected_model)
        # Detect model family and filter configurations based on the selected model.
        config_options = list(model_configs.keys())
        # Display detected model family and available configurations for the selected model.
        model_family = models.OllamaModelConfigs.detect_model_family(selected_model)
        print(f"\n📍 Detected model family: {model_family}")

        ## Display configuration options for the detected model family and let the user select one.
        config_names = [model_configs[opt].name for opt in config_options]
        ## Display the configuration options for the detected model family and let the user select one.
        selected_config_name = helpers.display_menu(config_names, title="Available configurations:")
        
        ## Validate the selected configuration and get the corresponding config key to retrieve the config details.
        selected_config_key = helpers.validate_config_selection(model_configs, selected_config_name)

        ## loads the selected configuration details
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