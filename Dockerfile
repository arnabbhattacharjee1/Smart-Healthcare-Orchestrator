FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the architecture files
COPY adk/ ./adk/
COPY agents/ ./agents/
COPY web/ ./web/
COPY main.py .
COPY app.py .

# Use Cloud Run's dynamic PORT environment variable (or 8080 by default)
CMD python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}
