import asyncio
import aiohttp
from typing import Any
import time

REQUESTS = 20

TODOS_URL = "https://jsonplaceholder.typicode.com/todos"


async def fetch_todo(session: aiohttp.ClientSession,
                     todo_id: int
                     ) -> dict[str, Any]:
    async with session.get(f"{TODOS_URL}/{todo_id}") as response:
        return await response.json()


async def run_requests() -> float:
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_todo(session, todo_id)
                 for todo_id in range(1, REQUESTS + 1)]

        for task in asyncio.as_completed(tasks):
            print(f"TODO {task['id']}: {task['title']}")

    return time.time() - start_time


def main() -> None:
    print("Fetching 20 TODO items using asyncio and aiohttp...")

    execution_duration = asyncio.run(run_requests())
    avg_time = execution_duration / REQUESTS

    print("Summary:")
    print(f"Total execution time: {execution_duration:.2f} seconds")
    print(f"Average time per request: {avg_time:.2f} seconds")


if __name__ == "__main__":
    main()
