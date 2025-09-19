#!/bin/bash

echo "=== Тестирование SHAI Bot API ==="

# Проверяем доступность основного endpoint
echo "1. Проверка health check endpoint..."
curl -s http://localhost:8000/ | jq '.' || echo "Health check failed"

echo -e "\n2. Тестирование API /api/messages..."
curl -X POST http://localhost:8000/api/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "Привет, как дела?"}' \
  | jq '.' || echo "API test failed"

echo -e "\n3. Проверка документации API..."
curl -s http://localhost:8000/docs | head -20

echo -e "\n=== Тест завершен ==="