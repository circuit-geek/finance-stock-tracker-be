## Finance and Stock Advisor (FinSage)

- **Steps to run**:
  1) `git clone https://github.com/circuit-geek/finance-stock-tracker-be.git`
  2) `cd finance-stock-tracker-be`
  3) `uv sync`
  4) `uv run uvicorn src.main:app --reload`

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

**Insights Table**
```{python}
{
    "id": "63216892-34a2-4925-b9cb-61c97b265043",
    "user_id": "63216892-34a2-4925-ab87-61c97b265043",
    "insight_type": "dashboard or agent (enum)"
    "insights": "summary-of-insights",
    "generated_date": "datetime"
}
```
- Display the insights of most recent-date.
