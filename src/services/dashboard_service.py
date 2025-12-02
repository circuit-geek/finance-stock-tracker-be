from src.entities.schema import DashBoardStats
from src.entities.db_model import Income, Expenses, Investments

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

async def show_expenses_by_category(user_id: str):
    expenses = list(Expenses.select().where(Expenses.user_id == user_id))
    expense_map = {}
    for expense in expenses:
        expense_map[expense.expense_type] = (expense_map.get(expense.expense_type, 0) +
                                             expense.amount)

    sorted_map = dict(sorted(expense_map.items(), key=lambda x:x[1], reverse=True))
    return sorted_map