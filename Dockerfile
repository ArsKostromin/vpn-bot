FROM python:3.11-slim

WORKDIR /app

# Устанавливаем сертификаты и curl для отладки (можно убрать позже)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем переменную окружения, указывающую путь к сертификатам
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

CMD ["python", "main.py"]
