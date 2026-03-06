FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir .

ENV OLLAMA_API_KEY=""
ENV OLLAMA_HOST="https://ollama.com"

CMD ["ollama-websearch-mcp"]
