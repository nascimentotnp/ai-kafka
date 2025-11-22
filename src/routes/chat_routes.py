from flask import Blueprint, request, jsonify
from typing import Any

from src.services.bot_service import bot

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat() -> Any:
    body = request.get_json(silent=True) or {}
    prompt = body.get("msg", "")

    if not prompt:
        return jsonify({"erro": "Campo 'msg' é obrigatório."}), 400

    reply = bot(prompt)
    return reply