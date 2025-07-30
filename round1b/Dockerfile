FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY input/ ./input
COPY output/ ./output

CMD ["python3", "src/rag_pipeline.py"]
