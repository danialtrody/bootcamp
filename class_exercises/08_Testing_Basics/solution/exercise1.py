from typing import Any
import requests

SUCCESS_STATUS_CODE = 200


def fetch_sorted_todos(limit: int = 20) -> list[dict[str, Any]]:

    todos_list: list[dict[str, Any]] = []

    for number in range(1, limit + 1):
        url = f"https://jsonplaceholder.typicode.com/todos/{number}"
        response = requests.get(url)

        if response.status_code == SUCCESS_STATUS_CODE:
            data = response.json()
            todos_list.append(data)

    return sorted(todos_list, key=lambda todo: todo["title"])
