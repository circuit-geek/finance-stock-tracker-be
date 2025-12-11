import json

import requests
from src.constants.properties import ALPHA_VANTAGE_KEY
from typing import List

def get_market_sentiment(tickers: List[str], api_key: str):
    high_relevant_news = []
    ticker_str = ",".join(tickers)
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker_str}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    news_items = data.get("feed", [])
    for news in news_items:
        ticker_sentiments = news.get("ticker_sentiment", [])
        for ts in ticker_sentiments:
            ticker = ts.get("ticker")
            if ticker in tickers:
                score = ts.get("relevance_score", "")
                score = float(score)
                if score > 0.9:
                    high_relevant_news.append({
                        "ticker": ticker,
                        "title": news.get("title"),
                        "url": news.get("url"),
                        "summary": news.get("summary"),
                        "relevance_score": score,
                        "ticker_sentiment_score": ts.get("ticker_sentiment_score")
                    })

    return high_relevant_news
