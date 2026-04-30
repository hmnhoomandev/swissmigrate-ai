import json
import re
from pathlib import Path
from typing import Any

import pdfplumber
from docx import Document

from config import DATA_DIR
from services.first_365_content_service import CANTON_SLUGS, CONTENT_ROOT, TOPIC_DETAILS, canton_slug


KNOWLEDGE_FILE = DATA_DIR / "canton_knowledge.json"
SUPPORTED_DOCUMENTS = {".md", ".txt", ".pdf", ".docx"}


def _load_all() -> dict[str, Any]:
    with KNOWLEDGE_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_canton_dataset(canton_code: str) -> dict[str, Any]:
    all_data = _load_all()
    dataset = all_data["cantons"].get(canton_code, {})

    override_file = DATA_DIR / "cantons" / f"{canton_code.lower()}.json"
    if override_file.exists() and override_file.stat().st_size > 0:
        with override_file.open("r", encoding="utf-8") as handle:
            override = json.load(handle)
        dataset = {**dataset, **override}

    if not dataset.get("sources"):
        dataset["sources"] = [
            {
                "title": "ch.ch foreigners in Switzerland",
                "url": "https://www.ch.ch/en/foreign-nationals-in-switzerland/",
                "description": "Federal information for foreign nationals in Switzerland.",
            }
        ]
    if not dataset.get("services"):
        dataset["services"] = [
            {
                "name": dataset.get("integration_office", "Cantonal integration office"),
                "topics": [
                    "registration_admin",
                    "legal_permits",
                    "language_learning",
                    "social_integration",
                    "letters_documents",
                ],
                "description": f"Official integration and migration guidance for {dataset.get('name', canton_code)}.",
                "contact": "Use the official canton portal or ch.ch to verify the current contact point.",
            }
        ]

    return dataset


def build_first_365_checklist(canton_code: str, user_type: str) -> list[dict[str, Any]]:
    data = load_canton_dataset(canton_code)
    common = _load_all().get("first_365_template", [])
    local_services = data.get("services", [])
    items = []

    for item in common:
        audience = item.get("audience", [])
        if audience and user_type not in audience and "all" not in audience:
            continue
        topic_services = [service for service in local_services if item["topic"] in service.get("topics", [])]
        enriched = dict(item)
        enriched["services"] = topic_services[:3]
        enriched["sources"] = data.get("sources", [])[:3]
        items.append(enriched)

    return sorted(items, key=lambda value: value.get("priority", 99))


def _tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[A-Za-zÀ-ÿ0-9]{3,}", text.lower())}


def retrieve_context(question: str, canton_code: str, user_type: str, limit: int = 6) -> list[dict[str, Any]]:
    data = load_canton_dataset(canton_code)
    query_tokens = _tokens(f"{question} {user_type}")
    candidates = []

    for document in load_canton_documents(canton_code, user_type):
        haystack = " ".join(
            [
                document.get("title", ""),
                document.get("topic", ""),
                document.get("content", ""),
                document.get("scope", ""),
            ]
        )
        score = len(query_tokens & _tokens(haystack))
        if score:
            candidates.append({"kind": "document", "score": score + document.get("boost", 0), **document})

    for service in data.get("services", []):
        haystack = " ".join(
            [
                service.get("name", ""),
                service.get("description", ""),
                " ".join(service.get("topics", [])),
                service.get("contact", ""),
            ]
        )
        score = len(query_tokens & _tokens(haystack))
        if score:
            candidates.append({"kind": "service", "score": score, **service})

    for source in data.get("sources", []):
        score = len(query_tokens & _tokens(f"{source.get('title', '')} {source.get('description', '')}"))
        if score:
            candidates.append({"kind": "source", "score": score, "source": source})

    if not candidates:
        candidates.extend(
            {"kind": "document", "score": 0, **document}
            for document in load_canton_documents(canton_code, user_type)[:3]
        )
        candidates.extend({"kind": "service", "score": 0, **service} for service in data.get("services", [])[:3])

    return sorted(candidates, key=lambda value: value["score"], reverse=True)[:limit]


