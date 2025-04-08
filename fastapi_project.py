from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import uvicorn
import json

# Загружаем переменные окружения из .env файла
load_dotenv()

app = FastAPI()

# Получаем данные из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN:
    print("Предупреждение: Не установлена переменная окружения TELEGRAM_BOT_TOKEN")


class Product(BaseModel):
    id: str
    title: str


class Buyer(BaseModel):
    email: str


class PaymentEvent(BaseModel):
    eventType: str
    product: Product
    buyer: Buyer
    contractId: str
    amount: float
    currency: str
    timestamp: str
    status: str
    errorMessage: str
    chat_id: str = None


async def send_telegram_message(chat_id: str, message: str):
    if not TELEGRAM_BOT_TOKEN:
        raise Exception("Не настроена переменная окружения для Telegram")
        
    async with httpx.AsyncClient() as client:
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = await client.post(TELEGRAM_API_URL, json=payload)
        if response.status_code != 200:
            raise Exception(f"Telegram API error: {response.text}")


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/webhook/payment")
async def payment_webhook(payload: PaymentEvent):
    # if payload.eventType != "payment.success":
    #     raise HTTPException(status_code=400, detail="Unsupported event type")

    message = (
        f"*Платёж прошёл успешно!*\n"
        f"💰 Сумма: `{payload.amount} {payload.currency}`\n"
        f"📦 Продукт: {payload.product.title}\n"
        f"📧 Покупатель: {payload.buyer.email}\n"
        f"📄 Договор: `{payload.contractId}`\n"
        f"🕒 Время: `{payload.timestamp}`\n"
        f"✅ Статус: {payload.status}"
    )

    try:
        # Используем chat_id из входящего JSON или используем дефолтный
        chat_id = payload.chat_id or TELEGRAM_CHAT_ID
        await send_telegram_message(chat_id, message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send Telegram message: {e}")

    return {"status": "ok"}


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    
    # Проверяем, что это сообщение
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        message_text = data["message"]["text"]
        user_name = data["message"]["from"].get("first_name", "Пользователь")
        
        # Эхо-бот, который повторяет сообщения пользователя
        try:
            response_message = f"Эхо: {message_text}"
            await send_telegram_message(str(chat_id), response_message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send Telegram message: {e}")
    
    return {"status": "ok"}


if __name__ == "__main__":
    # Настраиваем вебхук для Telegram бота при запуске
    print(f"Подпишись на канал: https://t.me/RuslanSenatorov")
    uvicorn.run("fastapi_project:app", host="0.0.0.0", port=8000, reload=True)
