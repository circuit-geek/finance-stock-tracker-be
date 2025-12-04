import datetime
from typing import Optional

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
    symbol: Optional[str] = Field(..., description="The ticker symbol of the stock")
    quantity: Optional[int] = Field(..., description="The quantity purchased")
    description: str = Field(..., description="Generated description based on user input")

    def run(self, user_id: str):
        new_investment =  Investments.create(
            user_id=user_id,
            investment_type=self.investment_type,
            amount=self.amount,
            description=self.description,
            symbol = self.symbol,
            quantity = self.quantity,
            purchased_at = datetime.datetime.now(datetime.UTC),
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

class GetExpenseSummary(OpenAISchema):
    """
    Use this tool to get summary of all the expenses for that user, this tool will return
    all the spends as dictionary.
    """

    def run(self, user_id: str):
        expense_map = {}
        expenses = list(Expenses.select().where(Expenses.user_id == user_id))
        for expense in expenses:
            expense_map[expense.expense_type] = (expense_map.get(expense.expense_type, 0) +
                                                 expense.amount)

        return expense_map


class GetInvestmentSummary(OpenAISchema):
    """
    Use this tool to get summary of all the investments for that user, this tool will return
    all the investments as dictionary.
    """

    def run(self, user_id: str):
        investment_map = {}
        investments = list(Investments.select().where(Investments.user_id == user_id))
        for investment in investments:
            investment_map[investment.investment_type] = (investment_map.get(investment.investment_type, 0)
                                                          + investment.amount)

        return investment_map