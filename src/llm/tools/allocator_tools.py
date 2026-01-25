from src.entities.db_model import User

def provide_acceptable_allocations(user_id: str) -> dict:
    """Provide allocations based on user risk appetite and investment horizon"""
    user = User.get_or_none(User.id == user_id)
    if not user or user.investment_preferences is None:
        raise ValueError("User or User's investment preferences not found!")
    risk_appetite = user.investment_preferences["risk_appetite"]
    investment_horizon = user.investment_preferences["investment_horizon"]

    base_risk_rules = {
        "low_risk": {
            "stocks": (0, 40),
            "mutual_funds": (30, 60),
            "crypto": (0, 5),
            "bonds": (20, 50)
        },
        "medium_risk": {
            "stocks": (40, 70),
            "mutual_funds": (20, 50),
            "crypto": (0, 10),
            "bonds": (10, 30)
        },
        "high_risk": {
            "stocks": (60, 85),
            "mutual_funds": (10, 40),
            "crypto": (0, 20),
            "bonds": (0, 20)
        }
    }

    rules = base_risk_rules.get(risk_appetite)
    if not rules:
        raise ValueError(f"Invalid risk appetite: {risk_appetite}")

    horizon_bonus = 0
    if investment_horizon in ["5-10_years", "10+_years"]:
        horizon_bonus = 5

    adjusted_rules = {}
    for asset, (min_pct, max_pct) in rules.items():
        adjusted_rules[asset] = (
            min_pct,
            min(100, max_pct + horizon_bonus)
        )

    return {
        "risk_appetite": risk_appetite,
        "investment_horizon": investment_horizon,
        "acceptable_allocation_ranges": adjusted_rules
    }
