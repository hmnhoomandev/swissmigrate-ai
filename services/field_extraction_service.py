import re
import dateparser

from services.llm_service import ask_llm_json

from utils.regex_patterns import (
    DATE_PATTERNS,
    CASE_PATTERNS,
)

from utils.constants import (
    LOW_CONFIDENCE_THRESHOLD,
)

AUTHORITIES = [
    "SEM",
    "State Secretariat for Migration",
    "Tribunal administratif",
    "Office cantonal",
    "Migration Office",
    "Population Office",
]


class FieldExtractionService:

    @staticmethod
    def extract_case_numbers(text):

        found = []

        for pattern in CASE_PATTERNS:

            matches = re.findall(pattern, text)

            for match in matches:

                found.append({
                    "value": match,
                    "confidence": 0.92,
                    "source": "regex",
                })

        return found

    @staticmethod
    def extract_dates(text):

        found = []

        for pattern in DATE_PATTERNS:

            matches = re.findall(pattern, text)

            for match in matches:

                parsed = dateparser.parse(match)

                if parsed:

                    found.append({
                        "value": parsed.strftime("%Y-%m-%d"),
                        "confidence": 0.88,
                        "source": "regex",
                    })

        return found

    @staticmethod
    def extract_authorities(text):

        results = []

        lower = text.lower()

        for authority in AUTHORITIES:

            if authority.lower() in lower:

                results.append({
                    "value": authority,
                    "confidence": 0.90,
                    "source": "authority_match",
                })

        return results

    @staticmethod
    def extract_actions(text):

        prompt = f"""
Extract required actions from this Swiss migration/legal document.

Return ONLY valid JSON.

{{
    "required_actions": [
        {{
            "action": "",
            "deadline": "",
            "confidence": 0.0
        }}
    ]
}}

Rules:
- Never hallucinate
- Keep actions short
- If no action exists return empty array
- Confidence must be between 0 and 1

DOCUMENT:
{text[:6000]}
"""

        try:

            result = ask_llm_json(prompt)

            return result.get("required_actions", [])

        except Exception:

            return []

    @staticmethod
    def extract_all(text):

        dates = FieldExtractionService.extract_dates(text)

        case_numbers = FieldExtractionService.extract_case_numbers(text)

        authorities = FieldExtractionService.extract_authorities(text)

        actions = FieldExtractionService.extract_actions(text)

        review_required = False

        all_scores = []

        for section in [dates, case_numbers, authorities]:

            for item in section:
                all_scores.append(item.get("confidence", 0))

        for action in actions:
            all_scores.append(action.get("confidence", 0))

        if all_scores:

            avg_confidence = sum(all_scores) / len(all_scores)

            if avg_confidence < LOW_CONFIDENCE_THRESHOLD:
                review_required = True

        else:
            avg_confidence = 0.0
            review_required = True

        return {
            "dates": dates,
            "case_numbers": case_numbers,
            "authorities": authorities,
            "required_actions": actions,
            "average_confidence": round(avg_confidence, 2),
            "manual_review_required": review_required,
        }

