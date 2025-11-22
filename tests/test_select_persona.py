from types import SimpleNamespace

import src.select_persona as sp


class FakeLLMClient:
    def __init__(self, answer: str):
        self._answer = answer

    class _Chat:
        def __init__(self, outer):
            self._outer = outer

        class _Completions:
            def __init__(self, outer):
                self._outer = outer

            def create(self, **kwargs):
                # Monta um objeto com a mesma "cara" da resposta da Groq
                message = SimpleNamespace(content=self._outer._answer)
                choice = SimpleNamespace(message=message)
                return SimpleNamespace(choices=[choice])

        @property
        def completions(self):
            return FakeLLMClient._Chat._Completions(self._outer)

    @property
    def chat(self):
        return FakeLLMClient._Chat(self)


def test_select_persona_positive(monkeypatch):
    fake_client = FakeLLMClient("positivo")
    monkeypatch.setattr(sp, "llm_client", fake_client)

    result = sp.select_persona("Eu amo os produtos do EcoMart, estou muito feliz!")
    assert result == "positivo"


def test_select_persona_negative(monkeypatch):
    fake_client = FakeLLMClient("negativo")
    monkeypatch.setattr(sp, "llm_client", fake_client)

    result = sp.select_persona("Estou insatisfeito com o atraso na entrega.")
    assert result == "negativo"


def test_select_persona_fallback_to_neutral(monkeypatch):
    fake_client = FakeLLMClient("qualquer-coisa")
    monkeypatch.setattr(sp, "llm_client", fake_client)

    result = sp.select_persona("Mensagem qualquer")
    assert result == "neutro"
