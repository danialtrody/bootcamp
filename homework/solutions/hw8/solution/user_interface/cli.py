from solution.user_interface import account_cli
from solution.user_interface import transaction_cli


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
        "\n|==================================|",
        "|        Budget Planner CLI        |",
        "|==================================|",
        "|Available Sections:               |",
        "|                                  |",
        "|1. ACCOUNTS - Manage              |",
        "|2. TRANSACTIONS - Income/Expense  |",
        "|3. CATEGORIES - Types             |",
        "|4. TRANSFER - Move Money          |",
        "|5. REPORTS - Reports              |",
        "|6. DASHBOARD - Summary            |",
        "|7. NET WORTH - Total              |",
        "|8. PORTABILITY - Import/Export    |",
        "|9. EXIT                           |",
        "|==================================|",
    ]
    for line in menu_lines:
        print(line)
    return input("\nChoose an option (1-9): ").strip()


def handle_user_choice(choice: str) -> bool:
    """Handle the user's menu choice. Returns True if should exit."""

    if choice == "9":
        print("Good Bye :)")
        return True

    actions = {
        "1": account_cli.run_account_cli,
        "2": transaction_cli.run_transaction_cli
    }

    action = actions.get(choice)

    if action is None:
        print("\nEnter a valid number between 1 and 9.")
        return False

    action()
    return False
