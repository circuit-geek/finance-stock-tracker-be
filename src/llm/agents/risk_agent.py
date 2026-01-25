import datetime
import json
from datetime import timedelta
from pathlib import Path

from src.constants.properties import GPT_MODEL
from src.entities.db_model import User, Insights
from src.entities.schema import LLMInsightType, AgentName
from src.llm.tools.risk_tools import analyze_portfolio_composition_for_risk
from src.utils.llm_utils import client


async def get_user_risk_profile(user_id: str):
    user = User.get_or_none(User.id == user_id)
    if not user or not user.investment_preferences:
        return {}
    prefs = user.investment_preferences
    return {
        "risk_appetite": prefs.get("risk_appetite"),
        "investment_horizon": prefs.get("investment_horizon"),
        "investment_goals": prefs.get("goals")
    }

async def get_risk_analysis(user_id: str):
    # Check DB cache
    recent_insights = Insights.get_or_none(
        (Insights.user_id == user_id) &
        (Insights.agent_name == AgentName.RISK_AGENT.value)
    )
    now = datetime.datetime.now(datetime.UTC)
    if recent_insights:
        if isinstance(recent_insights.generated_date, str):
            gen_date = datetime.datetime.fromisoformat(recent_insights.generated_date)
        else:
            gen_date = recent_insights.generated_date
        
        if now <= gen_date + timedelta(days=7):
            print("Risk Agent: fetching from db")
            if isinstance(recent_insights.insights, dict):
                return recent_insights.insights
            return json.loads(recent_insights.insights)

    # Generate new insight
    profile = await get_user_risk_profile(user_id)
    # Use the shared tool for consistent risk analysis
    # Note: analyze_portfolio_composition_for_risk is synchronous, assuming DB operations are quick or using peewee sync
    portfolio_risk_metrics = analyze_portfolio_composition_for_risk(user_id)
    
    if not profile or not portfolio_risk_metrics:
        # Not enough info to run risk agent
        return {"error": "Insufficient user profile or portfolio data."}

    system_prompt = Path("src/llm/prompts/risk_agent_prompt.jinja").read_text()
    
    context_data = {
        **profile,
        **portfolio_risk_metrics
    }

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(context_data)}
        ],
        response_format={"type": "json_object"}
    )
    
    final_response = json.loads(response.choices[0].message.content)
    
    Insights.create(
        user_id = user_id,
        insight_type = LLMInsightType.AGENT_INVESTMENT_INSIGHT.value,
        agent_name = AgentName.RISK_AGENT.value,
        insights = final_response,
        generated_date = datetime.datetime.now(datetime.UTC)
    )
    
    return final_response
