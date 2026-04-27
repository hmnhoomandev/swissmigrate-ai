import base64
from pathlib import Path


BRAND_DIR = Path(__file__).resolve().parents[1] / "assets" / "brand"


def brand_asset_uri(filename: str) -> str:
    path = BRAND_DIR / filename
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def brand_image(filename: str, alt: str, class_name: str) -> str:
    return f"<img src='{brand_asset_uri(filename)}' alt='{alt}' class='{class_name}' />"
