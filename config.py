import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.ig_username = os.getenv("INSTAGRAM_USERNAME")
        self.ig_password = os.getenv("INSTAGRAM_PASSWORD")
        self.niche = os.getenv("NICHE", "motivasi harian")
        self.post_time = os.getenv("POST_TIME", "09:00")

        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan di file .env")
        if not self.ig_username or not self.ig_password:
            raise ValueError("INSTAGRAM_USERNAME atau INSTAGRAM_PASSWORD tidak ditemukan di file .env")
