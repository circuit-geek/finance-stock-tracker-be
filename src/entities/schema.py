import datetime
from enum import Enum
from typing import Optional, Dict, List

from pydantic import BaseModel


class IncomeType(str, Enum):
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT_RETURNS = "investment_returns"

class InvestmentType(str, Enum):
    STOCKS = "stocks"
    MUTUAL_FUNDS = "mutual_funds"
    REAL_ESTATE = "real_estate"
    ETF = "etf"
    BONDS = "bonds"
    CRYPTO = "crypto"

class ExpenseType(str, Enum):
    FOOD_AND_DINING = "food_and_dining"
    ENTERTAINMENT = "entertainment"
    BILLS = "bills"
    HEALTHCARE = "healthcare"
    SHOPPING = "shopping"
    TRANSPORTATION = "transportation"

class InvestmentGoals(str, Enum):
    WEALTH_CREATION = "wealth_creation"
    SIP_GROWTH = "sip_growth"
    RETIREMENT_PLANNING = "retirement_planning"
    CHILD_EDUCATION = "child_education"
    HOME_PURCHASE = "home_purchase"
    SHORT_TERM_GROWTH = "short_term_growth" ## default this to 1 year

class RiskAppetite(str, Enum):
    LOW_RISK = "low_risk"
    MEDIUM_RISK = "medium_risk"
    HIGH_RISK = "high_risk"

class InvestmentHorizon(str, Enum):
    SHORT_TIME_HORIZON = "1-2_years"
    MEDIUM_TIME_HORIZON = "3-4_years"
    LONG_TIME_HORIZON = "5-10_years"
    VERY_LONG_TIME_HORIZON = "10+_years"

class LLMInsightType(str, Enum):
    DASHBOARD_INSIGHT = "dashboard_insight"
    AGENT_INVESTMENT_INSIGHT = "agent_investment_insight"

class UserRegister(BaseModel):
    name: str
    email_id: str
    password: str
    dob: datetime.datetime

class UserRegisterSuccess(BaseModel):
    user_id: str
    name: str
    email_id: str

class UserProfile(BaseModel):
    name: str
    email_id: str
    dob: datetime.datetime
    investment_preferences: Optional[Dict]

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
    symbol: Optional[str]
    quantity: Optional[int]
    purchased_at: Optional[datetime.datetime]
    created_at: datetime.datetime

class ShowInvestment(BaseModel):
    investment_id: str
    investment_type: InvestmentType
    amount: float
    description: str
    created_at: datetime.datetime

class UserChatInput(BaseModel):
    prompt: str


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

class DashBoardGraphStats(BaseModel):
    total_expenses: float
    liquid_savings: float
    investments: float
    expense_percent: float
    liquid_savings_percent: float
    investments_percent: float

class UserInvestmentPreferences(BaseModel):
    investment_goals: List[InvestmentGoals]
    risk_appetite: RiskAppetite
    investment_horizon: InvestmentHorizon
    investment_types: List[InvestmentType]
    monthly_investment_amount: float

class UserInvestmentPreferencesSaved(BaseModel):
    message: str
    investment_goals: List[InvestmentGoals]
    risk_appetite: RiskAppetite
    investment_horizon: InvestmentHorizon
    investment_types: List[InvestmentType]
    monthly_investment_amount: float
