import streamlit as st

from ui.brand import brand_image
from ui.flags import canton_flag_uri, flag_img
from utils.translations import t


PAGE_KEYS = ["dashboard", "letter_helper", "first_365", "canton_navigator", "history", "settings"]

PAGE_ICONS = {
    "dashboard": "⌂",
    "letter_helper": "✉",
    "first_365": "365",
    "canton_navigator": "⌖",
    "history": "◴",
    "settings": "⚙",
}


def page_label(page_key: str) -> str:
    return f"{PAGE_ICONS.get(page_key, '•')}  {t(page_key)}"


def set_page(page_key: str) -> None:
    st.session_state["nav_page"] = page_key


def render_brand(compact: bool = False) -> None:
    size_class = "brand-row--compact" if compact else "brand-row--full"
    logo = brand_image("logo-icon.png", "SwissMigrate AI logo", "brand-logo-img")
    st.markdown(
        f"""
        <div class="brand-row {size_class}">
            <div class="brand-logo-frame">{logo}</div>
            <div>
                <p class="brand-title">{t("app_name")}</p>
                <p class="brand-caption">{t("app_tagline")}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_hero(title: str, copy: str, eyebrow: str | None = None, canton_code: str | None = None) -> None:
    logo = brand_image("logo-icon.png", "SwissMigrate AI logo", "hero-logo-img")
    canton = ""
    if canton_code:
        canton = flag_img(canton_flag_uri(canton_code), f"{canton_code} canton flag", 28)
    st.markdown(
        f"""
        <section class="hero-panel">
            <div class="hero-eyebrow">{logo}{canton}<span>{eyebrow or t("app_name")}</span></div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-copy">{copy}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_profile_badge(canton_name: str, canton_code: str, user_type: str) -> None:
    flag = flag_img(canton_flag_uri(canton_code), f"{canton_name} flag", 30)
    st.markdown(
        f"""
        <div class="profile-badge">
            <span class="profile-badge__flag">{flag}</span>
            <span class="profile-badge__content">
                <span class="profile-badge__place">{canton_name} ({canton_code})</span>
                <span class="profile-badge__type">{t(user_type)}</span>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_profile_chip(canton_name: str, canton_code: str, user_type: str) -> None:
    render_profile_badge(canton_name, canton_code, user_type)


def render_service_shell(icon: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="service-shell">
            <div class="service-shell__shine"></div>
            <div class="service-icon">{icon}</div>
            <div class="service-title">{title}</div>
            <div class="service-text">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
