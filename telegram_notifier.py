import logging
from datetime import datetime
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def _api_url(self, method: str) -> str:
        return TELEGRAM_API.format(token=self.token, method=method)

    def send_message(self, text: str) -> bool:
        try:
            resp = requests.post(
                self._api_url("sendMessage"),
                json={"chat_id": self.chat_id, "text": text, "parse_mode": "HTML"},
                timeout=15,
            )
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Gagal kirim pesan Telegram: {e}")
            return False

    def send_photo(self, image_path: str, caption: str) -> bool:
        try:
            with open(image_path, "rb") as photo:
                resp = requests.post(
                    self._api_url("sendPhoto"),
                    data={"chat_id": self.chat_id, "caption": caption, "parse_mode": "HTML"},
                    files={"photo": photo},
                    timeout=30,
                )
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Gagal kirim foto Telegram: {e}")
            return False

    def notify_success(self, image_path: str, caption: str, niche: str):
        waktu = datetime.now().strftime("%d/%m/%Y %H:%M")
        preview = caption[:200] + "..." if len(caption) > 200 else caption

        tg_caption = (
            f"✅ <b>Posting Instagram Berhasil!</b>\n\n"
            f"🕘 <b>Waktu:</b> {waktu}\n"
            f"🎯 <b>Niche:</b> {niche}\n\n"
            f"📝 <b>Caption:</b>\n{preview}"
        )

        # Kirim foto + caption sekaligus
        if not self.send_photo(image_path, tg_caption):
            # Fallback: kirim teks saja jika foto gagal
            self.send_message(tg_caption)

    def notify_error(self, error: str):
        waktu = datetime.now().strftime("%d/%m/%Y %H:%M")
        text = (
            f"❌ <b>Posting Instagram Gagal!</b>\n\n"
            f"🕘 <b>Waktu:</b> {waktu}\n"
            f"⚠️ <b>Error:</b>\n<code>{error}</code>"
        )
        self.send_message(text)
