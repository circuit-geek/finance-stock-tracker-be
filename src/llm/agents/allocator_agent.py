import datetime
import json
from datetime import timedelta
from pathlib import Path

from src.constants.properties import GPT_MODEL
from src.entities.db_model import Insights
from src.entities.schema import LLMInsightType, AgentName
from src.llm.tools.allocator_tools import provide_acceptable_allocations
from src.llm.tools.risk_tools import get_current_allocation
from src.utils.llm_utils import client


async def get_latest_agent_output(user_id: str, agent_name: str):
    insight = Insights.select().where(
        (Insights.user_id == user_id) & 
        (Insights.agent_name == agent_name)
    ).order_by(Insights.generated_date.desc()).first()
    
    if insight:
        try:
             return json.loads(insight.insights)
        except:
             return insight.insights
    return None

async def get_allocation_suggestions(user_id: str):
    # Check DB cache
    recent_insights = Insights.get_or_none(
        (Insights.user_id == user_id) &
        (Insights.agent_name == AgentName.ASSET_ALLOCATOR_AGENT.value)
    )
    now = datetime.datetime.now(datetime.UTC)
    if recent_insights:
        if isinstance(recent_insights.generated_date, str):
            gen_date = datetime.datetime.fromisoformat(recent_insights.generated_date)
        else:
            gen_date = recent_insights.generated_date
        
        if now <= gen_date + timedelta(days=7):
            print("Allocator Agent: fetching from db")
            if isinstance(recent_insights.insights, dict):
                return recent_insights.insights
            return json.loads(recent_insights.insights)

    # Gather Context
    # Use allocator tool to get target ranges
    try:
        acceptable_ranges = provide_acceptable_allocations(user_id)
    except ValueError as e:
        return {"error": str(e)}

    # Use risk tools to get current allocation (standardized)
    current_allocation = get_current_allocation(user_id)
    
    risk_output = await get_latest_agent_output(user_id, AgentName.RISK_AGENT.value)
    market_output = await get_latest_agent_output(user_id, AgentName.MARKET_SENTIMENT_AGENT.value)
    
    # Prepare Prompt Input
    context_data = {
        "user_profile": acceptable_ranges, # Contains goals, risk appetite, and ideal ranges
        "current_allocation": current_allocation,
        "risk_analysis_summary": risk_output.get("analysis_summary", "Not available") if risk_output else "Not available",
        "market_sentiment_summary": market_output if market_output else "Not available"
    }

    system_prompt = Path("src/llm/prompts/allocator_agent_prompt.jinja").read_text()
    
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
        agent_name = AgentName.ASSET_ALLOCATOR_AGENT.value,
        insights = final_response,
        generated_date = datetime.datetime.now(datetime.UTC)
    )
    
    return final_response
