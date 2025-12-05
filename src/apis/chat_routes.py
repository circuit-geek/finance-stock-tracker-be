import json

from fastapi import APIRouter, Depends, BackgroundTasks

from src.entities.schema import NewChatSession, UserChatInput
from src.services.chat_service import (
    create_new_session, get_session_history, validate_session,
    get_chat_history_in_session, generate_response, add_chat_to_db
)
from src.utils.auth_utils import get_current_user

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.post("/session/create")
async def create_session_route(new_chat: NewChatSession, user=Depends(get_current_user)):
    new_chat.user_id = user.id
    session = await create_new_session(new_chat)
    return {"session_id": str(session.id), "session_name": session.session_name}

@chat_router.post("/session/{session_id}/send")
async def send_message_route(session_id: str, request: UserChatInput,
                             background_task: BackgroundTasks , user=Depends(get_current_user)):

    session = await validate_session(session_id)
    response = await generate_response(request=request, user_id=user.id)
    if isinstance(response, str):
        try:
            response = json.loads(response)
        except json.JSONDecodeError:
            response = {"message": response}
    background_task.add_task(add_chat_to_db, str(session.id), request.prompt, response)
    return response

@chat_router.get("/session/history")
async def get_history_route(user=Depends(get_current_user)):
    history = await get_session_history(user_id=user.id)
    return {"history": history}

@chat_router.get("/session/{session_id}/chat-history")
async def get_history_route(session_id: str, user=Depends(get_current_user)):
    history = await get_chat_history_in_session(session_id=session_id)
    return {"history": history}