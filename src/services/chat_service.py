from pathlib import Path
from typing import List
from src.entities.db_model import Session, Chat
from src.entities.schema import (NewChatSession, ChatHistoryItem, SessionInfo,
                                 IncomeType, ExpenseType, InvestmentType)
from src.utils.llm_utils import get_completion
from src.llm.cb_tools import GetInfoFromOnline, AddIncome, AddExpense, AddInvestment


async def create_new_session(new_chat: NewChatSession) -> Session:
    session = Session.create(user_id=new_chat.user_id, session_name=new_chat.chat_name)
    return session


async def validate_session(session_id: str) -> Session:
    session = Session.get_or_none(Session.id == session_id)
    return session

async def generate_response(prompt: str, user_id: str):
    system_prompt = Path("src/prompts/chat_prompt.jinja").read_text()
    income_types = f"""
    the income type is one among {[x for x in IncomeType]}
    """
    expense_types = f"""
    the expense type is one among {[x for x in ExpenseType]}
    """
    investment_types = f"""
    the investment type is one among {[x for x in InvestmentType]}
    """
    messages = [
        {"role": "system", "content": system_prompt + income_types + expense_types + investment_types},
        {"role": "user", "content": prompt}
    ]

    tool_functions = [GetInfoFromOnline, AddIncome, AddExpense, AddInvestment]
    response = get_completion(messages=messages, tool_functions=tool_functions, user_id= user_id)
    return response

async def get_session_history(user_id: str) -> List[SessionInfo]:
    query = Session.select().where(Session.user_id == user_id)

    sessions = []
    for session in query:
        sessions.append(SessionInfo(
            id=str(session.id),
            user_id=str(session.user_id),
            session_name=session.session_name
        ))

    return sessions


async def get_chat_history_in_session(session_id: str) -> List[ChatHistoryItem]:

    session = await validate_session(session_id)
    query = Chat.select().where(Chat.session_id == str(session.id))

    history = []
    for chat in query:
        history.append(ChatHistoryItem(
            id=str(chat.id),
            user_message=chat.user_message,
            assistant_message=chat.assistant_message
        ))

    return history

async def add_chat_to_db(session_id: str, user_message, assistant_message):
    Chat.create(
        session_id = session_id,
        user_message = user_message,
        assistant_message = assistant_message
    )