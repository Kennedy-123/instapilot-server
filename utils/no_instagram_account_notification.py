import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

def no_instagram_account_notification(telegram_id):
    msg = "⚠️ No Instagram Business/Creator account connected to your Facebook. Please switch your Instagram to a Business/Creator account and link it to a Facebook Page."
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": telegram_id,
        "text": msg
    }
    requests.post(url, data=payload)
