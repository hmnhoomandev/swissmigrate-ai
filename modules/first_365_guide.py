import streamlit as st

from services.llm_service import personalize_guide
from services.rag_service import build_first_365_checklist
from services.storage_service import save_interaction
from utils.translations import current_language_name, t


def render_first_365_guide() -> None:
    st.subheader(t("first_365"))
    st.write(t("first_365_desc"))

    profile = {
        "language": current_language_name(),
        "canton_code": st.session_state["canton_code"],
        "canton_name": st.session_state["canton_name"],
        "user_type": st.session_state["user_type"],
    }

    if st.button(t("generate_guide"), use_container_width=True):
        checklist = build_first_365_checklist(profile["canton_code"], profile["user_type"])
        with st.spinner(t("generate_guide")):
            guide = personalize_guide(profile, checklist, current_language_name())

        save_interaction("first_365", guide.get("note", ""), {"canton": profile["canton_code"]})
        if guide.get("service_warning"):
            st.warning(guide["service_warning"])
        st.info(guide.get("note", ""))

        for item in guide.get("items", []):
            with st.expander(f"{item.get('priority', '')}. {item.get('title', '')}", expanded=item.get("priority", 99) <= 4):
                st.caption(f"{t('timeframe')}: {item.get('timeframe', '')} | {t('priority')}: {item.get('priority', '')}")
                for action in item.get("actions", []):
                    st.checkbox(str(action), key=f"{item.get('topic')}-{action}")
                services = item.get("services", [])
                if services:
                    st.markdown(f"**{t('canton_navigator')}**")
                    for service in services:
                        st.write(f"{service.get('name')} - {service.get('contact', '')}")
                sources = item.get("sources", [])
                if sources:
                    st.markdown(f"**{t('sources')}**")
                    for source in sources:
                        st.link_button(source.get("title", "Source"), source.get("url", "https://www.ch.ch"))
