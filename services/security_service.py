import re
from dataclasses import dataclass


@dataclass
class MaskingResult:
    masked_text: str
    counts: dict


PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone": r"(?:(?:\+|00)41|0)\s?(?:\d[\s().-]?){8,12}",
    "permit_or_id": r"\b(?:ZEMIS|N|F|B|C|L|G|S)[\s:-]?\d{5,12}\b|\b\d{3}\.\d{4}\.\d{4}\.\d{2}\b|\b\d{6,12}\b",
    "address": r"\b(?:Rue|Avenue|Av\.|Chemin|Route|Boulevard|Place|Strasse|Gasse|Weg|Via|Piazza)\s+[A-Za-zÀ-ÿ'\- ]+\s+\d+[A-Za-z]?\b|\b\d{4}\s+[A-Za-zÀ-ÿ'\- ]+\b",
}


def _replace(pattern: str, label: str, text: str) -> tuple[str, int]:
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return re.sub(pattern, f"[{label}]", text, flags=re.IGNORECASE), len(matches)


def mask_pii(text: str) -> MaskingResult:
    masked = text or ""
    counts = {}

    for key, pattern in PATTERNS.items():
        masked, count = _replace(pattern, key.upper(), masked)
        counts[key] = count

    name_pattern = r"\b[A-ZÀ-Ý][a-zà-ÿ'\-]{2,}\s+[A-ZÀ-Ý][a-zà-ÿ'\-]{2,}(?:\s+[A-ZÀ-Ý][a-zà-ÿ'\-]{2,})?\b"
    masked, count = _replace(name_pattern, "NAME", masked)
    counts["possible_names"] = count

    return MaskingResult(masked_text=masked, counts=counts)
