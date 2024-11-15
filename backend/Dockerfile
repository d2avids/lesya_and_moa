FROM python:3.12-alpine
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8080 --workers ${GUNICORN_WORKERS} --threads 3 --timeout ${GUNICORN_TIMEOUT} --max-requests ${GUNICORN_MAX_REQUESTS} --max-requests-jitter ${GUNICORN_MAX_REQUESTS_JITTER} backend.wsgi"]
