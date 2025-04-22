FROM python:3.11

WORKDIR /app

# Копируем всё содержимое vpn-bot внутрь контейнера
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
