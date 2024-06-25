FROM python:3.12-alpine
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "--timeout", "360", "backend.wsgi"]