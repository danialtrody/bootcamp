import requests
from starlette.status import HTTP_200_OK


API_BASE_URL = "http://localhost:8000"
ERROR_SERVER = "Server returned an error."
ERROR_CONNECTION = "Cannot connect to the server. Make sure the API is running."


def run_report_cli() -> None:
    while True:
        user_choice = main_menu()
        if handle_user_choice(user_choice):
            break


def main_menu() -> str:
    menu_lines = [
        "\n|==============================|",
        "|Available Sections:           |",
        "|1. Show monthly summary       |",
        "|2. Show spending by category  |",
        "|3. BACK                       |",
        "|==============================|",
    ]

    for line in menu_lines:
        print(line)
    return input("\nChoose an option (1-3): ").strip()


def handle_user_choice(choice: str) -> bool:
    """Handle the user's menu choice. Returns True if should exit."""
    if choice == "3":
        return True

    actions = {"1": print_monthly_summary, "2": print_spending_breakdown_by_category}
    action = actions.get(choice)

    if action is None:
        print("\nEnter a valid number between 1 and 3.")
        return False

    action()
    return False


def print_monthly_summary() -> None:
    endpoint = f"{API_BASE_URL}/reports/monthly-summary"
    params = {
        "month": get_date_input("Enter month number (1-12): "),
        "year": get_date_input("Enter year: "),
        "account_id": get_account_id_input(),
    }

    try:
        response = requests.get(endpoint, params=params)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)

    if response.status_code == HTTP_200_OK:
        report = response.json()
        if report:
            print("\nMonthly Summary:")
            print(
                f"- Total Income: {report["total_income"]} |",
                f"Total Expense: {report["total_expense"]} |",
                f"Net Cash Flow: {report["net_cash_flow"]} ",
            )
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def print_spending_breakdown_by_category() -> None:
    endpoint = f"{API_BASE_URL}/reports/spending-breakdown"
    params = {
        "month": get_date_input("Enter month number (1-12): "),
        "year": get_date_input("Enter year: "),
        "account_id": get_account_id_input(),
    }

    try:
        response = requests.get(endpoint, params=params)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)

    if response.status_code == HTTP_200_OK:
        report = response.json()
        if report:
            print("\nSpending Breakdown:")
            for category_name, amount in report.items():
                print(f"- Category Name: {category_name} |", f"Total Expense: {amount}")
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def get_date_input(year_or_month: str) -> int:
    while True:
        date = input(year_or_month).strip()
        if date.isdigit():
            return int(date)


def get_account_id_input() -> int | None:
    while True:
        account_id_input = input("Enter account id (or leave blank for all): ")
        if account_id_input.isdigit() or account_id_input == "":
            return int(account_id_input) if account_id_input.isdigit() else None
