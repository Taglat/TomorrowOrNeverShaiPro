FROM python:3.11-slim

# Установим рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt ./

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Переменные окружения (можно переопределять через docker run)
ENV PYTHONUNBUFFERED=1

# Открываем порт для FastAPI
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
