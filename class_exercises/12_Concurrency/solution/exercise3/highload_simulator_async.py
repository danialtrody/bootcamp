import time
import asyncio
import aiohttp
import statistics
import uuid
from starlette.status import HTTP_200_OK
from constants import HOST, GOOD_HANDLER_PORT, BAD_HANDLER_PORT

# Constants
NUM_THREADS = 20
BAD_HANDLER_URL = f"http://{HOST}:{BAD_HANDLER_PORT}/get_data"
GOOD_HANDLER_URL = f"http://{HOST}:{GOOD_HANDLER_PORT}/get_data"


async def make_request(session: aiohttp.ClientSession, url: str) -> float:
    """Make a single request and return the time taken."""

    task_id: str = str(uuid.uuid4())
    start_time = time.time()

    async with session.get(url) as response:
        if response.status == HTTP_200_OK:
            await response.json()

    duration = time.time() - start_time
    print(f"Task {task_id} waited {duration:.3f} seconds for response")

    return duration


async def run_load_test(url: str, description: str) -> None:
    """Run load test against specified URL and print results."""

    print(f"\nTesting {description}...")

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session, url) for _ in range(NUM_THREADS)]

        times = await asyncio.gather(*tasks)

    total_time = time.time() - start_time
    max_request_time = max(times)
    min_request_time = min(times)
    requests_per_second = NUM_THREADS / total_time
    print(f"Results for {description}:")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average request time: {statistics.mean(times):.3f} seconds")
    print(f"Median request time: {statistics.median(times):.3f} seconds")
    print(f"Max request time: {max_request_time:.3f} seconds")
    print(f"Min request time: {min_request_time:.3f} seconds")
    print(f"Requests per second: {requests_per_second:.2f}")


async def main() -> None:
    """Run load tests against both good and bad handlers."""
    print("Starting load test simulation...")

    # Test bad handler
    await run_load_test(BAD_HANDLER_URL, "Bad Handler (blocking requests)")

    # Test good handler
    await run_load_test(GOOD_HANDLER_URL, "Good Handler (async requests)")


if __name__ == "__main__":
    asyncio.run(main())
