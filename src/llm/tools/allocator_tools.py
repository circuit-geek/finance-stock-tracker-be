from src.entities.db_model import Investments
from src.llm.tools.portfolio_tools import total_invested
from src.entities.db_model import db_init

db_init()

def get_current_allocation(user_id: str) -> dict:
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
        allocation_value[inv_type] = allocation_value.get(inv_type) + inv_value

    return allocation_value


def main():
    result = get_current_allocation(user_id="7c3c43b47db64d37b9423c3317df85e2")
    print(result)

if __name__ == "__main__":
    main()