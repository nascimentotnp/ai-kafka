import os
from types import SimpleNamespace

# Garante env fake para não explodir no import de config
os.environ.setdefault("GROQ_API_KEY", "fake-key-for-tests")
os.environ.setdefault("GROQ_MODEL", "llama-3.3-70b-versatile")

import src.services.bot_service as bs


def test_bot_calls_select_persona_and_call_llm(monkeypatch):
    captured = {}

    def fake_select_persona(message: str) -> str:
        captured["select_message"] = message
        return "positivo"

    def fake_call_llm(messages):
        captured["messages"] = messages
        return "RESPOSTA_FAKE"

    monkeypatch.setattr(bs, "select_persona", fake_select_persona)
    monkeypatch.setattr(bs, "call_llm", fake_call_llm)

    user_prompt = "O que é o bot?"
    result = bs.bot(user_prompt)

    assert result == "RESPOSTA_FAKE"

    assert captured["select_message"] == user_prompt

    msgs = captured["messages"]
    assert len(msgs) == 2

    assert msgs[0]["role"] == "system"
    assert "CONTEXTO DO ECOMART" in msgs[0]["content"] or "Contexto" in msgs[0]["content"]
    assert "EcoMart" in msgs[0]["content"]

    assert msgs[1]["role"] == "user"
    assert msgs[1]["content"] == user_prompt


def test_bot_retries_on_error(monkeypatch):
    calls = {"count": 0}

    def fake_select_persona(message: str) -> str:
        return "neutro"

    def fake_call_llm(messages):
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("Falha temporária na LLM")
        return "RESPOSTA_APOS_RETRY"

    monkeypatch.setattr(bs, "select_persona", fake_select_persona)
    monkeypatch.setattr(bs, "call_llm", fake_call_llm)
    monkeypatch.setattr(bs, "sleep", lambda *_args, **_kwargs: None)

    result = bs.bot("Teste de retry")

    assert result == "RESPOSTA_APOS_RETRY"
    assert calls["count"] == 2
