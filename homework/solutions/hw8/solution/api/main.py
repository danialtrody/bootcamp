from fastapi import FastAPI

from solution.api.routers import accounts_router
from solution.api.routers import net_worth_router


app = FastAPI()

app.include_router(accounts_router.router)
app.include_router(net_worth_router.router)
