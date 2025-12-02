import json
from pathlib import Path
from typing import List

from src.constants.properties import GPT_MODEL
from src.entities.db_model import Session, Chat
from src.entities.schema import NewChatSession, ChatHistoryItem, SessionInfo
from src.utils.llm_utils import client


async def create_new_session(new_chat: NewChatSession) -> Session:
    session = Session.create(user_id=new_chat.user_id, session_name=new_chat.chat_name)
    return session


async def validate_session(session_id: str) -> Session:
    session = Session.get_or_none(Session.id == session_id)
    return session

async def generate_response(prompt: str):
    system_prompt = Path("src/prompts/chat_prompt.jinja").read_text()
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=True
    )
    for chunk in response:
        if chunk.choices:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content

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