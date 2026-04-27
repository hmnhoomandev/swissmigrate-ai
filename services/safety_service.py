EMERGENCY_TERMS = {
    "suicide",
    "kill myself",
    "violence",
    "bleeding",
    "deportation tomorrow",
    "homeless tonight",
    "domestic violence",
}


def detect_emergency(text: str) -> bool:
    normalized = (text or "").lower()
    return any(term in normalized for term in EMERGENCY_TERMS)


def safety_banner() -> str:
    return (
        "Emergency: call 144 for medical help, 117 for police, 118 for fire. "
        "For emotional crisis support in Switzerland, call 143."
    )
