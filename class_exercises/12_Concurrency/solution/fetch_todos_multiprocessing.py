from concurrent.futures import ProcessPoolExecutor, as_completed
import time
from typing import Any

import requests

MAX_WORKERS = 8
REQUESTS = 20


def fetch_todo(todo_id: int) -> dict[str, Any]:
    try:
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/todos/{todo_id}",
            timeout=10,
        )
    except requests.exceptions.RequestException:
        return {}

    return response.json()


def run_requests() -> float:
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(fetch_todo, todo_id)
            for todo_id in range(1, REQUESTS + 1)
        ]

        for future in as_completed(futures):
            todo = future.result()
            print(f"TODO {todo['id']}: {todo['title']}")

    return time.time() - start_time


def main() -> None:
    print("Fetching 20 TODO items using ProcessPoolExecutor...")

    execution_duration = run_requests()
    avg_time = execution_duration / REQUESTS

    print("Summary:")
    print(f"Total execution time: {execution_duration:.2f} seconds")
    print(f"Average time per request: {avg_time:.2f} seconds")


if __name__ == "__main__":
    main()
