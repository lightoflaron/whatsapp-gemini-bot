import atexit
import logging
import signal
import sys
import schedule
import time

from config import Config
from generator import ContentGenerator
from instagram import InstagramPoster
from telegram_notifier import TelegramNotifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def post_daily():
    logger.info("=== Memulai postingan harian Instagram ===")
    config = Config()

    notifier = None
    if config.telegram_token and config.telegram_chat_id:
        notifier = TelegramNotifier(config.telegram_token, config.telegram_chat_id)

    try:
        generator = ContentGenerator(config.gemini_api_key, config.niche)
        poster = InstagramPoster(config.ig_username, config.ig_password, config.ig_sessionid)

        content = generator.generate()
        logger.info(f"Caption: {content['caption'][:80]}...")

        poster.post_photo(content["image_path"], content["caption"])
        logger.info("=== Postingan berhasil! ===")

        if notifier:
            notifier.notify_success(content["image_path"], content["caption"], config.niche)

    except Exception as e:
        logger.error(f"Gagal posting: {e}", exc_info=True)
        if notifier:
            notifier.notify_error(str(e))


def build_notifier(config: Config):
    if config.telegram_token and config.telegram_chat_id:
        return TelegramNotifier(config.telegram_token, config.telegram_chat_id)
    return None


def main():
    config = Config()
    notifier = build_notifier(config)

    # Notifikasi saat bot mati (SIGTERM, SIGINT, atau crash tak terduga)
    def on_shutdown(reason: str):
        logger.info(f"Bot berhenti: {reason}")
        if notifier:
            notifier.notify_stop(reason)

    def handle_signal(signum, frame):
        name = signal.Signals(signum).name
        on_shutdown(f"sinyal {name} diterima")
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    atexit.register(lambda: on_shutdown("proses berakhir"))

    # Notifikasi saat bot start / restart
    if notifier:
        notifier.notify_start(config.post_time, config.niche)

    schedule.every().day.at(config.post_time).do(post_daily)
    logger.info(f"Scheduler aktif — posting otomatis setiap hari pukul {config.post_time}")

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except Exception as e:
        logger.critical(f"Bot crash: {e}", exc_info=True)
        if notifier:
            notifier.notify_crash(str(e))
        raise


if __name__ == "__main__":
    main()
