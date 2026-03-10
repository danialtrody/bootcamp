from fastapi import FastAPI

from solution.api.routers import accounts_router
from solution.api.routers import net_worth_router
from solution.api.routers import categories_router
from solution.api.routers import transactions_router
from solution.api.routers import transfers_router
from solution.api.routers import reports_router
from solution.api.routers import dashboard_router
from solution.api.routers import portability_router

app = FastAPI()

app.include_router(accounts_router.router)
app.include_router(net_worth_router.router)
app.include_router(categories_router.router)
app.include_router(transactions_router.router)
app.include_router(transfers_router.router)
app.include_router(reports_router.router)
app.include_router(dashboard_router.router)
app.include_router(portability_router.router)

# run -> from HW8 fastapi dev solution/api/main.py
