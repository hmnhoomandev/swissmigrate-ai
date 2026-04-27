import base64
from pathlib import Path

from ui.cantons import canton_asset_path, canton_metadata, canton_remote_uri


ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "flags"
CANTON_DIR = ASSET_DIR / "cantons"


def _svg_data_uri(svg: str) -> str:
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def _file_data_uri(path: Path) -> str | None:
    if not path.exists():
        return None
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def _placeholder_canton_svg(code: str, name: str) -> str:
    initials = code.upper()
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="{name} flag placeholder">
      <defs>
        <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
          <stop stop-color="#e11d48"/>
          <stop offset="0.55" stop-color="#dc2626"/>
          <stop offset="1" stop-color="#0f766e"/>
        </linearGradient>
      </defs>
      <rect width="64" height="64" rx="16" fill="#fff7ed"/>
      <path d="M12 8h40v22c0 14-8 23-20 28-12-5-20-14-20-28V8Z" fill="url(#g)"/>
      <path d="M28 18h8v10h10v8H36v10h-8V36H18v-8h10V18Z" fill="white"/>
      <text x="32" y="57" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="800" fill="#111827">{initials}</text>
    </svg>
    """


def swiss_flag_uri() -> str:
    return _file_data_uri(ASSET_DIR / "switzerland.svg") or _svg_data_uri(
        """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Swiss flag">
          <rect width="64" height="64" rx="14" fill="#dc2626"/>
          <path fill="#fff" d="M27 14h10v13h13v10H37v13H27V37H14V27h13z"/>
        </svg>
        """
    )


def canton_flag_uri(code: str) -> str:
    normalized = code.lower()
    metadata = canton_metadata(code)
    return (
        _file_data_uri(canton_asset_path(code))
        or _file_data_uri(CANTON_DIR / f"{normalized}.svg")
        or canton_remote_uri(code)
        or _svg_data_uri(_placeholder_canton_svg(code, metadata["name"]))
    )


def flag_img(uri: str, alt: str, size: int = 34) -> str:
    return f"<img src='{uri}' alt='{alt}' class='flag-img' style='width:{size}px;height:{size}px;' />"
