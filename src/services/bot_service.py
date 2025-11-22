from time import sleep
from typing import List, Dict

from src.config.config import llm_client, MODEL
from src.helpers import load
from src.select_persona import select_persona, personas

CONTEXT_FILE = "dados/ecomart.txt"
context = load(CONTEXT_FILE) or ""


def setup_prompt(personality: str) -> str:
    return f"""
Você é um assistente virtual do EcoMart, um e-commerce especializado em produtos sustentáveis.

Siga estritamente as regras abaixo:

1. Use SOMENTE o contexto fornecido.  
   Não invente informações ou produtos que não estejam no contexto.

2. Adote a persona indicada:
   {personality}

3. Responda sempre em **português do Brasil**.

4. Quando o usuário fizer perguntas gerais como:
   - "O que é o EcoMart?"
   - "Como funciona o EcoMart?"
   - "Qual é a proposta do EcoMart?"
   você deve:
   - explicar o que é o EcoMart,
   - falar da missão e dos valores de sustentabilidade,
   - mencionar que há várias categorias de produtos (como Moda Sustentável, Eletrônicos Verdes, Alimentação Sustentável etc.),
   - destacar o compromisso com embalagens recicláveis, responsabilidade social e apoio a causas ambientais.

5. Formato da resposta:
   - use pelo menos **2 parágrafos curtos**;
   - se fizer sentido, use uma lista com 3–5 pontos destacando benefícios ou diferenciais;
   - evite respostas muito curtas (não responda em uma única frase);
   - mantenha um tom humano e acolhedor.

6. Se o usuário perguntar algo fora do contexto do EcoMart:
   - explique educadamente que você só pode responder sobre produtos, políticas e informações presentes no contexto.

---

### CONTEXTO DO ECOMART
{context}
"""


def call_llm(messages: List[Dict[str, str]]) -> str:
    reply = llm_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        max_tokens=500
    )

    return reply.choices[0].message.content


def bot(prompt_user: str) -> str:
    feeling = select_persona(prompt_user)
    personality = personas.get(feeling, personas["neutro"])

    retry = 0
    max_retry = 2

    while retry < max_retry:
        try:
            prompt_system = setup_prompt(personality)

            messages = [
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},
            ]

            return call_llm(messages)

        except Exception as e:
            retry += 1
            print(f"[bot] erro: {e}")
            sleep(1)

    return "Erro ao processar sua solicitação."
