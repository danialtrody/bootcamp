from solution.business_logic.budget import Budget
from solution.business_logic.income import Income
from solution.business_logic.expense import Expense


def add_transaction_ui(budget: Budget, transaction_type: str) -> None:
    """Prompt the user to add an income or expense to the budget."""

    description = input(f"Enter {transaction_type} description: ").strip()

    try:
        amount = float(input(f"Enter {transaction_type} amount: "))
    except ValueError:
        print_error("Invalid input. Please enter a valid amount.")
        return

    if transaction_type == "income":
        try:
            income: Income = Income(description, amount)
        except ValueError as error:
            print_error(error)
            return
        try:
            budget.add_income(income)
        except ValueError as error:
            print_error(error)
            return
    else:
        try:
            expense: Expense = Expense(description, amount)
        except ValueError as error:
            print_error(error)
            return
        try:
            budget.add_expense(expense)
        except ValueError as error:
            print_error(error)
            return

    print(f"{transaction_type.capitalize()} added successfully!")


def remove_transaction_ui(budget: Budget, transaction_type: str) -> None:
    """Prompt the user to remove an income or expense by description or index."""

    while True:
        print(f"1. remove {transaction_type} by description")
        print(f"2. remove {transaction_type} by index")
        remove_method = input("Choose a remove method (index-description): ")
        if remove_method:
            description_or_index = handle_remove(transaction_type, remove_method)
            break
    try:
        if transaction_type == "income":
            budget.remove_income(description_or_index)
        else:
            budget.remove_expense(description_or_index)

    except (ValueError, IndexError) as error:
        print(f"Error: {error}")
        return
    print(f"{transaction_type.capitalize()} Removed successfully!")


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


def print_error(error: Exception | str) -> None:
    """Print an error message."""
    print(f"Error: {error}")
