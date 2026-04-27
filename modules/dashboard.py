import streamlit as st

from utils.translations import t
from modules.letter_helper import show_letter_helper
from modules.first_365_guide import show_first_365_guide


LANGUAGES = [
    "Persian",
    "Arabic",
    "Turkish",
    "Ukrainian",
    "Chinese",
    "English",
    "Spanish",
    "French",
]


def show_sidebar():
    st.sidebar.markdown("## 🧭 FirstStep AI")
    st.sidebar.markdown("**Understand. Navigate. Belong.**")
    st.sidebar.markdown("---")

    selected_module = st.sidebar.radio(
        t("main_menu"),
        [
            t("letter_helper"),
            t("first_365"),
            t("canton_nav"),
            t("history"),
            t("saved"),
            t("settings"),
        ]
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        f"""
        <div class="privacy-box">
            🔒 {t("privacy_message")}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("")

    if st.sidebar.button(t("back"), use_container_width=True):
        st.session_state["page"] = "language"
        st.rerun()

    return selected_module


def show_header():
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f'<div class="main-title">{t("hello")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="subtitle">{t("how_help")}</div>', unsafe_allow_html=True)

    with col2:
        current_language = st.session_state.get("language", "English")

        language = st.selectbox(
            t("output_language"),
            LANGUAGES,
            index=LANGUAGES.index(current_language),
            label_visibility="collapsed"
        )

        if language != current_language:
            st.session_state["language"] = language
            st.rerun()


def show_footer_cards():
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    cards = [
        ("🛡️", t("footer_clarity_title"), t("footer_clarity_text")),
        ("🧭", t("footer_navigate_title"), t("footer_navigate_text")),
        ("🤝", t("footer_support_title"), t("footer_support_text")),
        ("🏠", t("footer_home_title"), t("footer_home_text")),
    ]

    for col, card in zip([col1, col2, col3, col4], cards):
        icon, title, text = card
        with col:
            st.markdown(
                f"""
                <div class="module-card">
                    <div class="module-icon">{icon}</div>
                    <div class="module-title">{title}</div>
                    <div class="module-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


def show_canton_navigator_placeholder():
    st.markdown(
        f"""
        <div class="card">
            <div class="module-icon">📍</div>
            <div class="module-title">{t("canton_nav")}</div>
            <div class="module-text">{t("navigator_desc")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_simple_placeholder(title_icon, title):
    st.markdown(
        f"""
        <div class="card">
            <div class="module-icon">{title_icon}</div>
            <div class="module-title">{title}</div>
            <div class="module-text">{t("coming_soon")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_dashboard():
    selected_module = show_sidebar()
    show_header()

    if selected_module == t("letter_helper"):
        show_letter_helper()

    elif selected_module == t("first_365"):
        show_first_365_guide()

    elif selected_module == t("canton_nav"):
        show_canton_navigator_placeholder()

    elif selected_module == t("history"):
        show_simple_placeholder("🕘", t("history"))

    elif selected_module == t("saved"):
        show_simple_placeholder("🔖", t("saved"))

    elif selected_module == t("settings"):
        show_simple_placeholder("⚙️", t("settings"))

    show_footer_cards()