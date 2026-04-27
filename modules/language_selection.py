import streamlit as st

from ui.components import render_brand
from utils.constants import LANGUAGES
from utils.translations import t


def render_language_gate() -> None:
    st.markdown("<div class='center-shell'>", unsafe_allow_html=True)
    render_brand()
    st.markdown(
        """
        <h1 class="hero-title">Choose the language that feels like home.</h1>
        <p class="hero-copy">SwissMigrate AI will keep the whole experience in your selected language, including AI answers.</p>
        """,
        unsafe_allow_html=True,
    )

    options = {language["name"]: language for language in LANGUAGES}
    selected = st.radio(
        t("choose_language"),
        list(options.keys()),
        horizontal=True,
    )

    if st.button(t("continue"), use_container_width=True):
        st.session_state["language"] = options[selected]["code"]
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
