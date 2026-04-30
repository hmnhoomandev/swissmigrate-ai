import re
from pathlib import Path
from typing import Any

from config import DATA_DIR
from utils.constants import FIRST_365_GUIDE_TOPICS


CONTENT_ROOT = DATA_DIR / "first_365_days"
CONTENT_FILE = "content.md"

CANTON_SLUGS = {
    "AG": "aargau",
    "AI": "appenzell_innerrhoden",
    "AR": "appenzell_ausserrhoden",
    "BE": "bern",
    "BL": "basel_landschaft",
    "BS": "basel_stadt",
    "FR": "fribourg",
    "GE": "geneva",
    "GL": "glarus",
    "GR": "graubunden",
    "JU": "jura",
    "LU": "lucerne",
    "NE": "neuchatel",
    "NW": "nidwalden",
    "OW": "obwalden",
    "SG": "st_gallen",
    "SH": "schaffhausen",
    "SO": "solothurn",
    "SZ": "schwyz",
    "TG": "thurgau",
    "TI": "ticino",
    "UR": "uri",
    "VD": "vaud",
    "VS": "valais",
    "ZG": "zug",
    "ZH": "zurich",
}

TOPIC_DETAILS: dict[str, dict[str, str]] = {
    "healthcare_insurance": {"label": "Healthcare & insurance", "icon": "Health", "timeframe": "Days 1-90"},
    "housing": {"label": "Housing", "icon": "Home", "timeframe": "Days 1-120"},
    "legal_permits": {"label": "Legal permits", "icon": "Permit", "timeframe": "Days 1-30"},
    "employment": {"label": "Employment", "icon": "Work", "timeframe": "Days 30-180"},
    "education": {"label": "Education", "icon": "Study", "timeframe": "Days 30-180"},
    "language_learning": {"label": "Language learning", "icon": "Language", "timeframe": "Days 15-120"},
    "financial_support": {"label": "Financial support", "icon": "Money", "timeframe": "Days 30-180"},
    "public_transport": {"label": "Public transport", "icon": "Transit", "timeframe": "Days 1-60"},
    "social_integration": {"label": "Social integration", "icon": "Community", "timeframe": "Days 30-365"},
    "mental_health": {"label": "Mental health", "icon": "Care", "timeframe": "Any time"},
    "registration_admin": {"label": "Registration/admin", "icon": "Admin", "timeframe": "Days 1-14"},
    "family_reunification": {"label": "Family reunification", "icon": "Family", "timeframe": "When relevant"},
    "digital_tools": {"label": "Digital tools", "icon": "Apps", "timeframe": "Days 1-30"},
}

DEFAULT_TOPIC_PRIORITIES = {topic: index + 1 for index, topic in enumerate(FIRST_365_GUIDE_TOPICS)}


def topic_options() -> list[dict[str, str]]:
    return [{"id": topic, **TOPIC_DETAILS[topic]} for topic in FIRST_365_GUIDE_TOPICS]


def content_path(canton_code: str, user_type: str, topic: str) -> Path:
    return CONTENT_ROOT / canton_slug(canton_code) / user_type / topic / CONTENT_FILE


def canton_slug(canton_code: str) -> str:
    normalized = canton_code.upper()
    return CANTON_SLUGS.get(normalized, canton_code.lower())


def scaffold_path(canton_code: str, user_type: str, topic: str) -> str:
    return str(content_path(canton_code, user_type, topic).relative_to(DATA_DIR.parent))


