from fastapi import APIRouter, Depends

from src.entities.schema import AddExpense
from src.services.expense_service import (
    add_new_expense, show_all_expense,
    delete_expense, update_expense, expense_stats
)
from src.utils.auth_utils import get_current_user
from typing import Optional

expense_router = APIRouter(prefix="/expense", tags=["Expenses"])

@expense_router.post("/add-new-expense")
async def new_expense(request: AddExpense, user = Depends(get_current_user)):
    response = await add_new_expense(expense=request, user_id=user.id)
    return response

@expense_router.get("/show-all-expense")
async def show_expense(user = Depends(get_current_user)):
    response = await show_all_expense(user_id=user.id)
    return response

@expense_router.delete("/delete-expense/{expense_id}")
async def delete_expense_by_id(expense_id: str, user=Depends(get_current_user)):
    response = await delete_expense(expense_id=expense_id)
    return response

@expense_router.patch("/update-expense/{expense_id}")
async def update_expense_by_id(expense_id: str, amount: Optional[float] = None,
                               description: Optional[str] = None, user=Depends(get_current_user)):
    response = await update_expense(expense_id=expense_id, amount=amount, description=description)
    return response

@expense_router.get("/show-expense-stats")
async def show_expense_stats(user=Depends(get_current_user)):
    response = await expense_stats(user_id=user.id)
    return response