# 🚀 Быстрый старт для Amvera

## Пошаговая инструкция

### 1. Подготовка
```bash
# Клонируйте репозиторий
git clone https://github.com/Taglat/TomorrowOrNeverShaiPro.git
cd TomorrowOrNeverShaiPro

# Проверьте готовность к деплою
./deploy_amvera.sh
```

### 2. Настройка на Amvera
1. Зайдите на [amvera.ru](https://amvera.ru)
2. Создайте новый проект
3. Подключите ваш Git репозиторий
4. Выберите ветку `main`

### 3. Переменные окружения
Добавьте в панели Amvera:
- `TELEGRAM_BOT_TOKEN` - от @BotFather
- `SHAI_API_URL` - URL API SHAI.pro  
- `SHAI_API_KEY` - ключ API SHAI.pro
- `CURATOR_CHAT_IDS` - ID чатов кураторов

### 4. Автоматический деплой
Amvera автоматически:
- Обнаружит `amvera.yml`
- Соберет Docker образ
- Запустит приложение
- Предоставит HTTPS URL

### 5. Проверка
```bash
curl https://ваш-проект.amvera.ru/
```

## Файлы для Amvera
- ✅ `amvera.yml` - конфигурация платформы
- ✅ `Dockerfile` - сборка контейнера  
- ✅ `requirements.txt` - зависимости Python
- ✅ `.env.example` - шаблон переменных

## Поддержка
📚 Подробная документация: `AMVERA_DEPLOYMENT.md`