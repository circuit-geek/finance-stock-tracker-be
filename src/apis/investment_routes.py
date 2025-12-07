from fastapi import APIRouter, Depends

from src.entities.schema import AddInvestment
from src.services.investment_service import (
    add_new_investment, show_all_investments,
    delete_investment, update_investment, investment_stats
)
from src.utils.auth_utils import get_current_user
from typing import Optional

investment_router = APIRouter(prefix="/investment", tags=["Investment"])

@investment_router.post("/add-new-investment")
async def new_investment(request: AddInvestment, user = Depends(get_current_user)):
    response = await add_new_investment(investment=request, user_id=user.id)
    return response

@investment_router.get("/show-all-investment")
async def show_investments(user = Depends(get_current_user)):
    response = await show_all_investments(user_id=user.id)
    return response

@investment_router.delete("/delete-investment/{investment_id}")
async def delete_investment_by_id(investment_id: str, user=Depends(get_current_user)):
    response = await delete_investment(investment_id=investment_id)
    return response

@investment_router.patch("/update-investment/{investment_id}")
async def update_investment_by_id(investment_id: str, amount: Optional[float] = None,
                                  description: Optional[str] = None, user=Depends(get_current_user)):
    response = await update_investment(investment_id=investment_id, amount=amount, description=description)
    return response

@investment_router.get("/show-investment-stats")
async def show_investment_stats(user=Depends(get_current_user)):
    response = await investment_stats(user_id=user.id)
    return response