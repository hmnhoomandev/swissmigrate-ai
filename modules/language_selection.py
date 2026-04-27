import streamlit as st

from ui.components import render_brand
from utils.constants import LANGUAGES
from utils.translations import t


LANGUAGE_DISPLAY = {
    "Persian": "فارسی",
    "Arabic": "العربية",
    "Turkish": "Türkçe",
    "Ukrainian": "Українська",
    "Chinese": "中文",
    "English": "English",
    "Spanish": "Español",
    "French": "Français",
}


def render_language_gate() -> None:
    st.markdown("<main class='language-gate'>", unsafe_allow_html=True)
    render_brand()
    st.markdown(
        """
        <section class="language-hero">
            <div class="language-hero__badge">Your AI guide for life in Switzerland</div>
            <h1 class="language-hero__title">Settle in Switzerland.</h1>
            <p class="language-hero__copy">
                Understand official letters, local services, healthcare, housing, work, and everyday steps
                with calm guidance in your own language.
            </p>
            <div class="language-benefits" aria-label="Key benefits">
                <span>Understand documents</span>
                <span>Find local next steps</span>
                <span>Ask safely in your language</span>
            </div>
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
            <span>Choose your language to get started</span>
            <small>The whole experience will adapt to you.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected = st.radio(
        t("choose_language"),
        list(options.keys()),
        index=default_index,
        label_visibility="collapsed",
        format_func=lambda name: LANGUAGE_DISPLAY.get(name, name),
    )
    st.markdown("</section>", unsafe_allow_html=True)

    st.markdown("<div class='language-action'>", unsafe_allow_html=True)
    if st.button(t("continue"), use_container_width=False):
        st.session_state["language"] = options[selected]["code"]
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</main>", unsafe_allow_html=True)
