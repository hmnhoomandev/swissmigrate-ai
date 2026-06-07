from services.llm_service import ask_llm_json

from utils.constants import (
    DOCUMENT_TYPES,
)


class DocumentClassifierService:

    RULES = {
        "decision": [
            "decision",
            "final decision",
            "negative decision",
            "rejected",
            "approved",
        ],

        "summons": [
            "summons",
            "hearing",
            "convocation",
            "appearance required",
        ],

        "request": [
            "we request",
            "submit documents",
            "provide",
            "missing documents"
            "please send",
            "please submit",
            "please provide",
        ],

        "form": [
            "application form",
            "formulaire",
            "registration form",
        ],

        "notice": [
            "notice",
            "notification",
            "important notice",
        ],

        "appeal_response": [
            "appeal response",
            "appeal has been registered",
            "appeal outcome",
            "under review",
        ]
    }

    @staticmethod
    def classify(text: str):

        if not text or not text.strip():

            return {
                "value": "unknown",
                "confidence": 0.0,
                "source": "empty_text",
            }

        lower = text.lower()

        # Rule-based classification first

        for doc_type, keywords in DocumentClassifierService.RULES.items():

            for keyword in keywords:

                if keyword.lower() in lower:

                    return {
                        "value": doc_type,
                        "confidence": 0.92,
                        "source": "rule",
                    }

        #LLM classification

        return DocumentClassifierService.llm_classify(text)

    @staticmethod
    def llm_classify(text: str):

        prompt = f"""
You classify Swiss migration and administrative documents.

Possible document categories:

{", ".join(DOCUMENT_TYPES)}

Return ONLY valid JSON.

{{
    "document_type": "",
    "confidence": 0.0,
    "reason": ""
}}

Rules:
- Never guess
- Use 'unknown' if uncertain
- Confidence must be between 0 and 1
- Keep reasoning short

DOCUMENT:
{text[:8000]}
"""

        try:

            result = ask_llm_json(prompt)

            return {
                "value": result.get("document_type", "unknown"),
                "confidence": float(result.get("confidence", 0.5)),
                "source": "llm",
                "reason": result.get("reason", ""),
            }

        except Exception:

            return {
                "value": "unknown",
                "confidence": 0.0,
                "source": "classification_error",
            }
