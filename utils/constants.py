LANGUAGES = [
    {"code": "fa", "name": "فارسی", "english": "Persian", "rtl": True},
    {"code": "ar", "name": "العربية", "english": "Arabic", "rtl": True},
    {"code": "tr", "name": "Türkçe", "english": "Turkish", "rtl": False},
    {"code": "uk", "name": "Українська", "english": "Ukrainian", "rtl": False},
    {"code": "zh", "name": "中文", "english": "Chinese", "rtl": False},
    {"code": "en", "name": "English", "english": "English", "rtl": False},
    {"code": "es", "name": "Español", "english": "Spanish", "rtl": False},
    {"code": "fr", "name": "Français", "english": "French", "rtl": False},
]

LANGUAGE_BY_CODE = {language["code"]: language for language in LANGUAGES}

SWISS_CANTONS = [
    {"code": "AG", "name": "Aargau"},
    {"code": "AI", "name": "Appenzell Innerrhoden"},
    {"code": "AR", "name": "Appenzell Ausserrhoden"},
    {"code": "BE", "name": "Bern"},
    {"code": "BL", "name": "Basel-Landschaft"},
    {"code": "BS", "name": "Basel-Stadt"},
    {"code": "FR", "name": "Fribourg"},
    {"code": "GE", "name": "Geneva"},
    {"code": "GL", "name": "Glarus"},
    {"code": "GR", "name": "Graubünden"},
    {"code": "JU", "name": "Jura"},
    {"code": "LU", "name": "Lucerne"},
    {"code": "NE", "name": "Neuchâtel"},
    {"code": "NW", "name": "Nidwalden"},
    {"code": "OW", "name": "Obwalden"},
    {"code": "SG", "name": "St. Gallen"},
    {"code": "SH", "name": "Schaffhausen"},
    {"code": "SO", "name": "Solothurn"},
    {"code": "SZ", "name": "Schwyz"},
    {"code": "TG", "name": "Thurgau"},
    {"code": "TI", "name": "Ticino"},
    {"code": "UR", "name": "Uri"},
    {"code": "VD", "name": "Vaud"},
    {"code": "VS", "name": "Valais"},
    {"code": "ZG", "name": "Zug"},
    {"code": "ZH", "name": "Zürich"},
]

USER_TYPES = ["asylum_seeker", "refugee", "migrant", "worker", "student"]

FIRST_365_GUIDE_TOPICS = [
    "healthcare_insurance",
    "housing",
    "legal_permits",
    "employment",
    "education",
    "language_learning",
    "financial_support",
    "public_transport",
    "social_integration",
    "mental_health",
    "registration_admin",
    "family_reunification",
    "digital_tools",
]

FIRST_365_TOPICS = FIRST_365_GUIDE_TOPICS + [
    "appointments",
    "letters_documents",
    "leisure",
]

EMERGENCY_CONTACTS = {
    "medical": "144",
    "police": "117",
    "fire": "118",
    "poison": "145",
    "mental_health": "143",
}

DOCUMENT_TYPES = [
    "decision",
    "request",
    "summons",
    "notice",
    "form",
    "legal_letter",
    "appeal_response",
    "unknown"
]

LOW_CONFIDENCE_THRESHOLD = 0.70
