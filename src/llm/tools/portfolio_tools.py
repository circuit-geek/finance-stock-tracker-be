import datetime
from datetime import timedelta
from typing import List
from pydantic_ai import FunctionToolset

import yfinance


def get_current_share_price(ticker: str) -> float:
    """Retrieves the current share price for a given stock"""
    stock_data = yfinance.Ticker(ticker=ticker).info
    market_price = stock_data.get("regularMarketPrice")
    return market_price

def get_share_price_on_purchase_date(ticker: str, purchased_date: datetime.datetime) -> float:
    """Retrieves the share price of a stock on purchased date"""
    if isinstance(purchased_date, str):
        purchased_date = datetime.datetime.fromisoformat(purchased_date)
    start = purchased_date.date()
    end = start + timedelta(days=7)
    stock = yfinance.Ticker(ticker)
    df = stock.history(start=start, end=end)
    return df["Close"].iloc[0]

def calculate_portfolio_value(portfolio_lst: List[dict]) -> float:
    """
    Calculates the total portfolio value by extracting the ticker, quantity and purchase_date
    example portfolio_lst:
    [{
        ticker: "MSFT",
        quantity: 5,
        purchase_date: datetime.datetime value
    }]
    """
    total_value = 0.0
    for stock in portfolio_lst:
        ticker = stock.get("ticker")
        quantity = stock.get("quantity")

        if ticker and quantity:
            current_price = get_current_share_price(ticker)
            if current_price:
                total_value += quantity * current_price

    return total_value

def total_invested(portfolio_lst: List[dict]) -> float:
    """Calculates the total amount invested across all stocks in the portfolio"""
    total_investment = 0.0

    for stock in portfolio_lst:
        ticker = stock.get("ticker")
        quantity = stock.get("quantity")
        purchase_date = stock.get("purchase_date")

        if ticker and quantity and purchase_date:
            purchase_price = get_share_price_on_purchase_date(ticker, purchase_date)
            if purchase_price:
                total_investment += quantity * purchase_price

    return total_investment

def total_gain_loss(portfolio_lst: List[dict]) -> float:
    """Calculates the total gain or loss across all stocks in the portfolio"""
    total_gl = 0.0

    for stock in portfolio_lst:
        ticker = stock.get("ticker")
        quantity = stock.get("quantity")
        purchase_date = stock.get("purchase_date")

        if ticker and quantity and purchase_date:
            current_price = get_current_share_price(ticker)
            purchase_price = get_share_price_on_purchase_date(ticker, purchase_date)

            if current_price and purchase_price:
                total_gl += quantity * (current_price - purchase_price)

    return total_gl

def portfolio_return_percent(portfolio_lst: List[dict]) -> float:
    """Calculates the portfolio return as a percentage"""
    total_gl = total_gain_loss(portfolio_lst)
    total_inv = total_invested(portfolio_lst)

    if total_inv == 0:
        return 0.0

    return (total_gl / total_inv) * 100


def analyze_single_stock(ticker: str, quantity: int, purchase_date: datetime.datetime) -> dict:
    """Analyzes a single stock investment and returns all metrics."""
    buy_price = get_share_price_on_purchase_date(ticker, purchase_date)
    current_price = get_current_share_price(ticker)
    invested_amount = buy_price * quantity
    current_value = current_price * quantity
    gain_loss = current_value - invested_amount
    return_percentage = (gain_loss / invested_amount) * 100

    return {
        "ticker": ticker,
        "quantity": quantity,
        "buy_price": buy_price,
        "current_price": current_price,
        "invested_amount": invested_amount,
        "current_value": current_value,
        "gain_loss": gain_loss,
        "return_percentage": return_percentage
    }

portfolio_toolset = FunctionToolset(tools=[get_current_share_price, get_share_price_on_purchase_date,
                                           calculate_portfolio_value, portfolio_return_percent,
                                           total_invested, total_gain_loss, analyze_single_stock])