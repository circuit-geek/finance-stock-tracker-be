from fastapi import APIRouter, Depends

from src.services.dashboard_service import dashboard_stats, show_expenses_by_category, dashboard_graph_stats, \
    get_llm_insights
from src.utils.auth_utils import get_current_user


dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@dashboard_router.get("/stats")
async def stats_for_dashboard(user = Depends(get_current_user)):
    response = await dashboard_stats(user_id=user.id)
    return response

@dashboard_router.get("/show-expenses")
async def show_category_expenses(user = Depends(get_current_user)):
    response = await show_expenses_by_category(user_id=user.id)
    return response

@dashboard_router.get("/graph-stats")
async def stats_for_graph(user = Depends(get_current_user)):
    response = await dashboard_graph_stats(user_id=user.id)
    return response

@dashboard_router.get("/llm-insights")
async def latest_llm_insights(user = Depends(get_current_user)):
    response = await get_llm_insights(user_id=user.id)
    return response
