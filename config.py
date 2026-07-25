import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.niche = os.getenv("NICHE", "motivasi islami")
        self.post_time = os.getenv("POST_TIME", "09:00")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.telegram_channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan di file .env")
        if not self.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di file .env")
        if not self.telegram_channel_id:
            raise ValueError("TELEGRAM_CHANNEL_ID tidak ditemukan di file .env")
