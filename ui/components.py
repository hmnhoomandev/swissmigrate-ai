import streamlit as st

from ui.flags import canton_flag_uri, flag_img, swiss_flag_uri
from utils.translations import t


PAGE_KEYS = ["dashboard", "letter_helper", "first_365", "canton_navigator", "history", "settings"]


def page_label(page_key: str) -> str:
    return t(page_key)


def set_page(page_key: str) -> None:
    st.session_state["nav_page"] = page_key


def render_brand(compact: bool = False) -> None:
    flag = flag_img(swiss_flag_uri(), "Swiss flag", 36 if compact else 42)
    st.markdown(
        f"""
        <div class="brand-row">
            {flag}
            <div>
                <p class="brand-title">{t("app_name")}</p>
                <p class="brand-caption">{t("app_tagline")}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_hero(title: str, copy: str, eyebrow: str | None = None, canton_code: str | None = None) -> None:
    flag = flag_img(swiss_flag_uri(), "Swiss flag", 28)
    canton = ""
    if canton_code:
        canton = flag_img(canton_flag_uri(canton_code), f"{canton_code} canton flag", 28)
    st.markdown(
        f"""
        <section class="hero-panel">
            <div class="hero-eyebrow">{flag}{canton}<span>{eyebrow or t("app_name")}</span></div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-copy">{copy}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_profile_chip(canton_name: str, canton_code: str, user_type: str) -> None:
    flag = flag_img(canton_flag_uri(canton_code), f"{canton_name} flag", 30)
    st.markdown(
        f"""
        <div class="profile-chip">
            {flag}
            <span>{canton_name} ({canton_code})</span>
            <span>•</span>
            <span>{t(user_type)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_service_shell(icon: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="service-shell">
            <div class="service-icon">{icon}</div>
            <div class="service-title">{title}</div>
            <div class="service-text">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
