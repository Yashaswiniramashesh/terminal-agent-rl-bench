FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pytest==9.1.1
COPY parse_logs.py .
COPY server.log .