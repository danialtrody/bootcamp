import requests
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


API_BASE_URL = "http://localhost:8000"
ERROR_SERVER = "Server returned an error."
ERROR_CONNECTION = "Cannot connect to the server. Make sure the API is running."


def run_category_cli() -> None:
    while True:
        user_choice = main_menu()
        if handle_user_choice(user_choice):
            break


def main_menu() -> str:
    menu_lines = [
        "\n|==============================|",
        "|Available Sections:           |",
        "|1. Show all categories        |",
        "|2. Add category               |",
        "|3. Delete category            |",
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
        "1": print_all_categories,
        "2": add_category,
        "3": delete_category,
    }
    action = actions.get(choice)

    if action is None:
        print("\nEnter a valid number between 1 and 4.")
        return False

    action()
    return False


def print_all_categories() -> None:
    endpoint = f"{API_BASE_URL}/categories/"

    try:
        response = requests.get(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)

    if response.status_code == HTTP_200_OK:
        categories = response.json()
        if categories:
            print("\nCategories: ")
            for catygory in categories:
                print(
                    f"- ID: {catygory["id"]} |",
                    f"Name: {catygory["name"]} |",
                    f"Type: {catygory["type"]} ",
                )
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def add_category() -> None:
    endpoint = f"{API_BASE_URL}/categories/"
    name = get_name_category_input()
    type = get_type_category_input()

    data = {"name": name, "type": type}

    try:
        response = requests.post(endpoint, json=data)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)

    if response.status_code == HTTP_201_CREATED:
        catrgory = response.json()
        print(
            "\nCategory added successfully:",
            f"- ID: {catrgory["id"]} |",
            f"Name: {catrgory["name"]} |",
            f"Type: {catrgory["type"]}",
        )
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def delete_category() -> None:
    category_id = get_category_id_input()
    endpoint = f"{API_BASE_URL}/categories/{category_id}"

    try:
        response = requests.delete(endpoint)
    except requests.exceptions.RequestException:
        print(ERROR_CONNECTION)
        return

    if response.status_code == HTTP_200_OK:
        print(f"\nCategory with ID: {category_id} deleted successfully")
    else:
        print(
            f"{ERROR_SERVER} Status code: {response.status_code}, detail: {response.text}"
        )


def get_name_category_input() -> str:
    while True:
        name = input("Enter category name: ").strip()
        if name:
            return name
        print("Category name can not be empty")


def get_type_category_input() -> str:
    while True:
        type = input("Enter category type: ").strip().lower()
        if not type:
            print("Category type can not be empty")
            continue
        if type in ("income", "expense"):
            return type
        else:
            print("Category type should be income or expense")


def get_category_id_input() -> int:
    while True:
        category_id = input("Enter category id: ").strip()
        if category_id.isdigit():
            return int(category_id)
        print("Enter a valid category id.")
