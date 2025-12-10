# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# system deps for Ollama are not provided here — Ollama runs on host; inside docker you must ensure ollama is available.
# If you plan to run Ollama inside container, additional setup is required (not covered here).
COPY backend /app/backend
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.api.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
