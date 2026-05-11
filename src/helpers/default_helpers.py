from typing import Optional

import ai.ollama
import ai.modelfile


class UserCancelledError(Exception):
    pass


def format_table(headers: list[str], rows: list[list[str]], col_padding: int = 2) -> str:
    """Format data as a text table."""
    if not rows:
        return ""

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    lines = []

    header_line = "  ".join(
        h.ljust(col_widths[i]) for i, h in enumerate(headers)
    )
    lines.append(header_line)

    separator = "  ".join("-" * w for w in col_widths)
    lines.append(separator)

    for row in rows:
        row_line = "  ".join(
            str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
        )
        lines.append(row_line)

    return "\n".join(lines)

## This will be used to display menus and get user input in the CLI.
## The display_menu function shows a numbered list of options and prompts 
# the user to select one by entering the corresponding number. 
# It validates the input and returns the selected item.
def display_config_options(model_configs: dict) -> str:
    """
    Display model configurations as a formatted table and return selection.

    Args:
        model_configs: Dictionary of config options with ModelConfig values.

    Returns:
        Selected config key.
    """
    headers = ["#", "Name", "num_ctx", "num_predict", "temp", "top_p", "top_k", "repeat_pen", "repeat_n"]
    rows = []
    config_list = list(model_configs.items())

    for i, (key, cfg) in enumerate(config_list, 1):
        params = cfg.get_params_table()
        param_dict = {name: value for name, value in params}

        rows.append([
            str(i),
            cfg.name,
            param_dict.get("num_ctx", "-"),
            param_dict.get("num_predict", "-"),
            param_dict.get("temperature", "-"),
            param_dict.get("top_p", "-"),
            param_dict.get("top_k", "-"),
            param_dict.get("repeat_penalty", "-"),
            param_dict.get("repeat_last_n", "-"),
        ])

    print("\nAvailable configurations:")
    print(format_table(headers, rows))
    print()

    while True:
        try:
            choice = input("Select configuration (number): ").strip()
            if choice == "":
                raise UserCancelledError()
            choice_num = int(choice)
            if 1 <= choice_num <= len(config_list):
                return config_list[choice_num - 1][0]
            else:
                print(f"Please enter a number between 1 and {len(config_list)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except (EOFError, KeyboardInterrupt):
            raise UserCancelledError()


def display_menu(items: list[str], title: str = "", show_table: bool = False, table_headers: list[str] = None, table_rows: list[list[str]] = None) -> str:
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


def confirm_and_create_model(model_name: str, modelfile_content: str) -> None:
    """
    Prompt user for confirmation, create model, and print result.

    Args:
        model_name: Name for the new model.
        modelfile_content: Content for the Modelfile.

    Raises:
        UserCancelledError: If user declines confirmation.
    """
    confirm = input(
        f"\nProceed to create model '{model_name}'? (yes/no): "
    ).strip().lower()
    if confirm not in ("yes", "y"):
        raise UserCancelledError()

    print(f"\nCreating model '{model_name}'...")

    with ai.modelfile.TemporaryModelfile(modelfile_content) as tmp_path:
        ai.ollama.create_model(model_name, tmp_path)

    print(
        f"\n✓ Model '{model_name}' created successfully!\n"
        f"Try it with: ollama run {model_name}"
    )