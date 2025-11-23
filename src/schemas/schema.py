from pydantic import BaseModel


class ChatRequest(BaseModel):
    msg: str


class ChatResponse(BaseModel):
    resposta: str
