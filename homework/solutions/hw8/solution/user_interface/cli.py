import requests
from starlette.status import (
    HTTP_200_OK,
)
from solution.user_interface.cli_helpers import (
    add_transaction_ui,
    remove_transaction_ui,
)

API_BASE_URL = "http://localhost:8000"
ERROR_SERVER = "Server returned an error."
ERROR_CONNECTION = "Cannot connect to the server. Make sure the API is running."


def run_cli() -> None:
    """Start the CLI loop for the budget planner."""

    while True:
        user_choice = main_menu()
        if handle_user_choice(user_choice):
            break


def main_menu() -> str:
    menu_lines = [
        "\n|==================|",
        "|  Budget Planner  |",
        "|==================|",
        "|1. Add Income     |",
        "|2. Add Expense    |",
        "|3. View Summary   |",
        "|4. Remove Income  |",
        "|5. Remove Expense |",
        "|6. Clear All Data |",
        "|7. Exit           |",
        "|==================|",
    ]
    for line in menu_lines:
        print(line)
    return input("\nChoose an option (1-7): ").strip()


def handle_user_choice(choice: str) -> bool:
    """Handle the user's menu choice. Returns True if should exit."""

    if choice == "7":
        print("Good Bye :)")
        return True

    actions = {
        "1": add_income_ui,
        "2": add_expense_ui,
        "3": summary_ui,
        "4": remove_income_ui,
        "5": remove_expense_ui,
        "6": clear_all_ui,
    }

    action = actions.get(choice)

    if action is None:
        print("\nEnter a valid number between 1 and 7.")
        return False

    action()
    return False


def add_income_ui() -> None:
    """Prompt the user to add a new income and update the budget."""
    add_transaction_ui("income")


def add_expense_ui() -> None:
    """Prompt the user to add a new expense and update the budget."""
    add_transaction_ui("expense")


def summary_ui() -> None:
    """Display the current budget summary including incomes and expenses."""
    endpoint = f"{API_BASE_URL}/summary"
    try:
        response = requests.get(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return
    if response.status_code == HTTP_200_OK:
        print(response.text)
    else:
        print(f"{ERROR_SERVER} (Status code: {response.status_code})")


def remove_income_ui() -> None:
    """Prompt the user to remove an income by description or index."""
    remove_transaction_ui("income")


def remove_expense_ui() -> None:
    """Prompt the user to remove an expense by description or index."""
    remove_transaction_ui("expense")


def clear_all_ui() -> None:
    """Clear all incomes and expenses from the budget."""
    endpoint = f"{API_BASE_URL}/clear"
    try:
        response = requests.delete(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return
    if response.status_code == HTTP_200_OK:
        print(response.json()["message"])
    else:
        print(f"{ERROR_SERVER} (Status code: {response.status_code})")
