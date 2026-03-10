import requests
from starlette.status import HTTP_200_OK

API_BASE_URL = "http://localhost:8000"
ERROR_SERVER = "Server returned an error."
ERROR_CONNECTION = "Cannot connect to the server. Make sure the API is running."


def run_other_cli() -> None:
    while True:
        user_choice = main_menu()
        if handle_user_choice(user_choice):
            break


def main_menu() -> str:
    menu_lines = [
        "\n|==============================|",
        "|Available Sections:           |",
        "|1. Show dashboard summary     |",
        "|2. Show net worth             |",
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

    actions = {"1": print_dashboard_summary, "2": all_account_net_worth}
    action = actions.get(choice)

    if action is None:
        print("\nEnter a valid number between 1 and 3.")
        return False

    action()
    return False


def print_dashboard_summary() -> None:
    endpoint = f"{API_BASE_URL}/dashboard"

    try:
        response = requests.get(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)

    if response.status_code == HTTP_200_OK:
        dashboard = response.json()
        if dashboard:
            print("\nDashboard:")
            print(
                f"- Total Income: {dashboard["total_income"]} |",
                f"Total Expense: {dashboard["total_expense"]} |",
                f"Net Cash Flow: {dashboard["net_cash_flow"]} ",
            )
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def all_account_net_worth() -> None:
    endpoint = f"{API_BASE_URL}/net-worth"

    try:
        response = requests.get(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)

    if response.status_code == HTTP_200_OK:
        net_worth = response.json()
        if net_worth:
            print("\nNet Worth:")
            print(net_worth)
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )
