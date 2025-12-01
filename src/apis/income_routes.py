from fastapi import APIRouter, Depends

from src.entities.schema import AddIncome
from src.services.income_service import (
    add_new_income, show_all_income,
    delete_income, update_income
)
from src.utils.auth_utils import get_current_user
from typing import Optional

income_router = APIRouter(prefix="/income", tags=["Income"])

@income_router.post("/add-new-income")
async def new_income(request: AddIncome, user = Depends(get_current_user)):
    response = await add_new_income(income=request, user_id=user.id)
    return response

@income_router.get("/show-all-income")
async def show_income(user = Depends(get_current_user)):
    response = await show_all_income(user_id=user.id)
    return response

@income_router.delete("/delete-income/{income_id}")
async def delete_income_by_id(income_id: str, user=Depends(get_current_user)):
    response = await delete_income(income_id=income_id)
    return response

@income_router.patch("/update-income/{income_id}")
async def update_income_by_id(income_id: str, amount: Optional[float] = None,
                              description: Optional[str] = None, user=Depends(get_current_user)):
    response = await update_income(income_id=income_id, amount=amount, description=description)
    return response