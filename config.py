import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_GROUPS = [g.strip() for g in os.getenv("TARGET_GROUPS", "").split(",")]
INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES", "2"))
