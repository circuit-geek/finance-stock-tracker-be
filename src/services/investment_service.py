import datetime

from src.entities.db_model import Investments
from src.entities.schema import AddInvestment, ShowInvestment
from typing import List, Optional

async def add_new_investment(investment: AddInvestment, user_id: str):
    investment_type = investment.investment_type
    amount = investment.amount
    description = investment.description
    symbol = investment.symbol
    quantity = investment.quantity
    purchased_at = investment.purchased_at
    created_at = investment.created_at

    new_investment = Investments.create(
        user_id = user_id,
        investment_type = investment_type,
        amount = amount,
        description = description,
        symbol = symbol,
        quantity = quantity,
        purchased_at = purchased_at,
        created_at = created_at
    )

    return {
        "message": "Added new investment",
        "income_id": new_investment.id
    }

async def show_all_investments(user_id: str) -> List[ShowInvestment]:
    query = Investments.select().where(Investments.user_id == user_id)
    output = []
    for value in query:
        output.append(ShowInvestment(
            investment_id=str(value.id),
            investment_type=value.investment_type,
            amount=value.amount,
            description=value.description,
            created_at=value.created_at
        ))
    return output

async def delete_investment(investment_id: str):
    Investments.delete().where(Investments.id == investment_id).execute()
    return {
        "message": "Investments deleted successfully!",
        "investment_id": investment_id
    }

async def update_investment(investment_id: str, amount: Optional[float], description: Optional[str]):
    investment = Investments.get_or_none(Investments.id == investment_id)
    if not investment:
        return {"message": "Investments not found"}

    updated = False

    if amount is not None:
        investment.amount = amount
        updated = True

    if description is not None:
        investment.description = description
        updated = True

    if updated:
        investment.created_at = datetime.datetime.now(datetime.UTC)
        investment.save()
        return {"message": "Data updated successfully!"}

async def investment_stats(user_id: str):
    investments = list(Investments.select().where(Investments.user_id == user_id))
    total_entries = len(investments)
    unique_categories = set()
    for investment in investments:
        if investment.investment_type not in unique_categories:
            unique_categories.add(investment.investment_type)

    total_categories = len(unique_categories)
    total_investment = 0
    for investment in investments:
        total_investment += investment.amount

    return {
        "total_amount": total_investment,
        "total_entries": total_entries,
        "categories": total_categories
    }
