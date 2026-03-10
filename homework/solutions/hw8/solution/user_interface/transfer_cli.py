import datetime
from decimal import Decimal, InvalidOperation
import requests
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

API_BASE_URL = "http://localhost:8000"
ERROR_SERVER = "Server returned an error."
ERROR_CONNECTION = "Cannot connect to the server. Make sure the API is running."


def run_transfer_cli() -> None:
    while True:
        user_choice = main_menu()
        if handle_user_choice(user_choice):
            break


def main_menu() -> str:
    menu_lines = [
        "\n|==============================|",
        "|Available Sections:           |",
        "|1. Show all transfers         |",
        "|2. Add transfer               |",
        "|3. Delete transfer            |",
        "|4. BACK                       |",
        "|==============================|",
    ]

    for line in menu_lines:
        print(line)
    return input("\nChoose an option (1-4): ").strip()


def handle_user_choice(choice: str) -> bool:
    """Handle the user's menu choice. Returns True if should exit."""
    if choice == "4":
        return True

    actions = {
        "1": print_all_transfers,
        "2": add_transfer,
        "3": delete_transfer,
    }
    action = actions.get(choice)

    if action is None:
        print("\nEnter a valid number between 1 and 4.")
        return False

    action()
    return False


def print_all_transfers() -> None:
    endpoint = f"{API_BASE_URL}/transfer"

    try:
        response = requests.get(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_200_OK:
        transfers = response.json()
        if transfers:
            print("\nTransfers:")
            for transfer in transfers:
                print(
                    f"- ID: {transfer["id"]} |",
                    f"Amount: {transfer['amount']} |",
                    f"Date: {transfer['date']} |",
                    f"Description: {transfer['description']} |",
                    f"From account ID: {transfer['from_account_id']} |",
                    f"To account ID: {transfer['to_account_id']}",
                )
        else:
            print("No Transfers found.")
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def add_transfer() -> None:
    endpoint = f"{API_BASE_URL}/transfer"

    data = {
        "amount": str(get_amount_input()),
        "date": datetime.date.today().isoformat(),
        "description": get_description_input(),
        "from_account_id": get_id_input("from"),
        "to_account_id": get_id_input("to"),
    }

    try:
        response = requests.post(endpoint, json=data)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_201_CREATED:
        transfer = response.json()
        if transfer:
            print("Transfer completed successfully:")
            print(
                f"- ID: {transfer["id"]} |",
                f"Amount: {transfer['amount']} |",
                f"Date: {transfer['date']} |",
                f"Description: {transfer['description']} |",
                f"From account ID: {transfer['from_account_id']} |",
                f"To account ID: {transfer['to_account_id']}",
            )
        else:
            print("No Transfers found.")
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def delete_transfer() -> None:
    transfer_id = get_id_input("")
    endpoint = f"{API_BASE_URL}/transfer/{transfer_id}"

    try:
        response = requests.delete(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_200_OK:
        print(f"\nTransfer with ID: {transfer_id} deleted successfully")
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def get_description_input() -> str:
    while True:
        name = input("Enter transfer description: ").strip()
        if name:
            return name
        print("Transfer description can not be empty")


def get_amount_input() -> Decimal:
    while True:
        amount_input = input("Enter amount: ").strip()
        try:
            return Decimal(amount_input)
        except InvalidOperation:
            print("Please enter a valid amount.")


def get_id_input(source_destenation_account: str) -> int:
    while True:
        account_id = input(f"Enter {source_destenation_account} account id: ").strip()
        if account_id.isdigit():
            return int(account_id)
        print("Enter a valid account id.")
