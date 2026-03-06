FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml README.md .
RUN pip install --no-cache-dir .

COPY src/ ./src/

ENV OLLAMA_API_KEY=""
ENV OLLAMA_HOST="https://ollama.com"

CMD ["ollama-websearch-mcp"]
