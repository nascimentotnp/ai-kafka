FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exemplo: rodar a assistant_api (depois você troca por FastAPI/uvicorn)
CMD ["python", "-m", "app.assistant_api.main"]
