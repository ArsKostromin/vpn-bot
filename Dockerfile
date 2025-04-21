FROM python:3.11

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# всё, код копировать не надо — он монтируется
