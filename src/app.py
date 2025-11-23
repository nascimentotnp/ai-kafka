import os
from fastapi import FastAPI
from dotenv import load_dotenv

from src.routes.chat_routes import chat_router
from src.routes.health_route import health_router

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Assistant API",
        version="1.0.0",
        description="API de atendimento da Taha Inc. usando LLaMA via Groq.",
    )

    app.include_router(health_router)
    app.include_router(chat_router)

    return app
