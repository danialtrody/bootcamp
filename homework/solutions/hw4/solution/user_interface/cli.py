from solution.business_logic.budget import Budget
from solution.business_logic.income import Income
from solution.business_logic.expense import Expense
from solution.user_interface.cli_helpers import print_error, handle_remove


def run_cli() -> None:
    """Start the CLI loop for the budget planner."""

    budget = Budget()
    while True:
        user_choice = main_menu()
        if handle_user_choice(budget, user_choice):
            break


def main_menu() -> str:
    print("\n===== Budget Planner =====")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Summary")
    print("4. Remove Income")
    print("5. Remove Expense")
    print("6. Clear All Data")
    print("7. Exit")
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

    description = input("Enter income description: ").strip()

    try:
        amount = float(input("Enter income amount: "))
    except ValueError as error:
        print_error(error)
        return

    try:
        income = Income(description, amount)
    except ValueError as error:
        print_error(error)
        return

    try:
        budget.add_income(income)
    except ValueError as error:
        print_error(error)
        return

    print("Income added successfully!")


def add_expense_ui(budget: Budget) -> None:
    """Prompt the user to add a new expense and update the budget."""

    description = input("Enter expense description: ").strip()

    try:
        amount = float(input("Enter expense amount: "))
    except ValueError as error:
        print_error(error)
        return

    try:
        expense = Expense(description, amount)
    except ValueError as error:
        print_error(error)
        return
    try:
        budget.add_expense(expense)
    except ValueError as error:
        print_error(error)
        return

    print("Expense added successfully!")


def summary_ui(budget: Budget) -> None:
    """Display the current budget summary including incomes and expenses."""
    print(budget.summary())


def remove_income_ui(budget: Budget) -> None:
    """Prompt the user to remove an income by description or index."""

    while True:
        print("1. remove income by description")
        print("2. remove income by index")
        remove_method = input("Choose a remove method (index-description): ")
        if remove_method:
            description_or_index = handle_remove("income", remove_method)
            break
    try:
        budget.remove_income(description_or_index)
    except ValueError as error:
        print(f"Error: {error}")

    print("Income Removed successfully!")


def remove_expense_ui(budget: Budget) -> None:
    """Prompt the user to remove an expense by description or index."""

    while True:
        print("1. remove expense by description")
        print("2. remove expense by index")
        remove_method = input("Choose a remove method (index-description): ")
        if remove_method:
            description_or_index = handle_remove("expense", remove_method)
            break
    try:
        budget.remove_expense(description_or_index)
    except ValueError as error:
        print(f"Error: {error}")
    print("Expense Removed successfully!")


def clear_all_ui(budget: Budget) -> None:
    """Clear all incomes and expenses from the budget."""

    budget.clear_all()
    print("Budget Cleared successfully!")
