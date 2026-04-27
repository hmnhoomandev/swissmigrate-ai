from pathlib import Path
from urllib.parse import quote


ASSET_CANTON_DIR = Path(__file__).resolve().parents[1] / "assets" / "cantons"

CANTON_FLAGS = {
    "AG": {"name": "Aargau", "file": "Wappen Aargau matt.svg"},
    "AI": {"name": "Appenzell Innerrhoden", "file": "Wappen Appenzell Innerrhoden matt.svg"},
    "AR": {"name": "Appenzell Ausserrhoden", "file": "Wappen Appenzell Ausserrhoden matt.svg"},
    "BE": {"name": "Bern", "file": "Wappen Bern matt.svg"},
    "BL": {"name": "Basel-Landschaft", "file": "Wappen Basel-Landschaft matt.svg"},
    "BS": {"name": "Basel-Stadt", "file": "Wappen Basel-Stadt matt.svg"},
    "FR": {"name": "Fribourg", "file": "Wappen Freiburg matt.svg"},
    "GE": {"name": "Geneva", "file": "Wappen Genf matt.svg"},
    "GL": {"name": "Glarus", "file": "Wappen Glarus matt.svg"},
    "GR": {"name": "Graubünden", "file": "Wappen Graubünden matt.svg"},
    "JU": {"name": "Jura", "file": "Wappen Jura matt.svg"},
    "LU": {"name": "Lucerne", "file": "Wappen Luzern matt.svg"},
    "NE": {"name": "Neuchâtel", "file": "Wappen Neuenburg matt.svg"},
    "NW": {"name": "Nidwalden", "file": "Wappen Nidwalden matt.svg"},
    "OW": {"name": "Obwalden", "file": "Wappen Obwalden matt.svg"},
    "SG": {"name": "St. Gallen", "file": "Wappen St. Gallen matt.svg"},
    "SH": {"name": "Schaffhausen", "file": "Wappen Schaffhausen matt.svg"},
    "SO": {"name": "Solothurn", "file": "Wappen Solothurn matt.svg"},
    "SZ": {"name": "Schwyz", "file": "Wappen Schwyz matt.svg"},
    "TG": {"name": "Thurgau", "file": "Wappen Thurgau matt.svg"},
    "TI": {"name": "Ticino", "file": "Wappen Tessin matt.svg"},
    "UR": {"name": "Uri", "file": "Wappen Uri matt.svg"},
    "VD": {"name": "Vaud", "file": "Wappen Waadt matt.svg"},
    "VS": {"name": "Valais", "file": "Wappen Wallis matt.svg"},
    "ZG": {"name": "Zug", "file": "Wappen Zug matt.svg"},
    "ZH": {"name": "Zürich", "file": "Wappen Zürich matt.svg"},
}


def canton_metadata(code: str) -> dict[str, str]:
    normalized = code.upper()
    return CANTON_FLAGS.get(normalized, {"name": normalized, "file": ""})


def canton_asset_path(code: str) -> Path:
    return ASSET_CANTON_DIR / f"{code.lower()}.svg"


def canton_remote_uri(code: str) -> str:
    file_name = canton_metadata(code)["file"]
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(file_name)}"
