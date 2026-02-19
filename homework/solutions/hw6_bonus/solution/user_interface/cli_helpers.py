import requests
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
)

API_BASE_URL = "http://localhost:8000"
ERROR_SERVER = "Server returned an error."
ERROR_CONNECTION = "Cannot connect to the server. Make sure the API is running."


def add_transaction_ui(transaction_type: str) -> None:
    """Prompt the user to add an income or expense via API."""

    description = input(f"Enter {transaction_type} description: ").strip()
    if not description:
        print("Description cannot be empty.")
        return
    try:
        amount = float(input(f"Enter {transaction_type} amount: "))
    except ValueError:
        print("Invalid input. Please enter a valid amount.")
        return
    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    data = {"description": description, "amount": amount}

    endpoint = f"{API_BASE_URL}/{transaction_type}"
    try:
        response = requests.post(endpoint, json=data)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_201_CREATED:
        print(f"{transaction_type.capitalize()} added successfully!")
    else:
        print(f"{ERROR_SERVER} (Status code: {response.status_code})")


def remove_transaction_ui(transaction_type: str) -> None:
    """Prompt the user to remove an income or expense by description or index."""

    while True:
        print(f"1. remove {transaction_type} by description")
        print(f"2. remove {transaction_type} by index")
        remove_method = input("Choose a remove method (index-description): ")
        if remove_method in ("1", "2"):
            description_or_index = handle_remove(transaction_type, remove_method)
            break
    endpoint = f"{API_BASE_URL}/{transaction_type}"
    try:
        if isinstance(description_or_index, int):
            response = requests.delete(f"{endpoint}/index/{description_or_index}")
        else:
            response = requests.delete(f"{endpoint}/description/{description_or_index}")

    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")
        return
    error_data = {}
    if response.status_code == HTTP_200_OK:
        print(f"{transaction_type.capitalize()} Removed successfully!")
    else:
        try:
            error_data = response.json()
        except ValueError:
            print(f"{ERROR_SERVER} (Status code: {response.status_code})")
            print(f"{error_data.get('detail', 'Unknown error')}")


def handle_remove(remove_item_type: str, remove_method: str) -> int | str | None:
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
            return None
    return None
