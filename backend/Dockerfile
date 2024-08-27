FROM python:3.12-alpine
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8080 --workers ${GUNICORN_WORKERS} --threads 2 --timeout ${GUNICORN_TIMEOUT} backend.wsgi"]
