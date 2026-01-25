from fastapi import APIRouter, Depends

from src.entities.schema import UserInvestmentPreferences
from src.services.investment_advisor_service import save_user_investment_prefs, run_investment_advisor_agents
from src.utils.auth_utils import get_current_user

advisor_router = APIRouter(prefix="/advisor", tags=["Investment Advisor"])

@advisor_router.post("/save-preferences")
async def add_user_prefs(request: UserInvestmentPreferences, user=Depends(get_current_user)):
    response = await save_user_investment_prefs(request=request, user_id=user.id)
    return response

@advisor_router.post("/generate-insights")
async def generate_advisor_insights(user=Depends(get_current_user)):
    response = await run_investment_advisor_agents(user_id=user.id)
    return response

