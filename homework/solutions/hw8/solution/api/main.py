from fastapi import FastAPI

from solution.api.routers import accounts_router
from solution.api.routers import net_worth_router
from solution.api.routers import categories_router
from solution.api.routers import transactions_router
from solution.api.routers import transfers_router
from solution.api.routers import reports_router
from solution.api.routers import dashboard_router
from solution.services.category_service import CategoryService
from solution.repository.base_repository import BaseRepository
from solution.models.categories import Category
from solution.repository.csv_accessor import CsvFileAccessor


app = FastAPI()

app.include_router(accounts_router.router)
app.include_router(net_worth_router.router)
app.include_router(categories_router.router)
app.include_router(transactions_router.router)
app.include_router(transfers_router.router)
app.include_router(reports_router.router)
app.include_router(dashboard_router.router)


@app.on_event("startup")
async def seed_categories() -> None:
    accessor = CsvFileAccessor("data/categories.csv")
    category_repository = BaseRepository(accessor, Category)
    service = CategoryService(category_repository)
    await service.seed_default_categories()

# run -> from HW8 fastapi dev solution/api/main.py
