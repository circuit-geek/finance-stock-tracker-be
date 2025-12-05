## Finance and Stock Advisor (FinSage)

- This application will track finances and also be a real-time investment advisor.
- There are 3 parts to it:
    1) **Finance Tracker** - Which can take input through modal or can upload a pic or pdf, if upload option is chosen that an LLM would extract information from it.
    2) **Chatbot** - This is a generic chatbot which you can talk about your finances or anything finance in general.
    3) **Investment Advisor** - All the investments done will be fed through multiple agents, which would constantly track the portfolio and suggest changes.

### Endpoints Needed:

- `/users/register` => POST
- `/users/login` => POST
- `/users/logout` => POST
- `/dashboard/stats` => GET
- `/dashboard/investment-performance-graph` => POST
- `/dashboard/top-spending` => GET
- `/dashboard/recent-notifications` => GET
- `/dashboard/latest-llm-insights` => GET
- `/income/add-income` => POST
- `/income/{income_id}/update-income` => PATCH
- `/income/{income_id}/delete-income` => DELETE
- `/income/show-income-history` => GET
- `/expense/add-expense` => POST
- `/expense/{expense_id}/update-expense` => PATCH
- `/expense/{expense_id}/delete-expense` => DELETE
- `/expense/show-expense-history` => GET
- `/investment/add-investment` => POST
- `/investment/{investment_id}/update-investment` => PATCH
- `/investment/{investment_id}/delete-investment` => DELETE
- `/investment/show-investment-history` => GET
- `/chat/session/create` => POST
- `/chat/session/{session_id}/send` => POST
- `/chat/session/history` => GET
- `/chat/session/{session_id}/chat-history` => GET

### Tables Needed:

- Users 
- Income
- Expenses
- Investment
- Session
- Chat
- Insights

### Chatbot Ideas:

- The user can interact with the chatbot to ask question regarding his portfolio, income and expenses.
- There will be an agent who has access to the user data of that particular user.
- This will enable the agent to effectively answer the user queries.
- The chatbot will have a Streaming Response.

### Chatbot Tools Ideas:

    1) add_income or expenses or investment through chat
    2) summary of expenses or investments 
    3) get_stock_price or information about company (yfinance API) 
    4) finance terms and details (Tavily API) 
    5) tool to search transactions

**Updated Users Table** => After inclusion of Investment Advisor
```{python}
{
    "id": "63216892-34a2-4925-b9cb-61c97b265043",
    "name": "Gaurav",
    "email_id": "gp@email.com",
    "password": "some-hashed-password",
    "dob": "21st Dec 2001 in (datetime format)",
    "investment_preferences": {
          "goals": ["wealth_creation", "retirement_planning"],
          "risk_appetite": "medium_risk",
          "investment_horizon": "5-10_years",
          "investment_type": ["stocks", "crypto"],
          "monthly_investment_capacity": 1000
    }
}
```

### Investment Advisor Ideas
- The first time user enter this page, there will be a modal which will take the user preferences about their investment goals and risk appetite.
- There will be multiple agents who will be coordinating and communicating with each other.
- **List of agents**:
    1) Portfolio Monitor Agent => This agent will monitor the portfolio and show returns   
    2) Risk Monitor Agent => This agent would act based on the user preference of risk and time horizon and existing portfolio and qualitatively evaluate the risk
    3) Market Sentiment Agent => This agent would collect the news of that company to give latest insights about all the companies of the user.
    4) Asset Allocator Agent => Based on the info collected from the Risk and Market agent and user preference goals this would suggest changes in asset allocations.
    5) Aggregator Agent => This agent is responsible for aggregating the responses from other agents, summarize their finding in 4-5 lines which would be given as the insights and stored in db. 

- Things to consider: Build agents independently and let them communicate with each other through network (A2A and MCP) or build graph based agent communication(Langgraph/Pydantic graph)?

**Insights Table**
```{python}
{
    "id": "63216892-34a2-4925-b9cb-61c97b265043",
    "user_id": "63216892-34a2-4925-ab87-61c97b265043",
    "insights": [
        {
            "date": 28-11-2025,
            "insights": ["insight-1", "insight-2", "insight-3", "insight-4", "insight-5"]
        },
        {
            "date": 05-12-2025,
            "insights": ["insight-1", "insight-2", "insight-3", "insight-4", "insight-5"]
        }
    ]
}
```
- Display the insights of most recent-date.
- Things to decide:
  1) How often to run the agents (weekly once?)
  2) Should aggregator run everytime there is a new output from agents? 