# Дизайн-документация проекта и Развертывание

## Обзор
Проект представляет собой веб-сервис на FastAPI для обработки платежных уведомлений и интеграции с Telegram ботом. Сервис принимает webhook-уведомления о платежах и отправляет информацию в Telegram чат.

## Развертывание
1. Установка зависимостей: `pip install -r requirements.txt`
2. Настройка переменных окружения в `.env`
3. Запуск сервера: `python fastapi_project.py`
4. Сервер запускается на `http://0.0.0.0:8000`

## Архитектура

### Компоненты системы
1. **FastAPI Backend**
   - Основной веб-сервер
   - Обработка webhook-запросов
   - Валидация входящих данных
   - Интеграция с Telegram API

2. **Telegram Bot**
   - Отправка уведомлений о платежах
   - Эхо-бот функциональность
   - Webhook для приема сообщений

### Модели данных

#### PaymentEvent
```python
class PaymentEvent:
    eventType: str        # Тип события платежа
    product: Product      # Информация о продукте
    buyer: Buyer         # Информация о покупателе
    contractId: str      # ID контракта
    amount: float        # Сумма платежа
    currency: str        # Валюта
    timestamp: str       # Временная метка
    status: str         # Статус платежа
    errorMessage: str   # Сообщение об ошибке
    chat_id: str       # ID чата Telegram (опционально)
```

#### Product
```python
class Product:
    id: str            # ID продукта
    title: str         # Название продукта
```

#### Buyer
```python
class Buyer:
    email: str         # Email покупателя
```

## API Endpoints

### 1. POST /webhook/payment
- **Назначение**: Прием уведомлений о платежах
- **Входные данные**: PaymentEvent
- **Действия**:
  - Валидация входящих данных
  - Форматирование сообщения для Telegram
  - Отправка уведомления в Telegram
- **Ответ**: JSON с статусом операции

### 2. POST /telegram/webhook
- **Назначение**: Прием сообщений от Telegram
- **Входные данные**: Telegram Update объект
- **Действия**:
  - Обработка входящих сообщений
  - Отправка эхо-ответа
- **Ответ**: JSON с подтверждением

## Безопасность
1. Использование переменных окружения для хранения секретов
2. Валидация входящих данных через Pydantic
3. Обработка ошибок и исключений

## Конфигурация
- Настройки хранятся в `.env` файле:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

## Зависимости
- FastAPI
- Uvicorn
- HTTPX
- Python-dotenv
- Pydantic

## Масштабирование
- Асинхронная обработка запросов
- Возможность горизонтального масштабирования
- Независимость от состояния

1.fastapi - для вашего FastAPI приложения
2.uvicorn - ASGI сервер для запуска FastAPI
3.httpx - для асинхронных HTTP запросов (используется для отправки сообщений в Telegram)
4.python-dotenv - для работы с .env файлами
5.pydantic - для валидации данных (используется в FastAPI)

