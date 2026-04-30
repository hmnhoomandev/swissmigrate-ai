from html import escape

import streamlit as st

from services.llm_service import answer_with_context
from services.rag_service import load_canton_documents, retrieve_context
from services.safety_service import detect_emergency, safety_banner
from services.security_service import mask_pii
from services.storage_service import save_interaction
from ui.components import render_page_hero, render_profile_badge
from utils.translations import current_language_name, t


def render_canton_navigator() -> None:
    render_page_hero(t("canton_navigator"), t("navigator_desc"), t("canton_navigator"), st.session_state["canton_code"])

    profile = {
        "language": current_language_name(),
        "canton_code": st.session_state["canton_code"],
        "canton_name": st.session_state["canton_name"],
        "user_type": st.session_state["user_type"],
    }
    documents = load_canton_documents(profile["canton_code"], profile["user_type"])

    _render_navigator_intro(profile, documents)

    st.markdown("<div class='navigator-chat-shell'>", unsafe_allow_html=True)
    question = st.text_area(t("ask_question"), placeholder=t("question_placeholder"), height=132, key="navigator-question")
    selected_example = st.selectbox(
        "Quick prompts",
        _quick_questions(),
        index=None,
        placeholder="Try an example question",
        label_visibility="collapsed",
        key="navigator-quick-prompt",
    )
    if selected_example and not question.strip():
        question = selected_example
    ask_clicked = st.button(t("ask"), type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if ask_clicked:
        if not question.strip():
            st.warning(t("ask_question"))
            return

        if detect_emergency(question):
            st.error(safety_banner())

        masked = mask_pii(question)
        contexts = retrieve_context(masked.masked_text, profile["canton_code"], profile["user_type"])
        with st.spinner(t("ask")):
            result = answer_with_context(masked.masked_text, profile, contexts, current_language_name())

        save_interaction("canton_navigator", result.get("answer", ""), {"canton": profile["canton_code"]})
        if result.get("service_warning"):
            st.warning(result["service_warning"])
        if result.get("confidence") == "low":
            st.warning(t("low_confidence"))

        _render_answer(result, contexts)


def _render_navigator_intro(profile: dict[str, str], documents: list[dict]) -> None:
    source_files = sorted({document.get("source_file", "") for document in documents if document.get("source_file")})
    topics = sorted({document.get("topic", "general") for document in documents})

    st.markdown("<div class='navigator-command-center'>", unsafe_allow_html=True)
    left, mid, right = st.columns([1.05, 1.15, 0.95], gap="large")
    with left:
        render_profile_badge(profile["canton_name"], profile["canton_code"], profile["user_type"])
    with mid:
        st.markdown(
            f"""
            <div class="navigator-source-meter">
                <span>{len(source_files)}</span>
                <div>
                    <b>{t('navigator_source_library')}</b>
                    <p>{t('navigator_source_library_desc')}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"""
            <div class="navigator-source-meter navigator-source-meter--quiet">
                <span>{len(topics)}</span>
                <div>
                    <b>{t('navigator_topics_ready')}</b>
                    <p>{t('navigator_folder_hint')}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def _quick_questions() -> list[str]:
    return [
        "Where should I register my address?",
        "How can I find language courses?",
        "What should I do about health insurance?",
        "Where can I get help with permits?",
    ]


def _render_answer(result: dict, contexts: list[dict]) -> None:
    confidence = result.get("confidence", "medium")
    st.markdown(
        f"""
        <section class="navigator-answer-card">
            <div class="navigator-answer-card__top">
                <span>{escape(str(confidence)).upper()}</span>
                <b>{t('navigator_answer_from_sources')}</b>
            </div>
            <div class="navigator-answer-copy">{escape(str(result.get('answer', ''))).replace(chr(10), '<br>')}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    steps = result.get("steps", [])
    if steps:
        with st.expander(t("actions"), expanded=True):
            for index, step in enumerate(steps):
                st.checkbox(str(step), value=False, key=f"navigator-step-{index}-{hash(str(step))}")

    services = result.get("services", [])
    if services:
        st.markdown(f"<div class='navigator-section-title'>{t('local_services')}</div>", unsafe_allow_html=True)
        for service in services:
            if isinstance(service, str):
                st.write(service)
                continue
            label = service.get("name") or service.get("title") or "Service"
            description = service.get("description", "")
            contact = service.get("contact") or service.get("url", "")
            st.markdown(
                f"""
                <div class="navigator-service-card">
                    <b>{escape(str(label))}</b>
                    <p>{escape(str(description))}</p>
                    <small>{escape(str(contact))}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    _render_sources(result.get("sources") or [context.get("source", context) for context in contexts])


def _render_sources(source_items: list) -> None:
    st.markdown(f"<div class='navigator-section-title'>{t('sources')}</div>", unsafe_allow_html=True)
    for source in source_items:
        if not isinstance(source, dict):
            st.write(source)
            continue
        title = source.get("title") or source.get("name") or "Source"
        url = source.get("url") or source.get("contact") or ""
        description = source.get("description", "")
        st.markdown(
            f"""
            <div class="navigator-source-card">
                <b>{escape(str(title))}</b>
                <p>{escape(str(description))}</p>
                <code>{escape(str(url))}</code>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if str(url).startswith("http"):
            st.link_button(t("open_source"), url)
