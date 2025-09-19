# Развертывание на Amvera

## Подготовка проекта для Amvera

### 1. Создание конфигурационного файла

Amvera использует файл `amvera.yml` для конфигурации:

```yaml
meta:
  environment: python
  toolchain: docker

build:
  dockerfile: Dockerfile

run:
  containerPort: 8000
  healthcheckPath: /

env:
  TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
  SHAI_API_URL: ${SHAI_API_URL}
  SHAI_API_KEY: ${SHAI_API_KEY}
  DATABASE_URL: sqlite+aiosqlite:///./shai.db
  CURATOR_CHAT_IDS: ${CURATOR_CHAT_IDS}
```

### 2. Пошаговое развертывание

#### Шаг 1: Подготовка репозитория
```bash
# Убедитесь, что все файлы закоммичены
git add .
git commit -m "Add Docker and Amvera configuration"
git push origin main
```

#### Шаг 2: Создание проекта на Amvera
1. Зайдите на https://amvera.ru
2. Создайте новый проект
3. Подключите ваш Git репозиторий
4. Выберите ветку `main`

#### Шаг 3: Настройка переменных окружения
В панели Amvera добавьте переменные:
- `TELEGRAM_BOT_TOKEN` - токен вашего бота от @BotFather
- `SHAI_API_URL` - URL API SHAI.pro
- `SHAI_API_KEY` - ключ для SHAI.pro API
- `CURATOR_CHAT_IDS` - ID чатов кураторов (через запятую)

#### Шаг 4: Деплой
Amvera автоматически соберет и запустит приложение после коммита.

### 3. Особенности для Amvera

#### Dockerfile оптимизация
Убедитесь, что Dockerfile использует многоэтапную сборку для уменьшения размера:

```dockerfile
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Health check
Добавьте простой health check endpoint (уже есть в `main.py`):
```python
@app.get("/")
async def root():
    return {"status": "running"}
```

### 4. Проверка развертывания

После успешного деплоя:
```bash
# Проверьте статус приложения
curl https://your-app-name.amvera.ru/

# Проверьте API
curl -X POST https://your-app-name.amvera.ru/api/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "тест"}'
```

### 5. Мониторинг и логи

- Логи доступны в панели Amvera
- Используйте встроенный мониторинг ресурсов
- Настройте уведомления о сбоях

### 6. Возможные проблемы

1. **Превышение лимитов ресурсов** - оптимизируйте Docker образ
2. **Проблемы с базой данных** - используйте персистентное хранилище
3. **Таймауты** - настройте правильные timeout'ы в uvicorn

### 7. Рекомендации для продакшн

- Используйте PostgreSQL вместо SQLite для лучшей производительности
- Настройте логирование в внешний сервис
- Добавьте мониторинг состояния бота
- Настройте автоматические бэкапы данных