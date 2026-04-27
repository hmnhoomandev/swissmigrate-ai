import streamlit as st

from ui.brand import brand_image
from ui.components import render_brand
from utils.constants import LANGUAGES
from utils.translations import t


LANGUAGE_DISPLAY = {
    "Persian": "\u0641\u0627\u0631\u0633\u06cc",
    "English": "English",
    "French": "Fran\u00e7ais",
    "Arabic": "\u0627\u0644\u0639\u0631\u0628\u064a\u0629",
    "Turkish": "T\u00fcrk\u00e7e",
    "Spanish": "Espa\u00f1ol",
    "Chinese": "\u4e2d\u6587",
    "Ukrainian": "\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430",
}

LANGUAGE_ORDER = [
    "Persian",
    "English",
    "French",
    "Arabic",
    "Turkish",
    "Spanish",
    "Chinese",
    "Ukrainian",
]


def render_language_gate() -> None:
    hero_image = brand_image("hero-banner.png", "SwissMigrate AI guidance banner", "language-banner-img")
    languages = {language["english"]: language for language in LANGUAGES}
    ordered_options = [name for name in LANGUAGE_ORDER if name in languages]

    st.markdown("<main class='language-gate'>", unsafe_allow_html=True)
    render_brand()
    st.markdown(
        f"""
        <section class="language-landing">
            <div class="language-copy">
                <div class="language-hero__badge">Your AI guide for life in Switzerland</div>
                <h1 class="language-hero__title">Settle in Switzerland.</h1>
                <p class="language-hero__copy">
                    Understand official letters, local services, healthcare, housing, work, and everyday steps
                    with calm guidance in your own language.
                </p>
                <div class="language-benefits" aria-label="Key benefits">
                    <span>Ask in your language</span>
                    <span>Get help with documents</span>
                    <span>Navigate with confidence</span>
                </div>
            </div>
            <div class="language-visual" aria-hidden="true">
                {hero_image}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <section class="language-selector-card">
            <div class="language-selector-heading">
                <span>Choose your language to get started</span>
                <small>The whole experience will adapt to you.</small>
            </div>
        """,
        unsafe_allow_html=True,
    )
    selected = st.radio(
        t("choose_language"),
        ordered_options,
        index=ordered_options.index("English"),
        label_visibility="collapsed",
        format_func=lambda name: LANGUAGE_DISPLAY.get(name, name),
    )
    st.markdown("</section>", unsafe_allow_html=True)

    _, action_col, _ = st.columns([1.25, 0.7, 1.25])
    with action_col:
        if st.button(t("continue"), use_container_width=True):
            st.session_state["language"] = languages[selected]["code"]
            st.rerun()

    st.markdown("</main>", unsafe_allow_html=True)
