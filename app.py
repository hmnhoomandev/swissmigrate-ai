import streamlit as st

from modules.canton_navigator import render_canton_navigator
from modules.first_365_guide import render_first_365_guide
from modules.language_selection import render_language_gate
from modules.letter_helper import render_letter_helper
from modules.user_profile import render_profile_gate, render_profile_summary
from services.storage_service import get_recent_interactions
from ui.styles import load_custom_css
from utils.translations import t


st.set_page_config(
    page_title="SwissMigrate AI",
    page_icon="SM",
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

with st.sidebar:
    st.markdown("<div class='brand-mark'>SM</div>", unsafe_allow_html=True)
    st.markdown(f"### {t('app_name')}")
    st.caption(t("app_tagline"))
    st.divider()
    page = st.radio(
        t("navigation"),
        [
            t("dashboard"),
            t("letter_helper"),
            t("first_365"),
            t("canton_navigator"),
            t("history"),
            t("settings"),
        ],
        label_visibility="collapsed",
    )
    st.divider()
    render_profile_summary(compact=True)

st.title(t("app_name"))
st.caption(t("app_tagline"))

if page == t("dashboard"):
    render_profile_summary(compact=False)
    st.subheader(t("today_focus"))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**{t('letter_helper')}**")
        st.write(t("letter_helper_desc"))
    with col2:
        st.markdown(f"**{t('first_365')}**")
        st.write(t("first_365_desc"))
    with col3:
        st.markdown(f"**{t('canton_navigator')}**")
        st.write(t("navigator_desc"))
    st.info(t("safety_notice"))

elif page == t("letter_helper"):
    render_letter_helper()

elif page == t("first_365"):
    render_first_365_guide()

elif page == t("canton_navigator"):
    render_canton_navigator()

elif page == t("history"):
    st.subheader(t("history"))
    rows = get_recent_interactions(limit=20)
    if not rows:
        st.info(t("no_history"))
    else:
        for row in rows:
            with st.expander(f"{row.get('created_at', '')} - {row.get('module', '')}"):
                st.write(row.get("summary", ""))
                st.caption(row.get("metadata", ""))

elif page == t("settings"):
    st.subheader(t("settings"))
    render_profile_gate(update_mode=True)
