import asyncio
import aiohttp
import time

FETCH_URL = "http://localhost:8000/process_order?user_id=123&product_id=456&zip_code=12345"
CONCURRENT_REQUESTS = 20


async def send_request(session):
    start = time.time()
    async with session.get(FETCH_URL) as response:
        await response.json()
    return time.time() - start


async def main():
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session) for _ in range(CONCURRENT_REQUESTS)]
        durations = await asyncio.gather(*tasks)

    total_time = time.time() - start_time
    average_time = sum(durations) / len(durations)
    request_per_second = CONCURRENT_REQUESTS / total_time

    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average response time: {average_time:.2f} seconds")
    print(f"Requests per second: {request_per_second:.2f}")


if __name__ == "__main__":
    asyncio.run(main())