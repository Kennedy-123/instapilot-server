import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

def notify_telegram_user(telegram_id):
    msg = "✅ You’re now connected to Instagram!"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": telegram_id,
        "text": msg
    }
    requests.post(url, data=payload)


