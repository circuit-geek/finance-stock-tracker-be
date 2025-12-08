from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from src.constants.properties import GPT_MODEL
from src.llm.tools.portfolio_tools import (
    get_current_share_price, get_share_price_on_purchase_date,
    total_gain_loss, total_invested,
    calculate_portfolio_value, portfolio_return_percent
)

system_prompt = Path("src/llm/prompts/portfolio_agent_prompt.jinja").read_text()

portfolio_agent = LlmAgent(
    name="Portfolio Agent",
    model=LiteLlm(model=GPT_MODEL),
    instruction=system_prompt,
    tools=[get_current_share_price, get_share_price_on_purchase_date,
           total_gain_loss, total_invested, calculate_portfolio_value, portfolio_return_percent]
)
