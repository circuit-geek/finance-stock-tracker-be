import datetime
from pathlib import Path

from src.constants.properties import GPT_MODEL
from src.entities.schema import DashBoardStats, DashBoardGraphStats, LLMInsightType
from src.entities.db_model import Income, Expenses, Investments, Insights
from src.utils.llm_utils import client


async def dashboard_stats(user_id: str) -> DashBoardStats:
    total_income = 0
    incomes = list(Income.select().where(Income.user_id == user_id))
    for income in incomes:
        total_income += income.amount

    total_expenses = 0
    expenses = list(Expenses.select().where(Expenses.user_id == user_id))
    for expense in expenses:
        total_expenses += expense.amount

    total_investments = 0
    investments = list(Investments.select().where(Investments.user_id == user_id))
    for investment in investments:
        total_investments += investment.amount

    net_savings = total_income - total_expenses

    return DashBoardStats(
        total_income=total_income,
        total_expenses=total_expenses,
        portfolio_value=total_investments,
        net_savings=net_savings
    )

async def dashboard_graph_stats(user_id: str) -> DashBoardGraphStats:

    total_income = 0
    incomes = list(Income.select().where(Income.user_id == user_id))
    for income in incomes:
        total_income += income.amount

    total_expenses = 0
    expenses = list(Expenses.select().where(Expenses.user_id == user_id))
    for expense in expenses:
        total_expenses += expense.amount

    total_investments = 0
    investments = list(Investments.select().where(Investments.user_id == user_id))
    for investment in investments:
        total_investments += investment.amount

    liquid_savings = total_income - (total_expenses + total_investments)

    expense_percent = (total_expenses/total_income)*100
    liquid_savings_percent = (liquid_savings / total_income) * 100
    investment_percent = (total_investments / total_income) * 100

    return DashBoardGraphStats(
        total_expenses=total_expenses,
        liquid_savings=liquid_savings,
        investments=total_investments,
        expense_percent=expense_percent,
        liquid_savings_percent=liquid_savings_percent,
        investments_percent=investment_percent
    )

async def show_expenses_by_category(user_id: str):
    expenses = list(Expenses.select().where(Expenses.user_id == user_id))
    expense_map = {}
    for expense in expenses:
        expense_map[expense.expense_type] = (expense_map.get(expense.expense_type, 0) +
                                             expense.amount)

    sorted_map = dict(sorted(expense_map.items(), key=lambda x:x[1], reverse=True))
    return sorted_map

async def get_llm_insights(user_id: str):
    income = list(Income.select().where(Income.user_id == user_id))
    expenses = list(Expenses.select().where(Expenses.user_id == user_id))
    investments = list(Investments.select().where(Investments.user_id == user_id))
    user_income = f"""
    This is the income of the user {[x for x in income]}
    """
    user_expense = f"""
    This is the expense of the user {[x for x in expenses]}
    """
    user_investment = f"""
    This is the investment of the user {[x for x in investments]}
    """
    system_prompt = Path("src/prompts/basic_insights_prompt.jinja").read_text()
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt + user_income + user_expense + user_investment
            }
        ]
    )
    insights = response.choices[0].message.content
    Insights.create(
        user_id = user_id,
        insights = insights,
        insight_type = LLMInsightType.DASHBOARD_INSIGHT.value,
        generated_date = datetime.datetime.now(datetime.UTC)
    )
    return {"insights": insights}