from fastapi import FastAPI
import asyncio
from typing import Dict
from constants import HOST, DB_PORT

SIMULATED_DB_DELAY = 1.0  # seconds


app = FastAPI(title="Database Simulator")


@app.get("/query")
async def query_db() -> Dict[str, str]:
    """Simulate a database query that takes some time to complete."""
    await asyncio.sleep(SIMULATED_DB_DELAY)
    return {"data": "some_data"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=DB_PORT)
