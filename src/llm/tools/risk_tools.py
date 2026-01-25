from src.entities.db_model import Investments
from src.llm.tools.portfolio_tools import analyze_single_stock, calculate_portfolio_value

def get_current_allocation(user_id: str) -> dict:
    """This will get the current asset allocation across entire portfolio based on Market Value"""
    current_investments = list(Investments.select().where(Investments.user_id == user_id))
    
    investment_list = []
    # Prepare list for calculate_portfolio_value equivalent
    for inv in current_investments:
        investment_list.append({
            "ticker": inv.symbol,
            "quantity": inv.quantity,
            "purchase_date": inv.purchased_at,
            "investment_type": inv.investment_type,
            "amount": inv.amount # Fallback
        })
        
    # We need total market value to calculate percentage
    # We can iterate and sum up
    
    type_value_map = {}
    total_market_value = 0.0
    
    for inv in investment_list:
        if inv["ticker"] and inv["quantity"]:
            # Use real market data
            # Note: analyze_single_stock fetches price. This might be slow if many stocks.
            # But essential for correct risk profile.
            metrics = analyze_single_stock(inv["ticker"], inv["quantity"], inv["purchase_date"])
            market_val = metrics["current_value"]
        else:
            # Fallback for assets without ticker (e.g. manual real estate entry)
            # Assuming 'amount' is total value in this case
            market_val = inv["amount"]
            
        total_market_value += market_val
        inv_type = inv["investment_type"]
        type_value_map[inv_type] = type_value_map.get(inv_type, 0) + market_val
        
    if total_market_value == 0:
        return {}

    allocation_value = {}
    for inv_type, val in type_value_map.items():
        allocation_value[inv_type] = val / total_market_value
        
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