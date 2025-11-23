import os

os.environ.setdefault("GROQ_API_KEY", "fake-key-for-tests")
os.environ.setdefault("GROQ_MODEL", "llama-3.3-70b-versatile")

import src.services.bot_service as bs


def test_setup_prompt_inclui_persona_e_contexto(monkeypatch):
    fake_persona = "EU SOU UMA PERSONA FAKE"
    fake_context = "ISTO É UM CONTEXTO FAKE DO ECOMART"

    # monkeypatch no contexto global do módulo
    monkeypatch.setattr(bs, "context", fake_context)

    prompt = bs.setup_prompt(fake_persona)

    # 1) Começa com a instrução base do EcoMart
    assert "assistente virtual do EcoMart" in prompt

    # 2) Persona passada foi incluída
    assert fake_persona in prompt

    # 3) Contexto foi incluído na seção certa
    assert "CONTEXTO DO ECOMART" in prompt
    assert fake_context in prompt

    # 4) Boas práticas mencionadas
    assert "Use SOMENTE o contexto fornecido" in prompt
    assert "Não invente informações" in prompt
