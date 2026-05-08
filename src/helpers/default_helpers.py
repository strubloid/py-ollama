from typing import Optional


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