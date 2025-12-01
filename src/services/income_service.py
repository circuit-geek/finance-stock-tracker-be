import datetime

from src.entities.db_model import Income
from src.entities.schema import AddIncome, ShowIncome
from typing import List, Optional

async def add_new_income(income: AddIncome, user_id: str):
    income_type = income.income_type
    amount = income.amount
    description = income.description
    created_at = income.created_at

    new_income = Income.create(
        user_id = user_id,
        income_type = income_type,
        amount = amount,
        description = description,
        created_at = created_at
    )

    return {
        "message": "Added new income",
        "income_id": new_income.id
    }

async def show_all_income(user_id: str) -> List[ShowIncome]:
    query = Income.select().where(Income.user_id == user_id)
    output = []
    for value in query:
        output.append(ShowIncome(
            income_id=str(value.id),
            income_type=value.income_type,
            amount=value.amount,
            description=value.description,
            created_at=value.created_at
        ))
    return output

async def delete_income(income_id: str):
    Income.delete().where(Income.id == income_id).execute()
    return {
        "message": "Income deleted successfully!",
        "income_id": income_id
    }

async def update_income(income_id: str, amount: Optional[float], description: Optional[str]):
    income = Income.get_or_none(Income.id == income_id)
    if not income:
        return {"message": "Income not found"}

    updated = False

    if amount is not None:
        income.amount = amount
        updated = True

    if description is not None:
        income.description = description
        updated = True

    if updated:
        income.created_at = datetime.datetime.now(datetime.UTC)
        income.save()
        return {"message": "Data updated successfully!"}

