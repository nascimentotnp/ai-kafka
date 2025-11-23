import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def send_message(message: str) -> str:
    """Chama a API FastAPI /chat e retorna o texto da resposta."""
    resp = requests.post(f"{API_URL}/chat", json={"msg": message}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # espera um JSON: { "resposta": "..." }
    return data.get("resposta", "Não foi possível obter resposta.")


def main() -> None:
    st.set_page_config(page_title="Taha Assistant", page_icon="🤖")

    st.title("🤖 Taha Assistant")
    # st.caption(f"Consumindo API em: {API_URL}")

    # inicializa histórico
    if "history" not in st.session_state:
        st.session_state.history = []  # [{"role": "user"|"assistant", "content": str}]

    # mostra histórico
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # input do usuário
    user_input = st.chat_input("Digite sua mensagem...")

    if user_input:
        # adiciona mensagem do usuário ao histórico
        st.session_state.history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        # chama API
        try:
            reply = send_message(user_input)
        except Exception as e:
            reply = f"⚠️ Erro ao chamar a API: `{e}`"

        # adiciona resposta ao histórico
        st.session_state.history.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)


if __name__ == "__main__":
    main()
