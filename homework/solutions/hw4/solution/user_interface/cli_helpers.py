def print_error(error: Exception | str) -> None:
    """Print an error message."""
    print(f"Error: {error}")


def handle_remove(remove_item_type: str, remove_method: str) -> int | str:
    """Return description or index for removing an item."""
    match remove_method:
        case "1":
            return input(f"Enter {remove_item_type} description: ").strip()
        case "2":
            try:
                return int(input(f"Enter {remove_item_type} index: "))
            except ValueError as error:
                print(f"Error: {error}")
        case _:
            print("\nEnter a valid number 1 or 2")
    return 0
