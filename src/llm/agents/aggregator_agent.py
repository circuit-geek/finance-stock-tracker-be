import datetime
import json
from datetime import timedelta
from pathlib import Path

from src.constants.properties import GPT_MODEL
from src.entities.db_model import Insights
from src.entities.schema import LLMInsightType, AgentName
from src.utils.llm_utils import client


async def get_latest_agent_output(user_id: str, agent_name: str):
    insight = Insights.select().where(
        (Insights.user_id == user_id) & 
        (Insights.agent_name == agent_name)
    ).order_by(Insights.generated_date.desc()).first()
    
    if insight:
         # Simplified parsing, assuming strict JSON storage
        try:
             return json.loads(insight.insights)
        except:
             return insight.insights
    return "No Data Available"

async def get_aggregated_insights(user_id: str):
    # Check DB cache
    recent_insights = Insights.get_or_none(
        (Insights.user_id == user_id) &
        (Insights.agent_name == AgentName.AGGREGATOR_AGENT.value)
    )
    now = datetime.datetime.now(datetime.UTC)
    if recent_insights:
        if isinstance(recent_insights.generated_date, str):
            gen_date = datetime.datetime.fromisoformat(recent_insights.generated_date)
        else:
            gen_date = recent_insights.generated_date
        
        if now <= gen_date + timedelta(days=7):
            print("Aggregator Agent: fetching from db")
            if isinstance(recent_insights.insights, dict):
                return recent_insights.insights
            return json.loads(recent_insights.insights)

    # Gather Context
    portfolio_out = await get_latest_agent_output(user_id, AgentName.PORTFOLIO_AGENT.value)
    market_out = await get_latest_agent_output(user_id, AgentName.MARKET_SENTIMENT_AGENT.value)
    risk_out = await get_latest_agent_output(user_id, AgentName.RISK_AGENT.value)
    allocator_out = await get_latest_agent_output(user_id, AgentName.ASSET_ALLOCATOR_AGENT.value)

    # Prepare Prompt Input
    context_data = {
        "portfolio_insight": portfolio_out,
        "market_sentiment_insight": market_out,
        "risk_insight": risk_out,
        "allocator_insight": allocator_out
    }

    system_prompt = Path("src/llm/prompts/aggregator_agent_prompt.jinja").read_text()
    
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
        agent_name = AgentName.AGGREGATOR_AGENT.value,
        insights = final_response,
        generated_date = datetime.datetime.now(datetime.UTC)
    )
    
    return final_response
