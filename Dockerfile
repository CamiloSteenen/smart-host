FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV PYTHONPATH=/app/src
ENV HOST=0.0.0.0
ENV PORT=8000
CMD ["sh", "-c", "uvicorn smart_host.interface.api:app --host ${HOST} --port ${PORT}"]
