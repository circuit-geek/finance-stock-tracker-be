from src.entities.db_model import Investments
from src.llm.tools.portfolio_tools import total_invested


def get_current_allocation(user_id: str) -> dict:
    """This will get the current asset allocation across entire portfolio"""
    current_investments = list(Investments.select().where(Investments.user_id == user_id))
    print(current_investments)
    investments_allocator = []
    for investment in current_investments:
        investments_allocator.append({
            "investment_type": investment.investment_type,
            "amount": investment.amount,
            "quantity": investment.quantity,
            "ticker": investment.symbol,
            "purchased_date": investment.purchased_at
        })

    print("assets_allocation", investments_allocator)
    total_invested_value = total_invested(portfolio_lst=investments_allocator)
    print("total_invested", total_invested_value)
    if total_invested_value == 0:
        return {}

    allocation_value = {}
    for investment_value in investments_allocator:
        inv_type = investment_value["investment_type"]
        inv_value = (investment_value["amount"] * investment_value["quantity"])/total_invested_value
        allocation_value[inv_type] = allocation_value.get(inv_type, 0) + inv_value
    return allocation_value

def analyze_portfolio_composition_for_risk(user_id: str) -> dict:
    """Detects high concentration in any single assets"""
    allocation_fraction = get_current_allocation(user_id)
    if not allocation_fraction:
        return {
            "asset_allocation_pct": {},
            "concentration_flags": []
        }

    allocation_pct = {
        asset: round(value * 100, 2)
        for asset, value in allocation_fraction.items()
    }
    concentration_flags = []
    for asset, pct in allocation_pct.items():
        if pct > 60:
            concentration_flags.append(
                f"High concentration detected in {asset} ({pct}%)."
            )

    return {
        "asset_allocation_pct": allocation_pct,
        "concentration_flags": concentration_flags
    }