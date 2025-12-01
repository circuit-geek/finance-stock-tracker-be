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