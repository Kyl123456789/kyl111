# Dockerfile for running the placeholder on CPU
# Build: docker build -t so101-placeholder:latest .
# Run: docker run --rm -it so101-placeholder:latest

FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "run_so101.py", "--input", "examples_input.txt", "--output", "out.jsonl"]
