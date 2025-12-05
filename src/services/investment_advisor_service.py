from fastapi import HTTPException, status

from src.entities.db_model import User
from src.entities.schema import UserInvestmentPreferences, UserInvestmentPreferencesSaved

async def save_user_investment_prefs(request: UserInvestmentPreferences,
                                     user_id: str) -> UserInvestmentPreferencesSaved:
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not valid user")

    user.investment_preferences = request.model_dump()
    user.save()
    return UserInvestmentPreferencesSaved(
        message="The user preferences have been saved",
        investment_goals=request.investment_goals,
        investment_horizon=request.investment_horizon,
        investment_types=request.investment_types,
        monthly_investment_amount=request.monthly_investment_amount,
        risk_appetite=request.risk_appetite
    )