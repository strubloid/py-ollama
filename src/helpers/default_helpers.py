from typing import Optional

import ai.ollama


class UserCancelledError(Exception):
    pass

## This will be used to display menus and get user input in the CLI.
## The display_menu function shows a numbered list of options and prompts 
# the user to select one by entering the corresponding number. 
# It validates the input and returns the selected item.
def display_menu(items: list[str], title: str = "") -> str:
    if title:
        print(f"\n{title}")

    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")

    while True:
        try:
            choice = input("\nEnter your choice (number): ").strip()
            if choice == "":
                raise UserCancelledError()
            choice_num = int(choice)
            if 1 <= choice_num <= len(items):
                return items[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(items)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except (EOFError, KeyboardInterrupt):
            raise UserCancelledError()

## The get_string_input function prompts the user for input and ensures that it is not empty (unless allow_empty is True).
## It keeps asking until valid input is provided. This is used in the CLI to get the new model name and other string inputs from the user.
def get_string_input(prompt: str, allow_empty: bool = False) -> str:
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Input cannot be empty. Please try again.")

## This function is used in the client to validate that Ollama is installed and 
# to get the list of available models. 
# Also: It raises exceptions if there are issues, which are caught in the main 
# function to display user-friendly messages.
def validate_config_selection(model_configs: dict, selected_config_name: str) -> str:
    config_key = next(
        (key for key, config in model_configs.items() if config.name == selected_config_name),
        None
    )
    if not config_key:
        raise ValueError("Configuration not found.")
    return config_key

## This function checks if Ollama is installed and retrieves the list of available models.
## It raises exceptions if Ollama is not installed or if no models are found, which are handled in the main function to provide feedback to the user.
def validate_ollama() -> list[str]:
    if not ai.ollama.check_ollama_installed():
        raise ai.ollama.OllamaError(
            "'ollama' command not found.\n"
            "Please install Ollama from https://ollama.ai"
        )

    available_models = ai.ollama.get_available_models()

    if not available_models:
        raise ai.ollama.OllamaError(
            "No models found. Please pull a model first with: ollama pull <model>"
        )

    return available_models