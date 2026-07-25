import logging
import schedule
import time

from config import Config
from generator import ContentGenerator
from instagram import InstagramPoster

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
    try:
        config = Config()
        generator = ContentGenerator(config.gemini_api_key, config.niche)
        poster = InstagramPoster(config.ig_username, config.ig_password)

        content = generator.generate()
        logger.info(f"Caption: {content['caption'][:80]}...")

        poster.post_photo(content["image_path"], content["caption"])
        logger.info("=== Postingan berhasil! ===")

    except Exception as e:
        logger.error(f"Gagal posting: {e}", exc_info=True)


def main():
    config = Config()
    post_time = config.post_time

    schedule.every().day.at(post_time).do(post_daily)
    logger.info(f"Scheduler aktif — posting otomatis setiap hari pukul {post_time}")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
