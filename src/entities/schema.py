import datetime
from enum import Enum

from pydantic import BaseModel


class IncomeType(str, Enum):
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT_RETURNS = "investment_returns"
    OTHERS = "others"

class InvestmentType(str, Enum):
    STOCKS = "stocks"
    MUTUAL_FUNDS = "mutual_funds"
    REAL_ESTATE = "real_estate"
    BONDS = "bonds"
    CRYPTO = "crypto"
    OTHERS = "others"

class ExpenseType(str, Enum):
    FOOD_AND_DINING = "food_and_dining"
    ENTERTAINMENT = "entertainment"
    BILLS = "bills"
    HEALTHCARE = "healthcare"
    SHOPPING = "shopping"
    TRANSPORTATION = "transportation"
    OTHERS = "others"

class UserRegister(BaseModel):
    name: str
    email_id: str
    password: str

class UserRegisterSuccess(BaseModel):
    user_id: str
    name: str
    email_id: str

class UserLogin(BaseModel):
    email_id: str
    password: str

class AddIncome(BaseModel):
    income_type: IncomeType
    amount: float
    description: str
    created_at: datetime.datetime

class ShowIncome(BaseModel):
    income_id: str
    income_type: IncomeType
    amount: float
    description: str
    created_at: datetime.datetime

class AddExpense(BaseModel):
    expense_type: ExpenseType
    amount: float
    description: str
    created_at: datetime.datetime

class ShowExpense(BaseModel):
    expense_id: str
    expense_type: ExpenseType
    amount: float
    description: str
    created_at: datetime.datetime

class AddInvestment(BaseModel):
    investment_type: InvestmentType
    amount: float
    description: str
    created_at: datetime.datetime

class ShowInvestment(BaseModel):
    investment_id: str
    investment_type: InvestmentType
    amount: float
    description: str
    created_at: datetime.datetime

class ChatResponse(BaseModel):
    message: str
    chat_id: str

class NewChatSession(BaseModel):
    user_id: str
    chat_name: str

class ChatHistoryItem(BaseModel):
    id: str
    user_message: str
    assistant_message: str

class SessionInfo(BaseModel):
    id: str
    user_id: str
    session_name: str

class DashBoardStats(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
    portfolio_value: float

