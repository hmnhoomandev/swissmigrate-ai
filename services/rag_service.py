import json
import re
from pathlib import Path
from typing import Any

from config import DATA_DIR


KNOWLEDGE_FILE = DATA_DIR / "canton_knowledge.json"


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
        candidates.extend({"kind": "service", "score": 0, **service} for service in data.get("services", [])[:3])

    return sorted(candidates, key=lambda value: value["score"], reverse=True)[:limit]
