import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"

load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

APP_ENV = os.getenv("APP_ENV", "local")
STORE_MASKED_INTERACTIONS = os.getenv("STORE_MASKED_INTERACTIONS", "true").lower() == "true"
