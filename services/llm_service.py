import json
from typing import Any

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL


def _client() -> OpenAI | None:
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)


def _json_chat(system: str, user: str, fallback: dict[str, Any]) -> dict[str, Any]:
    client = _client()
    if client is None:
        return fallback

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return json.loads(response.choices[0].message.content or "{}")
    except Exception as exc:
        fallback["service_warning"] = f"AI service unavailable: {exc}"
        return fallback


def analyze_letter(masked_text: str, language_name: str) -> dict[str, Any]:
    fallback = {
        "simple_explanation": "The uploaded letter appears to ask you to check instructions, deadlines, and required documents.",
        "urgency": "Medium",
        "deadline": "No exact deadline detected by the fallback analyzer.",
        "actions": [
            "Read the letter date and any deadline carefully.",
            "Prepare documents mentioned in the letter.",
            "Contact the office or a trusted advisor if anything is unclear.",
        ],
        "suggested_reply": "Dear Sir or Madam,\n\nI confirm that I received your letter. I will review the requested steps and provide the necessary documents as soon as possible.\n\nKind regards",
        "confidence": "low",
    }
    system = (
        "You help migrants in Switzerland understand official letters. "
        "Use simple, calm language. Never give definitive legal advice. "
        f"Return only valid JSON in {language_name}. Keys: simple_explanation, urgency, deadline, actions, suggested_reply, confidence."
    )
    user = f"Analyze this masked official letter:\n\n{masked_text[:12000]}"
    return _json_chat(system, user, fallback)


def personalize_guide(profile: dict[str, str], checklist: list[dict[str, Any]], language_name: str) -> dict[str, Any]:
    fallback = {"items": checklist, "note": "This guide is generated from structured local data.", "confidence": "medium"}
    system = (
        "You adapt a first-year settlement checklist for Switzerland. "
        "Keep every item practical, short, and non-alarming. "
        f"Return valid JSON in {language_name} with keys: items, note, confidence. "
        "Each item should keep title, topic, priority, timeframe, actions, services, sources."
    )
    user = json.dumps({"profile": profile, "checklist": checklist}, ensure_ascii=False)
    return _json_chat(system, user, fallback)


def answer_with_context(question: str, profile: dict[str, str], contexts: list[dict[str, Any]], language_name: str) -> dict[str, Any]:
    fallback = {
        "answer": "I found limited trusted context. Please contact your canton integration office or a qualified advisor for confirmation.",
        "steps": [],
        "services": [],
        "sources": [context.get("source", {}) for context in contexts],
        "confidence": "low",
    }
    system = (
        "You are a grounded Swiss canton navigator for migrants and refugees. "
        "Use only the provided context. If context is insufficient, say so. "
        f"Return valid JSON in {language_name} with keys: answer, steps, services, sources, confidence."
    )
    user = json.dumps(
        {"profile": profile, "question": question, "retrieved_context": contexts},
        ensure_ascii=False,
    )
    return _json_chat(system, user, fallback)
