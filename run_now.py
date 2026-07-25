"""Jalankan file ini untuk test posting langsung tanpa menunggu jadwal."""
import logging
from main import post_daily

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

if __name__ == "__main__":
    post_daily()
