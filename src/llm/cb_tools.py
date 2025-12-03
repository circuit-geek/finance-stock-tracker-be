import datetime

from instructor import OpenAISchema
from pydantic import Field
from tavily import TavilyClient
import yfinance

from src.constants.properties import TAVILY_API_KEY
from src.entities.db_model import Income, Expenses, Investments


class AddIncome(OpenAISchema):
    """
    Use this tool to add new income from the user prompt.
    """
    income_type: str = Field(..., description="Choose one from the income type enum")
    amount: float = Field(..., description="Value of the income entered by the user")
    description: str = Field(..., description="Generated description based on user input")

    def run(self, user_id: str):
        new_income = Income.create(
            user_id=user_id,
            income_type=self.income_type,
            amount=self.amount,
            description=self.description,
            created_at=datetime.datetime.now(datetime.UTC)
        )

        return {
            "message": "Added new income",
            "income_id": str(new_income.id),
        }

class AddExpense(OpenAISchema):
    """
    Use this tool to add new expense from the user prompt.
    """
    expense_type: str = Field(..., description="Choose one from the income type enum")
    amount: float = Field(..., description="Value of the income entered by the user")
    description: str = Field(..., description="Generated description based on user input")

    def run(self, user_id: str):
        new_expense = Expenses.create(
            user_id=user_id,
            expense_type=self.expense_type,
            amount=self.amount,
            description=self.description,
            created_at=datetime.datetime.now(datetime.UTC)
        )

        return {
            "message": "Added new expense",
            "expense_id": str(new_expense.id),
        }

class AddInvestment(OpenAISchema):
    """
    Use this tool to add new investment from the user prompt.
    """
    investment_type: str = Field(..., description="Choose one from the income type enum")
    amount: float = Field(..., description="Value of the income entered by the user")
    description: str = Field(..., description="Generated description based on user input")

    def run(self, user_id: str):
        new_investment =  Investments.create(
            user_id=user_id,
            investment_type=self.investment_type,
            amount=self.amount,
            description=self.description,
            created_at=datetime.datetime.now(datetime.UTC)
        )

        return {
            "message": "Added new investment",
            "investment_id": str(new_investment.id),
        }

class GetInfoFromOnline(OpenAISchema):
    """
    Use this tool to get information from web, for particular user queries
    where the user wants info about finance terms or other such stuff to give
    upto date information.
    """
    user_message: str = Field(..., description="user message which requests the information")

    def run(self):
        tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
        response = tavily_client.search(query=self.user_message)
        return {
            "search_result": response
        }

class GetStockInfo(OpenAISchema):
    """
    Use this tool to get complete information about stock, the user must give the ticker symbol.
    """
    ticker: str = Field(..., description="the ticker symbol for which the user wants info about")

    def run(self):
        ticker = yfinance.Ticker(ticker=self.ticker)
        financials = ticker.financials
        
        return {
            "financials": str(financials)
        }