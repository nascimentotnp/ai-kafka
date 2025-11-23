from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.schemas.schema import ChatResponse, ChatRequest
from src.services.bot_service import bot

chat_router = APIRouter()


@chat_router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.msg.strip():
        raise HTTPException(status_code=400, detail="Campo 'msg' é obrigatório.")

    answer = bot(req.msg)
    return ChatResponse(resposta=answer)
