import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from config import STORAGE_DIR, STORE_MASKED_INTERACTIONS
from services.security_service import mask_payload, mask_pii


PROFILE_FILE = STORAGE_DIR / "user_profiles.csv"
INTERACTIONS_FILE = STORAGE_DIR / "interactions.csv"
DATABASE_FILE = STORAGE_DIR / "swissmigrate.db"


def _ensure_storage() -> None:
    STORAGE_DIR.mkdir(exist_ok=True)
    if not PROFILE_FILE.exists() or PROFILE_FILE.stat().st_size == 0:
        PROFILE_FILE.write_text("created_at,language,canton_code,canton_name,user_type\n", encoding="utf-8")
    if not INTERACTIONS_FILE.exists() or INTERACTIONS_FILE.stat().st_size == 0:
        INTERACTIONS_FILE.write_text("created_at,module,summary,metadata\n", encoding="utf-8")


def ensure_user_id(session_state) -> str:
    if "user_id" not in session_state:
        session_state["user_id"] = str(uuid4())
    return session_state["user_id"]


def _connect() -> sqlite3.Connection:
    _ensure_storage()
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            masked_input TEXT NOT NULL,
            summary TEXT NOT NULL,
            urgency TEXT NOT NULL,
            translation TEXT NOT NULL,
            action_steps TEXT NOT NULL
        )
        """
    )
    return connection


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
    masked_summary = mask_pii(summary).masked_text
    masked_metadata = mask_payload(metadata or {})
    with INTERACTIONS_FILE.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["created_at", "module", "summary", "metadata"])
        writer.writerow(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "module": module,
                "summary": masked_summary[:2000],
                "metadata": json.dumps(masked_metadata, ensure_ascii=False),
            }
        )


def get_recent_interactions(limit: int = 20) -> list[dict[str, str]]:
    _ensure_storage()
    with INTERACTIONS_FILE.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return list(reversed(rows[-limit:]))


def save_letter_history(user_id: str, masked_input: str, analysis: dict) -> None:
    if not STORE_MASKED_INTERACTIONS:
        return
    masked_analysis = mask_payload(analysis)
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO history (user_id, timestamp, masked_input, summary, urgency, translation, action_steps)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                datetime.now(timezone.utc).isoformat(),
                mask_pii(masked_input).masked_text[:20000],
                json.dumps(masked_analysis.get("summary", {}), ensure_ascii=False),
                json.dumps(masked_analysis.get("urgency", {}), ensure_ascii=False),
                str(masked_analysis.get("translation", ""))[:20000],
                json.dumps(masked_analysis.get("action_steps", []), ensure_ascii=False),
            ),
        )


def get_letter_history(user_id: str | None = None, limit: int = 20) -> list[dict]:
    with _connect() as connection:
        if user_id:
            rows = connection.execute(
                "SELECT * FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
        else:
            rows = connection.execute("SELECT * FROM history ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()

    history = []
    for row in rows:
        item = dict(row)
        for key in ("summary", "urgency", "action_steps"):
            try:
                item[key] = json.loads(item[key])
            except json.JSONDecodeError:
                item[key] = {} if key != "action_steps" else []
        history.append(item)
    return history
