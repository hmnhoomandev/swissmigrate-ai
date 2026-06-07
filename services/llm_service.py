import json
import re
from datetime import datetime
from typing import Any

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from services.security_service import mask_pii


def _client() -> OpenAI | None:
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)


def _json_chat(system: str, user: str, fallback: dict[str, Any]) -> dict[str, Any]:
    client = _client()
    if client is None:
        return fallback
    safe_user = mask_pii(user).masked_text

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": safe_user},
            ],
        )
        return json.loads(response.choices[0].message.content or "{}")
    except Exception as exc:
        fallback["service_warning"] = f"AI service unavailable: {exc}"
        return fallback


def analyze_letter(masked_text: str, language_name: str) -> dict[str, Any]:
    fallback = {
        "summary": {
            "topic": "Not specified in the letter",
            "sender": "Not specified in the letter",
            "date": "Not specified in the letter",
            "recipient": "Not specified in the letter",
            "summary": "The letter could not be analyzed by the AI service. Please review the masked text and try again.",
        },
        "urgency": {
            "level": "No clear deadline found",
            "days_left": "Not specified in the letter",
        },
        "translation": masked_text,
        "action_steps": [
            "Read the letter date and any deadline carefully.",
            "Prepare documents mentioned in the letter.",
            "Contact the office or a trusted advisor if anything is unclear.",
        ],
    }
    today = datetime.now().date().isoformat()
    system = (
        "You help migrants in Switzerland understand official letters. "
        "You must use only the information present in the masked text. "
        "Never guess missing information, never infer hidden personal data from masked tokens, and never hallucinate. "
        "If a field is missing, write exactly: Not specified in the letter. "
        "Keep redacted privacy values such as [NAME:Ho...an], [EMAIL:jo...@ex...le.com], [PHONE:+41 79 ... 67], [ADDRESS:Ma...et 12], and [ID:AB...12] unchanged. "
        f"Today is {today}. Calculate days_left from any explicit deadline in the letter. "
        "Urgency rules: 0-1 days = VERY URGENT, 2-3 days = URGENT, 3-5 days = MEDIUM, 5+ days = LOW. "
        "If no clear deadline exists, urgency.level must be No clear deadline found and urgency.days_left must be Not specified in the letter. "
        f"Create a short translation field in {language_name}; the app will produce the full line-by-line translation separately. "
        "Return only valid JSON with this exact structure: "
        '{"summary":{"topic":"","sender":"","date":"","recipient":"","summary":""},'
        '"urgency":{"level":"","days_left":""},"translation":"","action_steps":[]}.'
    )
    user = f"Analyze this masked official letter:\n\n{masked_text[:16000]}"
    result = _json_chat(system, user, fallback)
    normalized = _normalize_letter_result(result, fallback)
    normalized["translation"] = translate_full_text(masked_text, language_name)
    return normalized


def translate_full_text(masked_text: str, language_name: str) -> str:
    fallback = {"translation": masked_text}
    system = (
        f"Translate the complete masked document into {language_name}. "
        "This is a full-document translation task, not a summary task. "
        "Preserve every visible line, ticket block, date, time, route, price, order number, reference number, and note. "
        "Do not omit repeated sections. Do not combine several tickets into one sentence. "
        "Keep line breaks and the original order as much as possible. "
        "Translate all human-readable words that are not already in the target language. "
        "If a line is already in the target language, copy it or lightly normalize it without deleting it. "
        "Keep proper nouns, station names, product codes, numbers, dates, times, and currency values unchanged. "
        "Keep redacted privacy values in square brackets exactly as written, for example [NAME:Ho...an]. "
        "Never guess missing or hidden characters. "
        "Return only valid JSON with one key: translation."
    )
    user = f"Translate this full masked document line by line:\n\n{masked_text[:20000]}"
    result = _json_chat(system, user, fallback)
    if result.get("service_warning"):
        return "Translation service unavailable; showing the extracted masked text instead.\n\n" + masked_text
    translation = result.get("translation")
    if isinstance(translation, str) and _looks_complete_translation(masked_text, translation):
        return translation.strip()

    retry_system = (
        f"Your previous output was incomplete. Translate the entire masked document into {language_name}. "
        "Output every ticket/block and every meaningful source line. Do not summarize. "
        "Keep station names, cities, dates, times, prices, product names, and all bracketed redactions unchanged. "
        "Return only valid JSON with one key: translation."
    )
    retry_user = (
        "Translate the complete document. Keep approximately the same structure and number of blocks:\n\n"
        f"{masked_text[:20000]}"
    )
    retry = _json_chat(retry_system, retry_user, fallback)
    retry_translation = retry.get("translation")
    if isinstance(retry_translation, str) and _looks_complete_translation(masked_text, retry_translation):
        return retry_translation.strip()

    return "Full translation was incomplete; showing the full extracted masked text instead.\n\n" + masked_text


def _looks_complete_translation(source: str, translation: str) -> bool:
    source_lines = [line for line in source.splitlines() if line.strip()]
    translated_lines = [line for line in translation.splitlines() if line.strip()]
    if not translation.strip():
        return False
    if len(source) > 1200 and len(translation) < len(source) * 0.45:
        return False
    if len(source_lines) > 20 and len(translated_lines) < len(source_lines) * 0.35:
        return False
    return True


