import datetime

from src.entities.db_model import Expenses
from src.entities.schema import AddExpense, ShowExpense
from typing import List, Optional

async def add_new_expense(expense: AddExpense, user_id: str):
    expense_type = expense.expense_type
    amount = expense.amount
    description = expense.description
    created_at = expense.created_at

    new_expense = Expenses.create(
        user_id = user_id,
        expense_type = expense_type,
        amount = amount,
        description = description,
        created_at = created_at
    )

    return {
        "message": "Added new expense",
        "expense_id": new_expense.id
    }

async def show_all_expense(user_id: str) -> List[ShowExpense]:
    query = Expenses.get_or_none(Expenses.user_id == user_id)
    output = []
    for value in query:
        output.append(ShowExpense(
            expense_type=value.expense_type,
            amount=value.amount,
            description=value.description,
            created_at=value.created_at
        ))
    return output

async def delete_expense(expense_id: str):
    Expenses.delete().where(Expenses.id == expense_id).execute()
    return {
        "message": "Expenses deleted successfully!",
        "expense_id": expense_id
    }

async def update_expense(expense_id: str, amount: Optional[float], description: Optional[str]):
    expense = Expenses.get_or_none(Expenses.id == expense_id)
    if not expense:
        return {"message": "Expenses not found"}

    updated = False

    if amount is not None:
        expense.amount = amount
        updated = True

    if description is not None:
        expense.description = description
        updated = True

    if updated:
        expense.created_at = datetime.datetime.now(datetime.UTC)
        expense.save()
        return {"message": "Data updated successfully!"}