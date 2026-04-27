import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from config import STORAGE_DIR, STORE_MASKED_INTERACTIONS


PROFILE_FILE = STORAGE_DIR / "user_profiles.csv"
INTERACTIONS_FILE = STORAGE_DIR / "interactions.csv"


def _ensure_storage() -> None:
    STORAGE_DIR.mkdir(exist_ok=True)
    if not PROFILE_FILE.exists() or PROFILE_FILE.stat().st_size == 0:
        PROFILE_FILE.write_text("created_at,language,canton_code,canton_name,user_type\n", encoding="utf-8")
    if not INTERACTIONS_FILE.exists() or INTERACTIONS_FILE.stat().st_size == 0:
        INTERACTIONS_FILE.write_text("created_at,module,summary,metadata\n", encoding="utf-8")


def save_profile(profile: dict[str, str]) -> None:
    _ensure_storage()
    with PROFILE_FILE.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["created_at", "language", "canton_code", "canton_name", "user_type"])
        writer.writerow(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "language": profile.get("language", ""),
                "canton_code": profile.get("canton_code", ""),
                "canton_name": profile.get("canton_name", ""),
                "user_type": profile.get("user_type", ""),
            }
        )


def save_interaction(module: str, summary: str, metadata: dict | None = None) -> None:
    if not STORE_MASKED_INTERACTIONS:
        return
    _ensure_storage()
    with INTERACTIONS_FILE.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["created_at", "module", "summary", "metadata"])
        writer.writerow(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "module": module,
                "summary": summary[:2000],
                "metadata": json.dumps(metadata or {}, ensure_ascii=False),
            }
        )


def get_recent_interactions(limit: int = 20) -> list[dict[str, str]]:
    _ensure_storage()
    with INTERACTIONS_FILE.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return list(reversed(rows[-limit:]))