def load_canton_documents(canton_code: str, user_type: str) -> list[dict[str, Any]]:
    """Collect source documents from the existing first-365 folder structure."""
    documents: list[dict[str, Any]] = []
    seen: set[Path] = set()

    for folder, scope, boost in _candidate_document_roots(canton_code, user_type):
        if not folder.exists():
            continue
        for file_path in sorted(folder.rglob("*")):
            if file_path in seen or not file_path.is_file() or file_path.suffix.lower() not in SUPPORTED_DOCUMENTS:
                continue
            if file_path.name.lower() == ".gitkeep" or file_path.stat().st_size == 0:
                continue
            seen.add(file_path)
            text = _read_document(file_path)
            if text.strip():
                topic = _topic_from_path(file_path)
                documents.extend(_chunk_document(file_path, text, topic, scope, boost))

    return documents


def _candidate_document_roots(canton_code: str, user_type: str) -> list[tuple[Path, str, int]]:
    readable_canton = canton_slug(canton_code)
    normalized_canton = canton_code.lower()
    roots = [
        (CONTENT_ROOT / readable_canton / user_type, "selected canton and situation", 4),
        (CONTENT_ROOT / normalized_canton / user_type, "selected canton and situation", 4),
        (CONTENT_ROOT / readable_canton / "_shared", "selected canton shared guidance", 3),
        (CONTENT_ROOT / normalized_canton / "_shared", "selected canton shared guidance", 3),
        (CONTENT_ROOT / "_shared" / user_type, "all cantons for this situation", 2),
        (CONTENT_ROOT / "_shared" / "all", "all cantons shared guidance", 1),
    ]

    for code, slug in CANTON_SLUGS.items():
        if code.lower() == normalized_canton or slug == readable_canton:
            roots.extend(
                [
                    (CONTENT_ROOT / code.lower() / user_type, "selected canton and situation", 4),
                    (CONTENT_ROOT / code.lower() / "_shared", "selected canton shared guidance", 3),
                ]
            )

    unique = []
    seen = set()
    for path, scope, boost in roots:
        resolved = path.resolve()
        if resolved not in seen:
            unique.append((path, scope, boost))
            seen.add(resolved)
    return unique


def _read_document(path: Path) -> str:
    try:
        if path.suffix.lower() in {".md", ".txt"}:
            return path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".pdf":
            with pdfplumber.open(path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
        if path.suffix.lower() == ".docx":
            document = Document(path)
            return "\n".join(paragraph.text for paragraph in document.paragraphs)
    except Exception:
        return ""
    return ""


def _topic_from_path(path: Path) -> str:
    parts = {part.lower() for part in path.parts}
    for topic in TOPIC_DETAILS:
        if topic.lower() in parts:
            return topic
    return "general"


def _chunk_document(path: Path, text: str, topic: str, scope: str, boost: int) -> list[dict[str, Any]]:
    title = _document_title(text, path, topic)
    cleaned = _clean_markdown(text)
    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", cleaned) if paragraph.strip()]
    chunks: list[dict[str, Any]] = []
    current: list[str] = []

    for paragraph in paragraphs:
        current.append(paragraph)
        if sum(len(item) for item in current) >= 900:
            chunks.append(_document_chunk(path, title, topic, scope, boost, "\n\n".join(current)))
            current = []

    if current:
        chunks.append(_document_chunk(path, title, topic, scope, boost, "\n\n".join(current)))

    return chunks


def _document_chunk(path: Path, title: str, topic: str, scope: str, boost: int, content: str) -> dict[str, Any]:
    relative_path = str(path.relative_to(DATA_DIR.parent))
    return {
        "title": title,
        "topic": topic,
        "scope": scope,
        "content": content[:1800],
        "source_file": relative_path,
        "source": {
            "title": f"{title} ({scope})",
            "url": relative_path,
            "description": f"Local knowledge file for {topic}.",
        },
        "boost": boost,
    }


def _document_title(text: str, path: Path, topic: str) -> str:
    heading = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if heading:
        return heading.group(1).strip()
    return TOPIC_DETAILS.get(topic, {}).get("label") or path.stem.replace("_", " ").title()


def _clean_markdown(text: str) -> str:
    without_links = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    without_headings = re.sub(r"^#{1,6}\s*", "", without_links, flags=re.MULTILINE)
    return re.sub(r"\n{3,}", "\n\n", without_headings).strip()
