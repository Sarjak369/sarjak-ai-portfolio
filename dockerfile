# ===== App image =====
FROM python:3.11-slim

# System deps for pip/Chromadb/PyTorch-lite wheels etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# Prevent HF tokenizers fork warning noise in containers
ENV TOKENIZERS_PARALLELISM=false \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    GRADIO_SERVER_NAME=0.0.0.0

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy source
COPY . .

# Default envs (override in platform)
ENV LLM_PROVIDER=ollama \
    OLLAMA_BASE_URL=http://ollama:11434 \
    CHUNK_SIZE=850 \
    CHUNK_OVERLAP=150 \
    RAG_TOP_K=8

# Expose Gradio
EXPOSE 7860

# Start the app
CMD ["python", "app.py"]
