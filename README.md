# stepik https://stepik.org/a/237390
# Дизайн-документация проекта

## Обзор
Проект представляет собой веб-сервис на FastAPI для обработки платежных уведомлений и интеграции с Telegram ботом. Сервис принимает webhook-уведомления о платежах и отправляет информацию в Telegram чат.

## Конфигурация
- Настройки хранятся в `.env` файле:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

## Развертывание
1. Установка зависимостей: `python -m venv venv` потом `pip install -r requirements.txt`
2. Настройка переменных окружения в `.env`
3. Запуск сервера: `python fastapi_project.py`
4. Сервер запускается на `http://0.0.0.0:8000`

## Команды для UBUNTU
1. Обновляем пакеты
```
sudo apt update
```
2. Устанавливаем NGINX
   
```
sudo apt install nginx
```

3. Создаем файл конфигурации:

```
sudo nano /etc/nginx/sites-available/ВАШ_ДОМЕН.ru
```
4. Наполняем файл конфигурации:
```
server {
    listen 80;
    server_name ВАШ_ДОМЕН.ru www.ВАШ_ДОМЕН.ru;

    location / {
        proxy_pass http://127.0.0.1:8000;  # Порт, на котором работает FastAPI
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

5. символическая ссылка для активации конфигурации:
   
```
sudo ln -s /etc/nginx/sites-available/ВАШ_ДОМЕН.ru /etc/nginx/sites-enabled/
```
6.  Тестируем nginx
```
sudo nginx -t
```
7. Перезапускаем Nginx
```
sudo systemctl restart nginx
```
8. Устанавливаем SSL
```
sudo apt install certbot python3-certbot-nginx
```
9. Настраиваем SSL
```
sudo certbot --nginx -d ВАШ_ДОМЕН.ru -d www.ВАШ_ДОМЕН.ru
```
10. Создаем крон задачу
```
sudo crontab -e
```
11. Конфигурируем крон
```
0 0 * * * certbot renew --quiet && systemctl reload nginx
```
12. Проверяем статус крон
```
sudo systemctl status certbot.timer
```
13. Создаем файл конфигов для демона
```
sudo nano /etc/systemd/system/НАЗВАНИЕ_СЕРВИСА_ЛЮБОЕ.service
```
14. Наполняем файл для демона
```

[Unit]
Description=My Python Script Service

[Service]
Type=simple
WorkingDirectory=/root/ВАША_ПАПКА
ExecStart=/bin/bash -c 'source /root/ВАША_ПАПКА/venv/bin/activate && /root/ВАША_ПАПКА/venv/bin/python /root/ВАША_ПАПКА/название_ФАЙЛА.py'
Environment="PATH=/root/ВАША_ПАПКА/venv/bin:$PATH"
Restart=on-failure
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
15. Перезапускаем службу демона
```
sudo systemctl daemon-reload
```
16. Запускаем службу демона
```
sudo systemctl start НАЗВАНИЕ_СЕРВИСА_СМ_ПУНКТ_13.service
```
17. Проверяем статус службы
```
sudo systemctl status НАЗВАНИЕ_СЕРВИСА_СМ_ПУНКТ_13.service
```

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

1. fastapi - для вашего FastAPI приложения
2. uvicorn - ASGI сервер для запуска FastAPI
3. httpx - для асинхронных HTTP запросов (используется для отправки сообщений в Telegram)
4. python-dotenv - для работы с .env файлами
5. pydantic - для валидации данных (используется в FastAPI)

