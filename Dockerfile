FROM python:3.9.6-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

ENV DATABASE_URL="postgresql://dev_username:dev_password@db/analitics"