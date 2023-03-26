FROM python:3.9.6-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app /app
COPY wait-for-it.sh .

CMD ["./wait-for-it.sh", "db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "8000"]

ENV PYTHONPATH="/app"
ENV DATABASE_URL="postgresql://dev_username:dev_password@db/analytics"
