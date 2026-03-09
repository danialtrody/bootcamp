from decimal import Decimal, InvalidOperation
import requests
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


API_BASE_URL = "http://localhost:8000"
ERROR_SERVER = "Server returned an error."
ERROR_CONNECTION = "Cannot connect to the server. Make sure the API is running."


def run_account_cli() -> None:
    while True:
        user_choice = main_menu()
        if handle_user_choice(user_choice):
            break


def main_menu() -> str:
    menu_lines = [
        "\n|==============================|",
        "|Available Sections:           |",
        "|1. Show all accounts balance  |",
        "|2. Add a new account          |",
        "|3. Get account balance        |",
        "|4. Update account name        |",
        "|5. Delete account             |",
        "|6. BACK                       |",
        "|==============================|",
    ]

    for line in menu_lines:
        print(line)
    return input("\nChoose an option (1-6): ").strip()


def handle_user_choice(choice: str) -> bool:
    """Handle the user's menu choice. Returns True if should exit."""
    if choice == "6":
        return True

    actions = {
        "1": print_account_balance,
        "2": add_account,
        "3": print_single_account_balance,
        "4": update_account_name,
        "5": delete_account,
    }
    action = actions.get(choice)

    if action is None:
        print("\nEnter a valid number between 1 and 6.")
        return False

    action()
    return False


def print_account_balance() -> None:
    endpoint = f"{API_BASE_URL}/accounts"

    try:
        response = requests.get(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_200_OK:
        accounts = response.json()
        if accounts:
            print("\nAccounts Balance:")
            for account in accounts:
                print(f"- {account['name']}: {account['balance']}")
        else:
            print("No accounts found.")
    else:
        print(f"{ERROR_SERVER} Status code: {response.status_code}")


def add_account() -> None:
    endpoint = f"{API_BASE_URL}/accounts"
    name = get_name_account_input()
    opening_balance = get_opening_balance_input()

    data = {"name": name, "opening_balance": str(opening_balance)}

    try:
        response = requests.post(endpoint, json=data)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_201_CREATED:
        account = response.json()
        print(
            f"\nAccount created successfully: {account['name']} with opening_balance {account['opening_balance']}"
        )
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def print_single_account_balance() -> None:
    account_id = get_account_id_input()
    endpoint = f"{API_BASE_URL}/accounts/{account_id}"

    try:
        response = requests.get(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_200_OK:
        account = response.json()
        print(f"- {account['name']}: {account['balance']}")
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def update_account_name() -> None:
    account_id = get_account_id_input()
    name = get_name_account_input()
    endpoint = f"{API_BASE_URL}/accounts/{account_id}?updated_name={name}"

    try:
        response = requests.put(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_200_OK:
        account = response.json()
        print(
            f"\nAccount name updated successfully: {account['name']} with opening_balance {account['opening_balance']}"
        )
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def delete_account() -> None:
    account_id = get_account_id_input()
    endpoint = f"{API_BASE_URL}/accounts/{account_id}"

    try:
        response = requests.delete(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_200_OK:
        print(f"\nAccount with ID: {account_id} deleted successfully")
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def get_name_account_input() -> str:
    while True:
        name = input("Enter account name: ").strip()
        if name:
            return name
        print("Account name can not be empty")


def get_opening_balance_input() -> Decimal:
    while True:
        balance_input = input("Enter opening amount: ").strip()
        try:
            return Decimal(balance_input)
        except InvalidOperation:
            print("Please enter a valid opening balance.")


def get_account_id_input() -> int:
    while True:
        account_id = input("Enter account id: ").strip()
        if account_id.isdigit():
            return int(account_id)
        print("Enter a valid account id.")
