import asyncio
import json
from pathlib import Path

from pydantic_ai.agent import Agent

from src.entities.db_model import Investments
from src.llm.tools.portfolio_tools import portfolio_toolset
from src.utils.agent_utils import azure_model
from src.entities.db_model import db_init

db_init()

system_prompt = Path("src/llm/prompts/portfolio_agent_prompt.jinja").read_text()

async def get_portfolio_agent_response(user_id: str):
    investments = Investments.select().where(Investments.user_id == user_id)
    portfolio_lst = []
    for investment in investments:
        portfolio_lst.append({
            "ticker": investment.symbol,
            "quantity": investment.quantity,
            "purchase_date": investment.purchased_at,
            "investment_type": investment.investment_type
        })
    print(json.dumps(portfolio_lst, indent=4))

    portfolio_agent = Agent(
        model=azure_model,
        system_prompt=system_prompt,
        toolsets=[portfolio_toolset]
    )
    response = await portfolio_agent.run(user_prompt=f"Give the analysis for this {portfolio_lst}")
    print(response)

if __name__ == "__main__":
    asyncio.run(get_portfolio_agent_response(user_id="c1667321-24ea-447a-afeb-98bcffd3e71a"))
