# helpers.py
from asyncio.log import logger
from pathlib import Path
from typing import Optional


def load(file_path: str) -> Optional[str]:
    try:
        path = Path(file_path)
        with path.open("r", encoding="utf-8") as file:
            return file.read()
    except OSError as e:
        logger.error(f"[helpers.carrega] Erro ao carregar arquivo '{file_path}': {e}")
        return None


def save(file_path: str, conteudo: str) -> bool:
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            file.write(conteudo)
        return True
    except OSError as e:
        logger.error(f"[helpers.salva] Erro ao salvar arquivo '{file_path}': {e}")
        return False
