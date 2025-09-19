# 🔐 Настройка секретов и переменных окружения

## Обязательные переменные

### 1. TELEGRAM_BOT_TOKEN
✅ **Уже настроен**: `7985665379:AAEWP3o4B__temsZPWNf5mo_1b7DRCCJCLM`

**Как получить:**
1. Напишите @BotFather в Telegram
2. Выполните команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

### 2. SHAI_API_KEY
❌ **Требует настройки**

**Как получить:**
1. Зарегистрируйтесь на https://shai.pro
2. Перейдите в раздел API
3. Создайте новый API ключ
4. Скопируйте ключ и вставьте в переменную

**Текущий URL**: `https://api.shai.pro/v1/chat/completions`

### 3. CURATOR_CHAT_IDS
❌ **Требует настройки**

**Как получить ID чата:**
1. Добавьте бота @userinfobot в чат с куратором
2. Отправьте команду `/start`
3. Скопируйте Chat ID
4. Для нескольких кураторов разделите запятой: `123456789,987654321`

## Настройка для разных платформ

### Локальная разработка
Отредактируйте файл `.env`:
```env
TELEGRAM_BOT_TOKEN=7985665379:AAEWP3o4B__temsZPWNf5mo_1b7DRCCJCLM
SHAI_API_KEY=ваш_ключ_shai_pro
CURATOR_CHAT_IDS=ваши_chat_id
```

### Amvera
В панели управления проектом добавьте переменные:
- `TELEGRAM_BOT_TOKEN` = `7985665379:AAEWP3o4B__temsZPWNf5mo_1b7DRCCJCLM`
- `SHAI_API_KEY` = `ваш_ключ_shai_pro`
- `CURATOR_CHAT_IDS` = `ваши_chat_id`
- `SHAI_API_URL` = `https://api.shai.pro/v1/chat/completions`

### Docker
```bash
docker run --env-file .env -p 8000:8000 shai-bot
```

### Docker Compose
Переменные берутся из `.env` файла автоматически.

## Проверка настройки

### 1. Проверьте Telegram бота
```bash
curl "https://api.telegram.org/bot7985665379:AAEWP3o4B__temsZPWNf5mo_1b7DRCCJCLM/getMe"
```

### 2. Запустите приложение
```bash
docker-compose up -d
curl http://localhost:8000/
```

### 3. Отправьте тестовое сообщение боту
Найдите бота в Telegram и отправьте `/start`

## Безопасность

⚠️ **ВАЖНО:**
- Никогда не коммитьте файл `.env` в Git
- Используйте разные токены для разработки и продакшн
- Регулярно обновляйте API ключи
- Ограничьте доступ к переменным окружения

## Статус настройки

- ✅ TELEGRAM_BOT_TOKEN - настроен
- ❌ SHAI_API_KEY - требует настройки
- ❌ CURATOR_CHAT_IDS - требует настройки
- ✅ SHAI_API_URL - настроен
- ✅ DATABASE_URL - настроен