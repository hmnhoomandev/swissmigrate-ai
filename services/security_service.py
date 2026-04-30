import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Any


@dataclass
class MaskingResult:
    masked_text: str
    counts: dict[str, int]
    mapping: dict[str, list[str]]


SENSITIVE_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "IBAN": r"\b[A-Z]{2}\d{2}(?:[\s-]?[A-Z0-9]){11,30}\b",
    "CREDIT_CARD": r"\b(?:\d[ -]?){13,19}\b",
    "PHONE": (
        r"(?<![\d.])(?:(?:\+|00)\d{1,3}[\s().-]?(?:\d[\s().-]?){8,12}"
        r"|0\d{1,2}[\s()-]?(?:\d[\s()-]?){7,10})(?![\d.:])"
    ),
    "ID": (
        r"\b(?:Ticket-ID|Order\s+no\.?|VAT\s+Reference\s+no\.?|Reference\s+no\.?|ZEMIS|AVS|AHV|"
        r"Case|Dossier|Aktenzeichen|Referenz|Numero|Nummer|Permit|Client\s+ID|Customer\s+ID)"
        r"\s?[:#-]?\s?[A-Z0-9][A-Z0-9./-]{4,24}\b"
        r"|\b(?:N|F|B|C|L|G|S)[\s:-]?\d{5,12}\b"
        r"|\b\d{3}\.\d{4}\.\d{4}\.\d{2}\b"
    ),
    "ADDRESS": (
        r"\b(?:Rue|Avenue|Av\.|Chemin|Route|Boulevard|Place|Strasse|Str\.|Gasse|Weg|"
        r"Via|Piazza|Allee|Quai|Street|St\.|Road|Rd\.)\s+[A-Za-zÀ-ÿ'’.\- ]+\s+\d+[A-Za-z]?\b"
    ),
}


NAME_PREFIX_RE = (
    r"\b(?:Name|Nom|Passenger|Passagier|Ticket|Customer|Kunde|Client|Dear|Cher|Chère|"
    r"Monsieur|Madame|Herr|Frau|Mr\.?|Mrs\.?|Ms\.?)\s+"
    r"([A-ZÀ-Ý][A-Za-zÀ-ÿ'’\-]{2,}(?:[ \t]+[A-ZÀ-Ý][A-Za-zÀ-ÿ'’\-]{2,}){1,3})"
)

SIGNATURE_NAME_RE = (
    r"(?:^|\n)\s*([A-ZÀ-Ý][A-Za-zÀ-ÿ'’\-]{2,}"
    r"(?:[ \t]+[A-ZÀ-Ý][A-Za-zÀ-ÿ'’\-]{2,}){1,3})\s*$"
)

SENDER_NAME_RE = (
    r"\b(?:Sender|From|Absender|Expediteur|Expéditeur|De|Von)\s*[:\-]?\s+"
    r"([^\n\r,;]{3,80})"
)

SENDER_BLOCK_RE = (
    r"(?im)^\s*(?:Sender|From|Absender|Expediteur|Expéditeur|De|Von)\s*[:\-]\s*$\n"
    r"\s*([^\n\r,;]{3,80})"
)

NAME_STOP_WORDS = {
    "article",
    "bern",
    "billet",
    "bundesbahnen",
    "cff",
    "chf",
    "class",
    "extract",
    "geneve",
    "geneva",
    "genève",
    "lausanne",
    "order",
    "pass",
    "point",
    "reduced",
    "réduit",
    "sbb",
    "schweizerische",
    "swiss",
    "ticket",
    "valid",
    "vat",
    "zurich",
    "zürich",
}


@lru_cache(maxsize=1)
def _spacy_model():
    try:
        import spacy

        for model_name in ("de_core_news_sm", "fr_core_news_sm", "en_core_web_sm", "xx_ent_wiki_sm"):
            try:
                return spacy.load(model_name)
            except OSError:
                continue
    except Exception:
        return None
    return None


def mask_pii(text: str) -> MaskingResult:
    masked = text or ""
    counts: dict[str, int] = {}
    mapping: dict[str, list[str]] = {}

    for label, pattern in SENSITIVE_PATTERNS.items():
        flags = 0 if label == "ADDRESS" else re.IGNORECASE
        values = _collect_matches(pattern, masked, flags=flags)
        if label == "CREDIT_CARD":
            # Mask any sequence that looks like a credit card format, even if invalid
            values = [value for value in values if len(re.sub(r"\D", "", value)) >= 13]
        masked, count = _replace_values(masked, values, label, mapping)
        counts[label.lower()] = count

    name_values = _name_candidates(masked)
    masked, name_count = _replace_values(masked, name_values, "NAME", mapping)
    counts["names"] = name_count

    return MaskingResult(masked_text=masked, counts=counts, mapping=mapping)


def mask_payload(value: Any) -> Any:
    if isinstance(value, str):
        return mask_pii(value).masked_text
    if isinstance(value, list):
        return [mask_payload(item) for item in value]
    if isinstance(value, tuple):
        return tuple(mask_payload(item) for item in value)
    if isinstance(value, dict):
        return {key: mask_payload(item) for key, item in value.items()}
    return value


def _collect_matches(pattern: str, text: str, flags: int = re.IGNORECASE) -> list[str]:
    return [match.group(0) for match in re.finditer(pattern, text, flags=flags)]


