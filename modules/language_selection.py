import streamlit as st

from utils.constants import LANGUAGES
from utils.translations import t


def render_language_gate() -> None:
    st.markdown("<div class='center-shell'>", unsafe_allow_html=True)
    st.title("FirstStep AI Switzerland")
    st.caption("Choose your language. All UI and AI output will follow it.")

    options = {language["name"]: language for language in LANGUAGES}
    selected = st.radio(
        "Language",
        list(options.keys()),
        horizontal=True,
        label_visibility="collapsed",
    )

    if st.button(t("continue"), use_container_width=True):
        st.session_state["language"] = options[selected]["code"]
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
