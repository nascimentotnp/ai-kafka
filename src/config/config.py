import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
TEMPERATURE = float(os.getenv("TEMPERATURE"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS"))

if not API_KEY:
    raise RuntimeError(
        "A variável de ambiente GROQ_API_KEY não está definida. "
        "Configure no .env ou no ambiente antes de iniciar a aplicação."
    )

llm_client = Groq(api_key=API_KEY)
