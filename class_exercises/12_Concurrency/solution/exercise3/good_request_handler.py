from fastapi import FastAPI
import aiohttp
from typing import Dict
from constants import HOST, GOOD_HANDLER_PORT, DB_PORT

DB_URL = f"http://{HOST}:{DB_PORT}/query"


app = FastAPI(title="Good Request Handler Example")


@app.get("/get_data")
async def get_data() -> Dict[str, str]:
    """
    GOOD PRACTICE: Using aiohttp for non-blocking HTTP requests.
    This allows the event loop to handle other requests while waiting for the response.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(DB_URL) as response:
            return await response.json()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=GOOD_HANDLER_PORT)
