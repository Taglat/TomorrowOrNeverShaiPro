#!/bin/bash

echo "🔐 Настройка секретов для SHAI Bot"
echo "=================================="

# Проверяем текущую конфигурацию
if [ -f ".env" ]; then
    echo "✅ Файл .env найден"
    
    # Проверяем Telegram токен
    if grep -q "7985665379:AAEWP3o4B__temsZPWNf5mo_1b7DRCCJCLM" .env; then
        echo "✅ Telegram bot token настроен"
        
        # Проверяем валидность токена
        echo "🔍 Проверяка токена через Telegram API..."
        RESPONSE=$(curl -s "https://api.telegram.org/bot7985665379:AAEWP3o4B__temsZPWNf5mo_1b7DRCCJCLM/getMe")
        if echo "$RESPONSE" | grep -q '"ok":true'; then
            BOT_NAME=$(echo "$RESPONSE" | grep -o '"first_name":"[^"]*"' | cut -d'"' -f4)
            BOT_USERNAME=$(echo "$RESPONSE" | grep -o '"username":"[^"]*"' | cut -d'"' -f4)
            echo "✅ Бот валиден: $BOT_NAME (@$BOT_USERNAME)"
        else
            echo "❌ Токен бота недействителен"
        fi
    else
        echo "❌ Telegram bot token не настроен"
    fi
    
    # Проверяем SHAI API
    if grep -q "your_shai_api_key_here" .env; then
        echo "❌ SHAI API key требует настройки"
        echo "   Получите ключ на https://shai.pro"
    else
        echo "✅ SHAI API key настроен"
    fi
    
    # Проверяем кураторов
    if grep -q "123456789,987654321" .env; then
        echo "❌ CURATOR_CHAT_IDS требует настройки"
        echo "   Получите Chat ID через @userinfobot"
    else
        echo "✅ CURATOR_CHAT_IDS настроены"
    fi
    
else
    echo "❌ Файл .env не найден. Создаем из примера..."
    cp .env.example .env
    echo "📝 Отредактируйте .env файл с реальными значениями"
fi

echo ""
echo "📋 Следующие шаги:"
echo "1. Получите SHAI API ключ на https://shai.pro"
echo "2. Получите Chat ID кураторов через @userinfobot"
echo "3. Обновите .env файл с реальными значениями"
echo "4. Запустите: docker compose up -d"
echo "5. Протестируйте: ./test_api.sh"
echo ""
echo "📚 Подробная инструкция в SECRETS_SETUP.md"