from solution.business_logic.budget import Budget
from solution.user_interface.cli_helpers import (
    add_transaction_ui,
    remove_transaction_ui,
)


def run_cli() -> None:
    """Start the CLI loop for the budget planner."""

    budget = Budget()
    while True:
        user_choice = main_menu()
        if handle_user_choice(budget, user_choice):
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


def handle_user_choice(budget: Budget, choice: str) -> bool:
    """Handle the user's menu choice. Returns True if should exit."""

    actions = {
        "1": add_income_ui,
        "2": add_expense_ui,
        "3": summary_ui,
        "4": remove_income_ui,
        "5": remove_expense_ui,
        "6": clear_all_ui,
        "7": lambda bye: print("Good Bye :)"),
    }

    action = actions.get(choice)
    if action is None:
        print("\nEnter a valid number between 1 and 7.")
        return False

    action(budget)
    return choice == "7"


def add_income_ui(budget: Budget) -> None:
    """Prompt the user to add a new income and update the budget."""
    add_transaction_ui(budget, "income")


def add_expense_ui(budget: Budget) -> None:
    """Prompt the user to add a new expense and update the budget."""
    add_transaction_ui(budget, "expense")


def summary_ui(budget: Budget) -> None:
    """Display the current budget summary including incomes and expenses."""
    print(budget.summary())


def remove_income_ui(budget: Budget) -> None:
    """Prompt the user to remove an income by description or index."""
    remove_transaction_ui(budget, "income")


def remove_expense_ui(budget: Budget) -> None:
    """Prompt the user to remove an expense by description or index."""
    remove_transaction_ui(budget, "expense")


def clear_all_ui(budget: Budget) -> None:
    """Clear all incomes and expenses from the budget."""

    budget.clear_all()
    print("Budget Cleared successfully!")
