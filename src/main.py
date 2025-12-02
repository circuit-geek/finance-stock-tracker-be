from fastapi import FastAPI
from src.entities.db_model import db_init
from src.apis.users_routes import users_router
from src.apis.income_routes import income_router
from src.apis.expenses_routes import expense_router
from src.apis.investment_routes import investment_router
from src.apis.dashboard_routes import dashboard_router
from src.apis.chat_routes import chat_router

async def lifespan(app: FastAPI):
    db_init()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(income_router)
app.include_router(expense_router)
app.include_router(investment_router)
app.include_router(dashboard_router)
app.include_router(chat_router)