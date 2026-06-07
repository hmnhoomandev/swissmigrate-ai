# regex_patterns.py
CASE_PATTERNS = [
    r"[A-Z]{2,5}-\d{4}-\d+",
    r"N°\s?\d+",
    r"Réf[:\s]+\S+",
    r"Reference[:\s]+\S+",
]

DATE_PATTERNS = [
    r"\d{2}\.\d{2}\.\d{4}",
    r"\d{1,2}/\d{1,2}/\d{4}",
    r"\d{4}-\d{2}-\d{2}",
]
