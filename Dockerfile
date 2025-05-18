FROM python:3.11-slim

WORKDIR /app

# Install required packages
RUN pip install --no-cache-dir fastapi uvicorn

# Copy project into the image
COPY . /app

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "smart_host.interface.api:app", "--host", "0.0.0.0", "--port", "8000"]
