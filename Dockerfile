# Dockerfile (Aiogram бот)
FROM python:3.11

WORKDIR /app

# Копируем только requirements.txt сначала
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем остальной код
COPY . .

CMD ["python", "main.py"]
