from fastapi import FastAPI

from src.infrastructure.logging_config import setup_logging
from src.routers.auth import router as auth_router
from src.routers.students import router as students_router

setup_logging()

app = FastAPI(
    title="CodeValue School API",
    description="API for the CodeValue School management system",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(students_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "OK"}
