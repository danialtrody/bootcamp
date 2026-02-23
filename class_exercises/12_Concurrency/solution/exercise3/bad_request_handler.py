from fastapi import FastAPI
import requests
from typing import Dict
from constants import HOST, DB_PORT, BAD_HANDLER_PORT

DB_URL = f"http://{HOST}:{DB_PORT}/query"


app = FastAPI(title="Bad Request Handler Example")


@app.get("/get_data")
async def get_data() -> Dict[str, str]:
    """
    BAD PRACTICE: Using blocking requests.get() in an async handler.
    This will block the event loop and prevent handling other requests.
    """
    response = requests.get(DB_URL)  # Blocking call!
    return response.json()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=BAD_HANDLER_PORT)
