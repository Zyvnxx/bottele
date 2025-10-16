import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient

# --- 1️⃣ Load konfigurasi ---
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_GROUPS = [g.strip() for g in os.getenv("TARGET_GROUPS", "").split(",") if g.strip()]
INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES", 2))
DELAY_BETWEEN_GROUPS = int(os.getenv("DELAY_BETWEEN_GROUPS", 5))  # jeda antar grup (detik)

# --- 2️⃣ Debug info ---
print(f"📞 PHONE: {PHONE_NUMBER}")
print(f"API_ID: {API_ID}")
print(f"API_HASH: {API_HASH}")
print(f"📡 SOURCE: {SOURCE_CHANNEL}")
print(f"🎯 TARGETS: {TARGET_GROUPS}")
print(f"⏳ Interval antar siklus: {INTERVAL_MINUTES} menit")
print(f"⏱ Jeda antar grup: {DELAY_BETWEEN_GROUPS} detik\n")

if not PHONE_NUMBER or not API_ID or not API_HASH:
    raise ValueError("❌ Missing API_ID, API_HASH, or PHONE_NUMBER from .env")

# --- 3️⃣ Inisialisasi client Telethon ---
client = TelegramClient('session', API_ID, API_HASH)

# --- 4️⃣ Fungsi auto-forward ---
async def auto_forward():
    print(f"🤖 Bot aktif! Auto-forward setiap {INTERVAL_MINUTES} menit.\n")

    while True:
        try:
            async for message in client.iter_messages(SOURCE_CHANNEL, limit=1):
                if message:
                    for group in TARGET_GROUPS:
                        try:
                            # 📨 Forward pesan asli
                            forwarded = await client.forward_messages(group, message)
                            print(f"✅ Pesan dari {SOURCE_CHANNEL} diteruskan ke {group}")

                            print(f"💬 Teks tambahan dikirim ke {group}")
                            await asyncio.sleep(DELAY_BETWEEN_GROUPS)

                        except Exception as e:
                            print(f"⚠️ Gagal kirim ke {group}: {e}")
                            await asyncio.sleep(3)

            print(f"🕒 Menunggu {INTERVAL_MINUTES} menit sebelum siklus berikutnya...\n")
            await asyncio.sleep(INTERVAL_MINUTES * 60)

        except Exception as e:
            print(f"❌ Error utama: {e}")
            await asyncio.sleep(10)

# --- 5️⃣ Jalankan bot ---
async def main():
    await client.start(phone=PHONE_NUMBER)
    await auto_forward()

with client:
    client.loop.run_until_complete(main())
