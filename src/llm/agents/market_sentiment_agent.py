import datetime
import json
from datetime import timedelta
from pathlib import Path

from src.constants.properties import GPT_MODEL, ALPHA_VANTAGE_KEY
from src.entities.db_model import Investments, Insights
from src.entities.schema import LLMInsightType, AgentName
from src.llm.tools.market_sentiment_tool import get_market_sentiment
from src.utils.llm_utils import client


async def get_tickers_to_extract(user_id: str):
    investments = Investments.select().where(Investments.user_id == user_id)
    ticker_lst = []
    for investment in investments:
        ticker_lst.append(investment.symbol)
    return ticker_lst

async def get_market_sentiments(user_id: str):
    get_user_tickers = await get_tickers_to_extract(user_id=user_id)
    market_sentiments = get_market_sentiment(tickers=get_user_tickers, api_key=ALPHA_VANTAGE_KEY)
    return market_sentiments

async def get_market_agent_insights(user_id: str):
    recent_insights = Insights.get_or_none(
        (Insights.user_id == user_id) &
        (Insights.agent_name == AgentName.MARKET_SENTIMENT_AGENT.value)
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

    system_prompt = Path("src/llm/prompts/market_sentiment_agent_prompt.jinja").read_text()
    get_market_sentiment_data = get_market_sentiments(user_id=user_id)
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(get_market_sentiment_data)}
        ]
    )
    final_response = json.loads(response.choices[0].message.content)
    Insights.create(
        user_id = user_id,
        insight_type = LLMInsightType.AGENT_INVESTMENT_INSIGHT.value,
        agent_name = AgentName.MARKET_SENTIMENT_AGENT.value,
        insights = final_response,
        generated_date = datetime.datetime.now(datetime.UTC)
    )
    return final_response