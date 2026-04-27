import streamlit as st

from modules.canton_navigator import render_canton_navigator
from modules.first_365_guide import render_first_365_guide
from modules.language_selection import render_language_gate
from modules.letter_helper import render_letter_helper
from modules.user_profile import render_profile_gate, render_profile_summary
from services.storage_service import get_recent_interactions
from ui.components import PAGE_KEYS, page_label, render_brand, render_page_hero, render_service_shell, set_page
from ui.styles import load_custom_css
from utils.translations import t


st.set_page_config(
    page_title="SwissMigrate AI",
    page_icon="🇨🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_custom_css()

if "language" not in st.session_state:
    render_language_gate()
    st.stop()

if "profile_complete" not in st.session_state:
    render_profile_gate()
    st.stop()

if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "dashboard"

with st.sidebar:
    render_brand(compact=True)
    st.divider()
    selected_page = st.radio(
        t("navigation"),
        PAGE_KEYS,
        index=PAGE_KEYS.index(st.session_state["nav_page"]),
        format_func=page_label,
        label_visibility="collapsed",
    )
    if selected_page != st.session_state["nav_page"]:
        set_page(selected_page)
        st.rerun()
    st.divider()
    render_profile_summary(compact=True)

page = st.session_state["nav_page"]

if page == "dashboard":
    render_page_hero(t("today_focus"), t("dashboard_intro"), t("dashboard"), st.session_state["canton_code"])
    render_profile_summary(compact=False)

    services = [
        ("letter_helper", "✉", t("letter_helper"), t("letter_helper_desc"), t("open_letter_helper")),
        ("first_365", "365", t("first_365"), t("first_365_desc"), t("open_first_365")),
        ("canton_navigator", "⌖", t("canton_navigator"), t("navigator_desc"), t("open_canton_navigator")),
    ]
    cols = st.columns(3)
    for col, (page_key, icon, title, description, button_label) in zip(cols, services):
        with col:
            render_service_shell(icon, title, description)
            if st.button(button_label, key=f"open-{page_key}", use_container_width=True):
                set_page(page_key)
                st.rerun()

    st.markdown("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='stat-card'><b>{t('privacy_first')}</b><br>{t('privacy_first_desc')}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-card'><b>{t('source_grounded')}</b><br>{t('source_grounded_desc')}</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card'><b>{t('human_friendly')}</b><br>{t('human_friendly_desc')}</div>", unsafe_allow_html=True)
    st.info(t("safety_notice"))

elif page == "letter_helper":
    render_letter_helper()

elif page == "first_365":
    render_first_365_guide()

elif page == "canton_navigator":
    render_canton_navigator()

elif page == "history":
    render_page_hero(t("history"), t("history_intro"), t("history"), st.session_state["canton_code"])
    rows = get_recent_interactions(limit=20)
    if not rows:
        st.info(t("no_history"))
    else:
        for row in rows:
            with st.expander(f"{row.get('created_at', '')} - {row.get('module', '')}"):
                st.write(row.get("summary", ""))
                st.caption(row.get("metadata", ""))

elif page == "settings":
    render_page_hero(t("settings"), t("settings_intro"), t("settings"), st.session_state["canton_code"])
    render_profile_gate(update_mode=True)
