# SHAI - Система Психо-Эмоциональной Поддержки Студентов 🎓

## Описание проекта

Этот проект представляет собой интеллектуального чат-бота, разработанного для мониторинга и поддержки психо-эмоционального состояния студентов. Бот использует Telegram как интерфейс взаимодействия с пользователями и интегрируется с SHAI.pro для анализа сообщений и оценки рисков.

### Основные функции

- 🤝 Поддерживающий диалог со студентами
- 🔍 Мониторинг психо-эмоционального состояния
- ⚠️ Автоматическое определение рисков
- 📢 Система эскалации для критических ситуаций
- 👥 Прозрачное взаимодействие с кураторами

## Технический стек

- Python 3.8+
- FastAPI (веб-фреймворк)
- SQLAlchemy + SQLite (база данных)
- python-telegram-bot (Telegram API)
- SHAI.pro API (анализ эмоций)
- Pydantic (валидация данных)
- Alembic (миграции БД)
- Loguru (логирование)

## Установка и настройка

### Предварительные требования

- Docker и Docker Compose
- Telegram Bot Token (от @BotFather)
- SHAI.pro API доступ

### Быстрый старт с Docker

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Taglat/TomorrowOrNeverShaiPro.git
cd TomorrowOrNeverShaiPro
```

2. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл с реальными токенами
```

3. Запустите с Docker Compose:
```bash
docker-compose up -d
```

4. Проверьте работу:
```bash
curl http://localhost:8000/
./test_api.sh
```

### Ручная установка (без Docker)

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл конфигурации:
```bash
cp .env.example .env
```

4. Настройте переменные окружения в файле `.env`:
```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# SHAI.pro Configuration
SHAI_API_URL=your_shai_api_url_here
SHAI_API_KEY=your_shai_api_key_here

# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./shai.db

# Escalation Configuration
CURATOR_CHAT_IDS=123456789,987654321  # ID чатов кураторов через запятую
```

### Запуск

Запустите сервер с помощью команды:
```bash
python main.py
```

Сервер запустится на `http://localhost:8000`

## Структура проекта

```
SHAI/
├── app/
│   ├── core/
│   │   ├── api_schemas.py     # API модели данных
│   │   ├── config.py         # Конфигурация приложения
│   │   ├── database.py       # Настройки базы данных
│   │   ├── models.py         # SQLAlchemy модели
│   │   └── schemas.py        # Базовые схемы данных
│   └── services/
│       ├── database_service.py    # Сервис работы с БД
│       ├── escalation_service.py  # Сервис эскалации
│       ├── shai_service.py        # Интеграция с SHAI.pro
│       └── telegram_bot.py        # Telegram бот
├── main.py                   # FastAPI приложение
├── requirements.txt          # Зависимости
├── .env.example             # Пример переменных окружения
├── .gitignore              # Git игнорируемые файлы
├── LICENSE                 # MIT лицензия
└── README.md               # Документация
```

## API Endpoints

### GET /api/analyze/{message_id}
Получение анализа конкретного сообщения:
```json
{
    "emotion": ["joy", "gratitude"],
    "risk_level": "NO_RISK",
    "escalation_required": false,
    "response_to_user": "..."
}
```

### POST /api/messages
Отправка сообщения на анализ:
```json
{
    "message": "Текст сообщения"
}
```

## Функциональность

### Telegram Bot

- `/start` - Начало работы с ботом
- Обработка текстовых сообщений
- Автоматические ответы с поддержкой
- Уведомления кураторов в случае критических ситуаций

### Система оценки рисков

Бот анализирует каждое сообщение через SHAI.pro API и оценивает:
- Эмоциональное состояние (на основе GoEmotions)
- Уровень риска (NO_RISK, LOW_RISK, MODERATE_RISK, HIGH_RISK)
- Необходимость эскалации
- Сохранение результатов в базе данных

### Система эскалации

При обнаружении критических ситуаций (MODERATE_RISK или HIGH_RISK + escalation_required):
1. Автоматическое уведомление кураторов через Telegram
2. Предоставление полного контекста:
   - Временная метка
   - ID сообщения
   - ID пользователя
   - Уровень риска
   - Обнаруженные эмоции
   - Текст сообщения
3. Сохранение данных в БД для анализа
4. Прозрачное информирование о процессе

### База данных

- Хранение всех сообщений и их анализа
- Связанные таблицы для сообщений и результатов анализа
- Асинхронное взаимодействие через SQLAlchemy
- Поддержка миграций через Alembic
