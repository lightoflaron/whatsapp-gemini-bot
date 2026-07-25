import logging
from pathlib import Path

from instagrapi import Client
from instagrapi.exceptions import LoginRequired

logger = logging.getLogger(__name__)

SESSION_FILE = Path("session.json")


class InstagramPoster:
    def __init__(self, username: str, password: str, sessionid: str = None):
        self.username = username
        self.password = password
        self.sessionid = sessionid
        self.client = Client()
        self._login()

    def _login(self):
        # Prioritas 1: pakai session ID dari browser (paling aman)
        if self.sessionid:
            try:
                self.client.login_by_sessionid(self.sessionid)
                logger.info("Login berhasil menggunakan Session ID")
                self.client.dump_settings(SESSION_FILE)
                return
            except Exception as e:
                logger.warning(f"Session ID gagal ({e}), coba cara lain...")

        # Prioritas 2: pakai session tersimpan
        if SESSION_FILE.exists():
            try:
                self.client.load_settings(SESSION_FILE)
                self.client.login(self.username, self.password)
                logger.info("Login berhasil menggunakan session tersimpan")
                return
            except Exception as e:
                logger.warning(f"Session tersimpan tidak valid ({e}), login ulang...")

        # Prioritas 3: login biasa username + password
        self.client.login(self.username, self.password)
        self.client.dump_settings(SESSION_FILE)
        logger.info("Login berhasil dengan username/password")

    def post_photo(self, image_path: str, caption: str):
        try:
            media = self.client.photo_upload(image_path, caption)
            logger.info(f"Foto berhasil diposting! Media ID: {media.id}")
            return media
        except LoginRequired:
            logger.warning("Session expired, login ulang...")
            self._login()
            media = self.client.photo_upload(image_path, caption)
            logger.info(f"Foto berhasil diposting! Media ID: {media.id}")
            return media

    def post_reel(self, video_path: str, caption: str, thumbnail_path: str = None):
        try:
            media = self.client.clip_upload(video_path, caption, thumbnail=thumbnail_path)
            logger.info(f"Reel berhasil diposting! Media ID: {media.id}")
            return media
        except LoginRequired:
            logger.warning("Session expired, login ulang...")
            self._login()
            media = self.client.clip_upload(video_path, caption, thumbnail=thumbnail_path)
            logger.info(f"Reel berhasil diposting! Media ID: {media.id}")
            return media
