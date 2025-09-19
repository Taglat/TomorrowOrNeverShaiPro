#!/bin/bash

echo "=== Подготовка к деплою на Amvera ==="

# Проверяем наличие необходимых файлов
if [ ! -f "amvera.yml" ]; then
    echo "❌ Файл amvera.yml не найден!"
    exit 1
fi

if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile не найден!"
    exit 1
fi

echo "✅ Конфигурационные файлы найдены"

# Проверяем .env файл
if [ ! -f ".env" ]; then
    echo "⚠️ Файл .env не найден. Создается из примера..."
    cp .env.example .env
    echo "📝 Отредактируйте .env файл с реальными токенами перед деплоем!"
fi

# Проверяем Git репозиторий
if [ ! -d ".git" ]; then
    echo "❌ Git репозиторий не инициализирован!"
    echo "Выполните: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

# Проверяем, есть ли незакоммиченные изменения
if ! git diff --quiet; then
    echo "⚠️ Есть незакоммиченные изменения. Коммитим..."
    git add .
    git commit -m "Update for Amvera deployment $(date)"
fi

echo "✅ Проект готов к деплою на Amvera!"
echo ""
echo "Следующие шаги:"
echo "1. Загрузите код в Git репозиторий (GitHub/GitLab)"
echo "2. Зайдите на https://amvera.ru"
echo "3. Создайте новый проект и подключите репозиторий"
echo "4. Настройте переменные окружения:"
echo "   - TELEGRAM_BOT_TOKEN"
echo "   - SHAI_API_URL" 
echo "   - SHAI_API_KEY"
echo "   - CURATOR_CHAT_IDS"
echo "5. Запустите деплой"
echo ""
echo "📚 Подробная инструкция в файле AMVERA_DEPLOYMENT.md"