"""
Jalankan file ini SEKALI untuk setup login Instagram.
Setelah berhasil, session disimpan dan bot tidak perlu login ulang.
"""
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, BadPassword
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

if not username or not password:
    print("ERROR: Isi dulu INSTAGRAM_USERNAME dan INSTAGRAM_PASSWORD di file .env")
    exit(1)

cl = Client()


def challenge_code_handler(username, choice):
    print(f"\nInstagram mengirim kode verifikasi ke: {choice}")
    code = input("Masukkan kode yang kamu terima: ").strip()
    return code


cl.challenge_code_handler = challenge_code_handler

print(f"Mencoba login sebagai @{username}...")

try:
    cl.login(username, password)
    cl.dump_settings("session.json")
    print("\n✅ Login berhasil! Session tersimpan di session.json")
    print("Sekarang kamu bisa jalankan: python run_now.py")

except BadPassword as e:
    print(f"\n❌ Password salah atau akun diblokir: {e}")
    print("Pastikan username dan password di .env sudah benar.")

except ChallengeRequired as e:
    print(f"\n⚠️  Instagram minta verifikasi tambahan: {e}")
    print("Coba buka Instagram di HP dulu, setujui login, lalu jalankan ulang script ini.")

except Exception as e:
    print(f"\n❌ Error: {e}")
