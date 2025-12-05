from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.entities.db_model import db_init
from src.apis.users_routes import users_router
from src.apis.income_routes import income_router
from src.apis.expenses_routes import expense_router
from src.apis.investment_routes import investment_router
from src.apis.dashboard_routes import dashboard_router
from src.apis.chat_routes import chat_router
from src.apis.investment_advisor_routes import advisor_router

async def lifespan(app: FastAPI):
    db_init()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(income_router)
app.include_router(expense_router)
app.include_router(investment_router)
app.include_router(dashboard_router)
app.include_router(chat_router)
app.include_router(advisor_router)