def load_first_365_content(canton_code: str, user_type: str, selected_topics: list[str]) -> list[dict[str, Any]]:
    normalized_canton = canton_code.lower()
    readable_canton = canton_slug(canton_code)
    requested_topics = [topic for topic in selected_topics if topic in FIRST_365_GUIDE_TOPICS]
    items = []

    for topic in requested_topics:
        candidate_dirs = [
            CONTENT_ROOT / readable_canton / user_type / topic,
            CONTENT_ROOT / readable_canton / "_shared" / topic,
            CONTENT_ROOT / normalized_canton / user_type / topic,
            CONTENT_ROOT / normalized_canton / "_shared" / topic,
            CONTENT_ROOT / "_shared" / user_type / topic,
            CONTENT_ROOT / "_shared" / "all" / topic,
        ]
        source_file = next((_first_markdown_file(path) for path in candidate_dirs if _first_markdown_file(path)), None)
        item = _default_item(canton_code, user_type, topic)
        if source_file:
            item.update(_parse_markdown_content(source_file.read_text(encoding="utf-8"), topic))
            item["source_file"] = str(source_file.relative_to(DATA_DIR.parent))
        else:
            item["source_file"] = scaffold_path(canton_code, user_type, topic)
            item["missing_content"] = True
        items.append(item)

    return sorted(items, key=lambda item: item.get("priority", 99))


def _first_markdown_file(folder: Path) -> Path | None:
    exact_file = folder / CONTENT_FILE
    if exact_file.exists() and exact_file.stat().st_size > 0:
        return exact_file
    if not folder.exists():
        return None
    markdown_files = sorted(path for path in folder.glob("*.md") if path.stat().st_size > 0)
    return markdown_files[0] if markdown_files else None


def _default_item(canton_code: str, user_type: str, topic: str) -> dict[str, Any]:
    details = TOPIC_DETAILS[topic]
    return {
        "topic": topic,
        "title": details["label"],
        "summary": (
            "Content for this canton and situation is not filled yet. "
            f"Add guidance in {scaffold_path(canton_code, user_type, topic)}."
        ),
        "timeframe": details["timeframe"],
        "priority": DEFAULT_TOPIC_PRIORITIES[topic],
        "actions": ["Add practical steps for this canton, situation, and topic."],
        "services": [],
        "sources": [],
    }


def _parse_markdown_content(markdown: str, topic: str) -> dict[str, Any]:
    lines = [line.rstrip() for line in markdown.splitlines()]
    result: dict[str, Any] = {
        "topic": topic,
        "title": TOPIC_DETAILS[topic]["label"],
        "summary": "",
        "timeframe": TOPIC_DETAILS[topic]["timeframe"],
        "priority": DEFAULT_TOPIC_PRIORITIES[topic],
        "actions": [],
        "services": [],
        "sources": [],
    }

    body_lines: list[str] = []
    section = "summary"

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            result["title"] = stripped[2:].strip()
            continue
        if stripped.lower().startswith("timeframe:"):
            result["timeframe"] = stripped.split(":", 1)[1].strip()
            continue
        if stripped.lower().startswith("priority:"):
            result["priority"] = _safe_int(stripped.split(":", 1)[1].strip(), result["priority"])
            continue
        if stripped.startswith("## "):
            section = stripped[3:].strip().lower()
            continue
        if section.startswith("action") and stripped.startswith("- "):
            result["actions"].append(stripped[2:].strip())
            continue
        if section.startswith("service") and stripped.startswith("- "):
            result["services"].append(_parse_link_line(stripped[2:].strip()))
            continue
        if section.startswith("source") and stripped.startswith("- "):
            result["sources"].append(_parse_link_line(stripped[2:].strip()))
            continue
        if section == "summary":
            body_lines.append(stripped)

    result["summary"] = " ".join(body_lines).strip() or result["summary"]
    return result


def _safe_int(value: str, fallback: int) -> int:
    try:
        return int(value)
    except ValueError:
        return fallback


def _parse_link_line(value: str) -> dict[str, str]:
    match = re.match(r"\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\s*-?\s*(?P<description>.*)", value)
    if match:
        return {
            "name": match.group("title").strip(),
            "title": match.group("title").strip(),
            "url": match.group("url").strip(),
            "contact": match.group("url").strip(),
            "description": match.group("description").strip(),
        }
    return {"name": value, "title": value, "description": "", "contact": "", "url": ""}
