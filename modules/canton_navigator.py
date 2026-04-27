import streamlit as st

from services.llm_service import answer_with_context
from services.rag_service import retrieve_context
from services.safety_service import detect_emergency, safety_banner
from services.security_service import mask_pii
from services.storage_service import save_interaction
from ui.components import render_page_hero
from utils.translations import current_language_name, t


def render_canton_navigator() -> None:
    render_page_hero(t("canton_navigator"), t("navigator_desc"), t("canton_navigator"), st.session_state["canton_code"])

    st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
    question = st.text_area(t("ask_question"), placeholder=t("question_placeholder"), height=140)
    ask_clicked = st.button(t("ask"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if ask_clicked:
        if not question.strip():
            st.warning(t("ask_question"))
            return

        if detect_emergency(question):
            st.error(safety_banner())

        masked = mask_pii(question)
        profile = {
            "language": current_language_name(),
            "canton_code": st.session_state["canton_code"],
            "canton_name": st.session_state["canton_name"],
            "user_type": st.session_state["user_type"],
        }
        contexts = retrieve_context(masked.masked_text, profile["canton_code"], profile["user_type"])
        with st.spinner(t("ask")):
            result = answer_with_context(masked.masked_text, profile, contexts, current_language_name())

        save_interaction("canton_navigator", result.get("answer", ""), {"canton": profile["canton_code"]})
        if result.get("service_warning"):
            st.warning(result["service_warning"])
        if result.get("confidence") == "low":
            st.warning(t("low_confidence"))

        st.write(result.get("answer", ""))
        for step in result.get("steps", []):
            st.checkbox(str(step), value=False)

        services = result.get("services", [])
        if services:
            st.markdown(f"**{t('canton_navigator')}**")
            for service in services:
                st.write(service if isinstance(service, str) else service.get("name", service))

        st.markdown(f"**{t('sources')}**")
        source_items = result.get("sources") or [context.get("source", context) for context in contexts]
        for source in source_items:
            if isinstance(source, dict):
                st.link_button(source.get("title", "Source"), source.get("url", "https://www.ch.ch"))
            else:
                st.write(source)
