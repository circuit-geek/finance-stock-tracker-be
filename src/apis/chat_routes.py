from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.entities.db_model import Chat
from src.entities.schema import NewChatSession
from src.services.chat_service import (
    create_new_session, get_session_history, validate_session,
    get_chat_history_in_session, stream_llm
)
from src.utils.auth_utils import get_current_user

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.post("/session/create")
async def create_session_route(new_chat: NewChatSession, user=Depends(get_current_user)):
    new_chat.user_id = user.id
    session = await create_new_session(new_chat)
    return {"session_id": str(session.id), "session_name": session.session_name}

@chat_router.post("/session/{session_id}/send")
async def send_message_route(session_id: str, prompt: str, user=Depends(get_current_user)):

    session = await validate_session(session_id)

    async def event_stream():
        full_response = ""
        async for chunk in stream_llm(prompt=prompt):
            full_response += chunk
            yield chunk

        Chat.create(
            session_id=str(session.id),
            user_message=prompt,
            assistant_message=full_response
        )

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@chat_router.get("/session/history")
async def get_history_route(user=Depends(get_current_user)):
    history = await get_session_history(user_id=user.id)
    return {"history": history}

@chat_router.get("/session/{session_id}/chat-history")
async def get_history_route(session_id: str, user=Depends(get_current_user)):
    history = await get_chat_history_in_session(session_id=session_id)
    return {"history": history}