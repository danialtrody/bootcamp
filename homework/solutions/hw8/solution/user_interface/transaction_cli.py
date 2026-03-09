from decimal import Decimal, InvalidOperation
import requests
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from typing import List, Optional, Dict
import datetime

API_BASE_URL = "http://localhost:8000"
ERROR_SERVER = "Server returned an error."
ERROR_CONNECTION = "Cannot connect to the server. Make sure the API is running."


def run_transaction_cli() -> None:
    while True:
        user_choice = main_menu()
        if handle_user_choice(user_choice):
            break


def main_menu() -> str:
    menu_lines = [
        "\n|==============================|",
        "|Available Sections:           |",
        "|1. Show all transactions      |",
        "|2. Add income                 |",
        "|3. Add expense                |",
        "|4. Delete transaction         |",
        "|5. BACK                       |",
        "|==============================|",
    ]

    for line in menu_lines:
        print(line)
    return input("\nChoose an option (1-5): ").strip()


def handle_user_choice(choice: str) -> bool:
    """Handle the user's menu choice. Returns True if should exit."""
    if choice == "5":
        return True

    actions = {
        "1": print_all_transactions,
        "2": add_income,
        "3": add_expense,
        "4": delete_transaction
    }
    action = actions.get(choice)

    if action is None:
        print("\nEnter a valid number between 1 and 6.")
        return False

    action()
    return False


def print_all_transactions():
    params = all_transactions_user_inputs()
    endpoint = f"{API_BASE_URL}/transactions/"
    
    try:
        response = requests.get(endpoint, params=params)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        
    if response.status_code==HTTP_200_OK:
        transactions = response.json()
        if not transactions:
            print("No transactions found.")
        else:
            for transaction in transactions:
                print(
                    f"ID {transaction['id']} | "
                    f"{transaction['date']} | "
                    f"{transaction['type']} | "
                    f"Amount: {transaction['amount']} | "
                    f"Account ID: {transaction['account_id']} | "
                    f"Category ID: {transaction['category_id']}"
                    )
    else:
        print(f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}")

def all_transactions_user_inputs() -> Dict:
    account_id_input = input("Enter account id (or leave blank for all): ").strip()
    month_input = input("Enter month number (1-12, optional): ").strip()
    year_input = input("Enter year (optional): ").strip()

    account_id: Optional[int] = int(account_id_input) if account_id_input.isdigit() else None
    month: Optional[int] = int(month_input) if month_input.isdigit() else None
    year: Optional[int] = int(year_input) if year_input.isdigit() else None

    params = {}
    if account_id is not None:
        params["account_id"] = account_id
    if month is not None:
        params["month"] = month
    if year is not None:
        params["year"] = year
    return params

def add_income():
    endpoint = f"{API_BASE_URL}/transactions/income"
    amount = get_amount_input()
    date = datetime.date.today()
    account_id = get_account_id_input()
    category_id = get_category_id_input()
    
    data = {
        "amount": str(amount),
        "date": date.isoformat(),
        "type": "income",
        "account_id": account_id,
        "category_id": category_id
        }    
    try:
        response = requests.post(endpoint, json=data)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        
    if response.status_code==HTTP_201_CREATED:
        transaction = response.json()
        print(
            f"Transaction added successfully:\n"
            f"ID: {transaction['id']} | "
            f"Date: {transaction['date']} | "
            f"Type: {transaction['type']} | "
            f"Amount: {transaction['amount']} | "
            f"Account ID: {transaction['account_id']} | "
            f"Category ID: {transaction['category_id']}"
        )

    else:
        print(f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}")
        
def add_expense():
    endpoint = f"{API_BASE_URL}/transactions/expense"
    amount = get_amount_input()
    date = datetime.date.today()
    account_id = get_account_id_input()
    category_id = get_category_id_input()
    
    data = {
        "amount": str(amount),
        "date": date.isoformat(),
        "type": "expense",
        "account_id": account_id,
        "category_id": category_id
        }    
    try:
        response = requests.post(endpoint, json=data)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        
    if response.status_code==HTTP_201_CREATED:
        transaction = response.json()
        print(
            f"Transaction added successfully:\n"
            f"ID: {transaction['id']} | "
            f"Date: {transaction['date']} | "
            f"Type: {transaction['type']} | "
            f"Amount: {transaction['amount']} | "
            f"Account ID: {transaction['account_id']} | "
            f"Category ID: {transaction['category_id']}"
        )

    else:
        print(f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}")
        

def delete_transaction():
    account_id = get_account_id_input()
    endpoint = f"{API_BASE_URL}/transactions/{account_id}"

    try:
        response = requests.delete(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_200_OK:
        print(f"\nTransaction with ID: {account_id} deleted successfully")
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )
        


def get_amount_input() -> Decimal:
    while True:
        amount = input("Enter amount: ").strip()
        try:
            return Decimal(amount)
        except InvalidOperation:
            print("Please enter a valid amount (numbers only).")

def get_account_id_input() -> int:
    while True:
        account_id = input("Enter account id: ").strip()
        if account_id.isdigit():
            return int(account_id)
        print("Enter a valid account id.")

def get_category_id_input() -> int:
    while True:
        category_id = input("Enter category id: ").strip()
        if category_id.isdigit():
            return int(category_id)
        print("Enter a valid category id.")