def _replace_values(text: str, values: list[str], label: str, mapping: dict[str, list[str]]) -> tuple[str, int]:
    unique_values = sorted({value.strip() for value in values if value and value.strip()}, key=len, reverse=True)
    count = 0
    for value in unique_values:
        replacement = _mask_value(label, value)
        text, replacements = re.subn(re.escape(value), replacement, text)
        if replacements:
            mapping.setdefault(label, []).append(value)
            count += replacements
    return text, count


def _mask_value(label: str, value: str) -> str:
    if label == "EMAIL" and "@" in value:
        local, domain = value.split("@", 1)
        domain_parts = domain.split(".")
        if len(domain_parts) > 1:
            masked_domain = ".".join([_mask_word(part) for part in domain_parts[:-1]] + [domain_parts[-1]])
        else:
            masked_domain = _mask_word(domain)
        masked = f"{_mask_word(local)}@{masked_domain}"
    elif label in {"IBAN", "CREDIT_CARD"}:
        masked = _mask_alnum_token(value)
    elif label == "PHONE":
        masked = _mask_phone(value)
    elif label == "ID":
        masked = _mask_labeled_identifier(value)
    else:
        masked = _mask_words(value)
    return f"[{label}:{masked}]"


def _mask_word(value: str) -> str:
    if len(value) <= 2:
        return value[0] + "..." if value else value
    if len(value) <= 4:
        return value[0] + "..." + value[-1]
    keep = 2 if len(value) >= 6 else 1
    return value[:keep] + "..." + value[-keep:]


def _mask_words(value: str) -> str:
    return re.sub(r"[A-Za-zÀ-ÿ0-9]+", lambda match: _mask_word(match.group(0)), value)


def _mask_labeled_identifier(value: str) -> str:
    match = re.match(r"^(.{0,48}?)([A-Z0-9][A-Z0-9./-]{4,})$", value)
    if match and re.search(r"[A-Za-zÀ-ÿ]", match.group(1)):
        prefix, identifier = match.groups()
        return prefix + _mask_words(identifier)
    return _mask_compact_identifier(value)


def _mask_compact_identifier(value: str) -> str:
    sensitive_chars = [char for char in value if char.isalnum()]
    keep_start = min(2, len(sensitive_chars))
    keep_end = min(2, max(len(sensitive_chars) - keep_start, 0))
    seen = 0
    result = []
    hidden_started = False
    for char in value:
        if not char.isalnum():
            result.append(char)
            continue
        seen += 1
        if seen <= keep_start or seen > len(sensitive_chars) - keep_end:
            result.append(char)
        elif not hidden_started:
            result.append("...")
            hidden_started = True
    return "".join(result)


def _mask_alnum_token(value: str) -> str:
    compact = "".join(char for char in value if char.isalnum())
    if len(compact) <= 4:
        return _mask_word(compact)
    return compact[:2] + "..." + compact[-2:]


def _mask_phone(value: str) -> str:
    digits = "".join(char for char in value if char.isdigit())
    if len(digits) <= 4:
        return _mask_word(digits)
    prefix = "+" if value.strip().startswith("+") else ""
    return prefix + digits[:2] + "..." + digits[-2:]


def _name_candidates(text: str) -> list[str]:
    candidates = [
        match.group(1)
        for match in re.finditer(NAME_PREFIX_RE, text)
        if _looks_like_person_name(match.group(1))
    ]
    candidates.extend(
        match.group(1)
        for match in re.finditer(SIGNATURE_NAME_RE, text, re.MULTILINE)
        if _looks_like_person_name(match.group(1))
    )
    candidates.extend(
        match.group(1)
        for match in re.finditer(SENDER_NAME_RE, text)
        if _looks_like_person_name(match.group(1))
    )
    candidates.extend(
        match.group(1)
        for match in re.finditer(SENDER_BLOCK_RE, text)
        if _looks_like_person_name(match.group(1))
    )
    candidates.extend(_spacy_person_names(text))
    return [candidate for candidate in candidates if _looks_like_person_name(candidate)]


def _spacy_person_names(text: str) -> list[str]:
    nlp = _spacy_model()
    if nlp is None:
        return []
    try:
        doc = nlp(text[:20000])
    except Exception:
        return []
    return [ent.text.strip() for ent in doc.ents if ent.label_.upper() in {"PER", "PERSON"}]


def _looks_like_person_name(value: str) -> bool:
    if "\n" in value or "\r" in value:
        return False
    words = re.findall(r"[A-Za-zÀ-ÿ'’\-]{2,}", value)
    if len(words) < 2 or len(words) > 4:
        return False
    normalized = [word.lower().strip("'’-.") for word in words]
    if any(word in NAME_STOP_WORDS for word in normalized):
        return False
    return all(word[:1].isupper() for word in words)


def _looks_like_credit_card(value: str) -> bool:
    digits = re.sub(r"\D", "", value)
    if len(digits) < 13 or len(digits) > 19:
        return False
    total = 0
    reverse_digits = digits[::-1]
    for index, char in enumerate(reverse_digits):
        number = int(char)
        if index % 2 == 1:
            number *= 2
            if number > 9:
                number -= 9
        total += number
    return total % 10 == 0
