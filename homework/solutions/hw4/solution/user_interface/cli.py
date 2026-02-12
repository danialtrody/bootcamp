from solution.business_logic.budget import Budget
from solution.business_logic.income import Income
from solution.business_logic.expense import Expense


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


def run_cli() -> None:
    budget = Budget()
    while True:
        user_choice = main_menu()
        if handle_user_choice(budget, user_choice):
            break


def add_income_ui(budget: Budget) -> None:
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

    print("Income added successfully!")


def summary_ui(budget: Budget) -> None:
    print(budget.summary())


def remove_income_ui(budget: Budget) -> None:
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


def handle_remove(remove_item_type: str, remove_method: str) -> int | str:
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


def clear_all_ui(budget: Budget) -> None:
    budget.clear_all()
    print("Budget Cleared successfully!")


def print_error(error: Exception) -> None:
    print(f"Error: {error}")
