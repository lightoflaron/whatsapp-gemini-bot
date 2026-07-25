import os
import urllib.parse
import logging
from pathlib import Path

import requests
import google.generativeai as genai

logger = logging.getLogger(__name__)


class ContentGenerator:
    def __init__(self, api_key: str, niche: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.niche = niche
        self.image_dir = Path("generated_images")
        self.image_dir.mkdir(exist_ok=True)

    def _generate_text(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_image_prompt(self) -> str:
        prompt = f"""Buat satu prompt bahasa Inggris untuk menghasilkan gambar Instagram tentang "{self.niche}".

Syarat:
- Bahasa Inggris
- Deskriptif dan visual
- Gaya: aesthetic, cinematic, high quality photography
- Maksimal 1 kalimat pendek

Balas dengan prompt saja, tanpa penjelasan tambahan."""
        return self._generate_text(prompt)

    def generate_caption(self) -> str:
        prompt = f"""Buat caption Instagram dalam bahasa Indonesia tentang "{self.niche}".

Syarat:
- 3-5 kalimat, inspiratif dan engaging
- Gunakan emoji yang sesuai
- Tambahkan 10-15 hashtag relevan di baris bawah

Balas dengan caption + hashtag saja, tanpa penjelasan tambahan."""
        return self._generate_text(prompt)

    def generate_image(self, image_prompt: str) -> str:
        seed = int.from_bytes(os.urandom(4), "big")
        encoded = urllib.parse.quote(image_prompt)
        url = (
            f"https://image.pollinations.ai/prompt/{encoded}"
            f"?width=1080&height=1080&nologo=true&seed={seed}"
        )

        logger.info(f"Generating image for prompt: {image_prompt[:60]}...")
        response = requests.get(url, timeout=90)
        response.raise_for_status()

        image_path = self.image_dir / f"post_{seed}.jpg"
        with open(image_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Image saved to {image_path}")
        return str(image_path)

    def generate(self) -> dict:
        logger.info(f"Generating content for niche: {self.niche}")
        image_prompt = self.generate_image_prompt()
        image_path = self.generate_image(image_prompt)
        caption = self.generate_caption()

        return {
            "image_path": image_path,
            "caption": caption,
            "image_prompt": image_prompt,
        }
