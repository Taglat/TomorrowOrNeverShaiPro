# Инструкция по развертыванию SHAI Bot

## Развертывание с Docker

### 1. Подготовка окружения

Убедитесь, что у вас установлены:
- Docker
- Docker Compose (опционально)

### 2. Настройка переменных окружения

Скопируйте файл с примером и заполните реальными значениями:
```bash
cp .env.example .env
```

Отредактируйте `.env` файл:
```env
TELEGRAM_BOT_TOKEN=your_real_bot_token_from_botfather
SHAI_API_URL=https://your-shai-api-endpoint.com
SHAI_API_KEY=your_shai_api_key
CURATOR_CHAT_IDS=123456789,987654321
```

### 3. Сборка и запуск

#### Вариант 1: Docker
```bash
# Сборка образа
docker build -t shai-bot .

# Запуск контейнера
docker run --env-file .env -p 8000:8000 --name shai-bot shai-bot
```

#### Вариант 2: Docker Compose
```bash
# Запуск в фоне
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### 4. Тестирование

#### Проверка health endpoint:
```bash
curl http://localhost:8000/
```

#### Тест API:
```bash
./test_api.sh
```

#### Интерактивная документация API:
Откройте в браузере: http://localhost:8000/docs

## Развертывание на продакшн

### 1. VPS/Облако
- Скопируйте проект на сервер
- Настройте .env с реальными токенами
- Запустите через docker-compose
- Настройте nginx как reverse proxy (опционально)

### 2. Heroku/Railway/Render/Amvera
- Загрузите код в Git репозиторий
- Подключите к платформе
- Настройте переменные окружения через веб-интерфейс
- Платформа автоматически соберет и запустит Docker контейнер

#### Специально для Amvera:
- Используйте файл `amvera.yml` для конфигурации
- См. подробную инструкцию в `AMVERA_DEPLOYMENT.md`
- Убедитесь, что настроены все переменные окружения

### 3. Переменные окружения для продакшн:

```env
# Обязательные
TELEGRAM_BOT_TOKEN=<реальный токен от BotFather>
SHAI_API_URL=<URL API SHAI.pro>
SHAI_API_KEY=<ключ для SHAI.pro>
CURATOR_CHAT_IDS=<ID чатов кураторов через запятую>

# Опциональные
DATABASE_URL=sqlite+aiosqlite:///./shai.db
PORT=8000
```

## Мониторинг

### Проверка статуса:
```bash
# Health check
curl http://your-domain:8000/

# Логи контейнера
docker logs shai-bot

# Статус сервисов
docker-compose ps
```

### Возможные проблемы:
1. **Invalid Telegram token** - проверьте токен от BotFather
2. **SHAI API недоступен** - проверьте URL и ключ API
3. **Порт 8000 занят** - измените порт в docker run или docker-compose.yml