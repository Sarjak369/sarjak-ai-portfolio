# ---- 1) Base
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TOKENIZERS_PARALLELISM=false

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl && \
    rm -rf /var/lib/apt/lists/*

# ---- 2) App
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy only what we need for runtime
COPY . .

# Gradio expects us to listen on 7860 in Spaces
ENV PORT=7860
EXPOSE 7860

# Important for HF Spaces: bind 0.0.0.0 and use PORT
CMD ["python", "app.py"]
