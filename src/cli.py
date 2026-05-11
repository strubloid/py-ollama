"""
Interactive command-line interface for creating customized Ollama models.

Provides the main entry point and interactive flow for the tool with
model-specific configurations optimized for each model family.
"""

import sys

import ai
import helpers
from ai.models import get_configs_for_model, detect_model_family


def main() -> int:
    try:
        # Display the main menu
        print("=" * 60)
        print("Ollama Tweak Advanced V2.0 - Create Customized Models")
        print("=" * 60)
        
        ## loading models
        available_models = helpers.validate_ollama()

        ## selecting a model
        selected_model = helpers.display_menu(available_models, title="Select base model:")
        print("=" * 60 + "\n")
        
        new_model_name = helpers.get_string_input("New tweaked model name: ")

        # get model family and configurations
        model_configs = get_configs_for_model(selected_model, new_model_name)
        model_family = detect_model_family(selected_model)
        print(f"==> Model: {model_family}")

        selected_config_key = helpers.display_config_options(model_configs)
        selected_config = model_configs[selected_config_key]
        print(f"\n✓ Selected configuration: {selected_config.name}")

        modelfile_content = ai.build_modelfile_content(
            base_model=selected_model,
            config_params=selected_config.config,
            system_prompt=selected_config.system,
        )
        
        ## formatting and displaying the generated modelfile content for confirmation
        print("\n" + "=" * 60 + "\n" + "Generated modelfile content:\n" + "=" * 60 + "\n")
        print(modelfile_content)

        # confirming and creating the new model
        helpers.confirm_and_create_model(new_model_name, modelfile_content)

        return 0

    except ai.ModelfileError as e:
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