def _normalize_letter_result(result: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "summary": {**fallback["summary"], **(result.get("summary") if isinstance(result.get("summary"), dict) else {})},
        "urgency": {**fallback["urgency"], **(result.get("urgency") if isinstance(result.get("urgency"), dict) else {})},
        "translation": result.get("translation") if isinstance(result.get("translation"), str) else fallback["translation"],
        "action_steps": result.get("action_steps") if isinstance(result.get("action_steps"), list) else fallback["action_steps"],
    }
    normalized["urgency"] = _normalize_urgency(normalized["urgency"])
    if result.get("service_warning"):
        normalized["service_warning"] = result["service_warning"]
    return normalized


def _normalize_urgency(urgency: dict[str, Any]) -> dict[str, Any]:
    days_value = urgency.get("days_left", "Not specified in the letter")
    days_left = _parse_days_left(days_value)
    if days_left is None:
        return {
            **urgency,
            "level": "No clear deadline found",
            "days_left": "Not specified in the letter",
        }

    if days_left <= 1:
        level = "VERY URGENT"
    elif days_left <= 3:
        level = "URGENT"
    elif days_left <= 5:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {**urgency, "level": level, "days_left": str(days_left)}


def _parse_days_left(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return max(value, 0)
    if isinstance(value, float):
        return max(int(value), 0)
    if not isinstance(value, str):
        return None

    normalized = value.strip().lower()
    if not normalized or "not specified" in normalized or "no clear" in normalized or "none" == normalized:
        return None

    match = re.search(r"-?\d+", normalized)
    if not match:
        return None
    return max(int(match.group(0)), 0)


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


def translate_first_365_items(items: list[dict[str, Any]], language_name: str) -> dict[str, Any]:
    if language_name.lower() == "english":
        return {"items": items}
    if _client() is None:
        return {
            "items": items,
            "service_warning": "AI translation is unavailable because OPENAI_API_KEY is not configured; showing English content.",
        }

    fallback = {"items": items}
    system = (
        f"Translate first-year settlement guidance into {language_name}. "
        "Translate only user-facing human-readable text. "
        "Preserve the JSON structure exactly. "
        "Do not translate URLs, source_file paths, topic ids, contact URLs, or numeric priorities. "
        "Keep services and sources as objects with the same keys. "
        "Keep the content practical, clear, and non-alarming. "
        "Return only valid JSON with one key: items."
    )
    user = json.dumps({"items": items}, ensure_ascii=False)
    result = _json_chat(system, user, fallback)
    if not isinstance(result.get("items"), list):
        return fallback
    return result


def answer_with_context(question: str, profile: dict[str, str], contexts: list[dict[str, Any]], language_name: str) -> dict[str, Any]:
    fallback = _grounded_navigator_fallback(question, contexts)
    system = (
        "You are a grounded Swiss canton navigator for migrants and refugees. "
        "Use only the provided retrieved_context. Do not use outside knowledge. "
        "If the context is insufficient, say exactly what is missing and suggest checking the listed sources. "
        "Prefer concrete steps that are explicitly supported by the context. "
        f"Return valid JSON in {language_name} with keys: answer, steps, services, sources, confidence."
    )
    user = json.dumps(
        {"profile": profile, "question": question, "retrieved_context": contexts},
        ensure_ascii=False,
    )
    return _json_chat(system, user, fallback)


def _grounded_navigator_fallback(question: str, contexts: list[dict[str, Any]]) -> dict[str, Any]:
    sources = [_source_from_context(context) for context in contexts if _source_from_context(context)]
    document_contexts = [context for context in contexts if context.get("kind") == "document" and context.get("content")]
    services = [
        {"name": context.get("name", ""), "contact": context.get("contact", ""), "description": context.get("description", "")}
        for context in contexts
        if context.get("kind") == "service"
    ]

    if not document_contexts and not services:
        return {
            "answer": (
                "I could not find enough local source material for this question. "
                "Please add a Markdown, PDF, Word, or text file to the matching canton/status folder and try again."
            ),
            "steps": [],
            "services": [],
            "sources": sources,
            "confidence": "low",
        }

    snippets = []
    for context in document_contexts[:3]:
        snippets.append(f"{context.get('title', 'Source')}: {context.get('content', '').strip()[:650]}")

    answer = "Based only on the available local sources, here is what I found"
    if question:
        answer += f" for your question: {question.strip()}"
    answer += ".\n\n" + "\n\n".join(snippets)
    if services:
        answer += "\n\nRelevant local service records are listed below."

    return {
        "answer": answer.strip(),
        "steps": _steps_from_contexts(document_contexts),
        "services": services[:4],
        "sources": sources,
        "confidence": "medium" if document_contexts else "low",
    }


def _source_from_context(context: dict[str, Any]) -> dict[str, str]:
    source = context.get("source")
    if isinstance(source, dict):
        return source
    if context.get("source_file"):
        return {
            "title": context.get("title", "Local source"),
            "url": context["source_file"],
            "description": context.get("scope", ""),
        }
    return {}


def _steps_from_contexts(contexts: list[dict[str, Any]]) -> list[str]:
    steps: list[str] = []
    for context in contexts:
        content = context.get("content", "")
        for line in content.splitlines():
            cleaned = line.strip().lstrip("-*").strip()
            if 18 <= len(cleaned) <= 180 and cleaned not in steps:
                steps.append(cleaned)
            if len(steps) >= 5:
                return steps
    return steps

def ask_llm_json(prompt: str, fallback: dict | None = None) -> dict:

    fallback = fallback or {}

    system = (
        "Return only valid JSON. "
        "Never hallucinate missing information. "
        "If unsure, return empty values."
    )

    return _json_chat(
        system=system,
        user=prompt,
        fallback=fallback,
    )


