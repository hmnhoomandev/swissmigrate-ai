import streamlit as st

from ui.components import render_brand
from utils.constants import LANGUAGES
from utils.translations import t


LANGUAGE_ACCENTS = {
    "Persian": "FA",
    "Arabic": "AR",
    "Turkish": "TR",
    "Ukrainian": "UK",
    "Chinese": "ZH",
    "English": "EN",
    "Spanish": "ES",
    "French": "FR",
}


def render_language_gate() -> None:
    st.markdown("<main class='language-gate'>", unsafe_allow_html=True)
    render_brand()
    st.markdown(
        """
        <section class="language-hero">
            <div class="language-hero__badge">Private, practical support for life in Switzerland</div>
            <h1 class="language-hero__title">Choose the language that feels like home.</h1>
            <p class="language-hero__copy">
                We will shape every screen and AI answer around the language you choose,
                so the next step feels calmer and easier to understand.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    options = {language["english"]: language for language in LANGUAGES}
    default_index = list(options.keys()).index("English")

    st.markdown("<section class='language-selector-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="language-selector-heading">
            <span>Select your language</span>
            <small>You can change this later in settings.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected = st.radio(
        t("choose_language"),
        list(options.keys()),
        index=default_index,
        label_visibility="collapsed",
        format_func=lambda name: f"{LANGUAGE_ACCENTS.get(name, name[:2].upper())}  {name}",
    )
    st.markdown("</section>", unsafe_allow_html=True)

    st.markdown("<div class='language-action'>", unsafe_allow_html=True)
    if st.button(t("continue"), use_container_width=False):
        st.session_state["language"] = options[selected]["code"]
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</main>", unsafe_allow_html=True)
