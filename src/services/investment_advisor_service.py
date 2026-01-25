from fastapi import HTTPException, status

from src.entities.db_model import User
from src.entities.schema import UserInvestmentPreferences, UserInvestmentPreferencesSaved
from src.llm.agents.portfolio_agent import get_portfolio_agent_insights
from src.llm.agents.market_sentiment_agent import get_market_agent_insights
from src.llm.agents.risk_agent import get_risk_analysis
from src.llm.agents.allocator_agent import get_allocation_suggestions
from src.llm.agents.aggregator_agent import get_aggregated_insights

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

async def run_investment_advisor_agents(user_id: str):
    # 1. Portfolio Agent
    print("Running Portfolio Agent...")
    await get_portfolio_agent_insights(user_id)
    
    # 2. Market Sentiment Agent
    print("Running Market Sentiment Agent...")
    await get_market_agent_insights(user_id)
    
    # 3. Risk Agent
    print("Running Risk Agent...")
    await get_risk_analysis(user_id)
    
    # 4. Allocator Agent
    print("Running Allocator Agent...")
    await get_allocation_suggestions(user_id)
    
    # 5. Aggregator Agent
    print("Running Aggregator Agent...")
    final_insight = await get_aggregated_insights(user_id)
    
    return final_insight