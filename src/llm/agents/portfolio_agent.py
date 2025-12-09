import datetime
import json
from datetime import timedelta
from pathlib import Path

from src.constants.properties import GPT_MODEL
from src.entities.db_model import Investments, Insights
from src.entities.schema import LLMInsightType, AgentName
from src.llm.tools.portfolio_tools import (
    calculate_portfolio_value, portfolio_return_percent,
    total_invested, total_gain_loss, analyze_single_stock
)
from src.utils.llm_utils import client


async def get_portfolio_lst(user_id: str):
    investments = Investments.select().where(Investments.user_id == user_id)
    portfolio_lst = []
    for investment in investments:
        portfolio_lst.append({
            "ticker": investment.symbol,
            "quantity": investment.quantity,
            "purchase_date": investment.purchased_at,
            "investment_type": investment.investment_type
        })

    return portfolio_lst

async def prepare_for_portfolio_insight(user_id: str):
    portfolio_data = await get_portfolio_lst(user_id=user_id)
    total_portfolio = calculate_portfolio_value(portfolio_lst=portfolio_data)
    total_invested_value = total_invested(portfolio_lst=portfolio_data)
    total_gain_and_loss = total_gain_loss(portfolio_lst=portfolio_data)
    portfolio_returns = portfolio_return_percent(portfolio_lst=portfolio_data)

    individual_stock_data = []
    for stock in portfolio_data:
        individual_stock_data.append(
            analyze_single_stock(ticker=stock["ticker"], quantity=stock["quantity"],
                                 purchase_date=stock["purchased_date"])
        )

    return {
        "portfolio_value": total_portfolio,
        "total_invested_value": total_invested_value,
        "total_gain_and_loss": total_gain_and_loss,
        "portfolio_returns": portfolio_returns,
        "single_stock_data": individual_stock_data
    }

async def get_portfolio_agent_insights(user_id: str):
    recent_insights = Insights.get_or_none(
        (Insights.user_id == user_id) &
        (Insights.agent_name == AgentName.PORTFOLIO_AGENT.value)
    )
    now = datetime.datetime.now(datetime.UTC)
    if recent_insights:
        if isinstance(recent_insights.generated_date, str):
            generated_date = datetime.datetime.fromisoformat(recent_insights.generated_date)
        else:
            generated_date = recent_insights.generated_date
        seven_days_later = generated_date + timedelta(days=7)
        if now <= seven_days_later:
            print("fetching from db")
            return json.loads(recent_insights.insights)

    system_prompt = Path("src/llm/prompts/portfolio_agent_prompt.jinja").read_text()
    portfolio_data = prepare_for_portfolio_insight(user_id=user_id)
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(portfolio_data)}
        ]
    )
    final_response = json.loads(response.choices[0].message.content)
    Insights.create(
        user_id = user_id,
        insight_type = LLMInsightType.AGENT_INVESTMENT_INSIGHT.value,
        agent_name = AgentName.PORTFOLIO_AGENT.value,
        insights = final_response,
        generated_date = datetime.datetime.now(datetime.UTC)
    )
    return final_response