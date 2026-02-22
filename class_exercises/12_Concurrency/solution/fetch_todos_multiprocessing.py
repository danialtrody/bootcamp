from concurrent.futures import ProcessPoolExecutor, as_completed
import time
from typing import Any
import requests

MAX_WORKERS = 8

def fetch_todo(todo_id: int) -> dict[str, Any]:
    try:
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/todos/{todo_id}",
        )
        response.raise_for_status()

        data = response.json()
        print(f"TODO {data['id']}: {data['title']}")

        return data

    except requests.exceptions.RequestException as e:
        print(f"Failed fetching TODO {todo_id}: {e}")
        return {}


if __name__ == "__main__":
    start_execution_time = time.time()

    print("Fetching 20 TODO items using ProcessPoolExecutor...")
    
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_todo,id) for id in range(1,21)]
        for future in as_completed(futures):
            future.result()
            
    print("Summary:")
    execution_duration = time.time() - start_execution_time
    avg_per_request = execution_duration/20
    print(f"Total execution time: {execution_duration:.2f} seconds")
    print(f"Average time per request: {avg_per_request:.2f} seconds")