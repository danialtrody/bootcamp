from fastapi import FastAPI

from src.routers.students import router as students_router

app = FastAPI(
    title="CodeValue School API",
    description="API for the CodeValue School management system",
    version="0.1.0",
)

app.include_router(students_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "OK"}
