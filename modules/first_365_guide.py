import streamlit as st

from services.first_365_content_service import load_first_365_content, topic_options
from services.storage_service import save_interaction
from ui.components import render_page_hero, render_profile_badge
from utils.translations import t


def render_first_365_guide() -> None:
    render_page_hero(t("first_365"), t("first_365_desc"), t("first_365"), st.session_state["canton_code"])

    profile = {
        "canton_code": st.session_state["canton_code"],
        "canton_name": st.session_state["canton_name"],
        "user_type": st.session_state["user_type"],
    }

    st.markdown("<div class='first365-shell'>", unsafe_allow_html=True)
    left, right = st.columns([0.95, 1.35], gap="large")
    with left:
        st.markdown(f"<div class='first365-panel-title'>{t('first365_profile_context')}</div>", unsafe_allow_html=True)
        render_profile_badge(profile["canton_name"], profile["canton_code"], profile["user_type"])
        st.markdown(
            f"<p class='first365-muted'>{t('first365_profile_hint')}</p>",
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(f"<div class='first365-panel-title'>{t('first365_choose_topics')}</div>", unsafe_allow_html=True)
        selected_topics = _render_topic_picker()
        submit = st.button(t("show_selected_guidance"), type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if submit:
        if not selected_topics:
            st.warning(t("first365_select_at_least_one"))
            return
        _render_selected_guidance(profile, selected_topics)


def _render_topic_picker() -> list[str]:
    options = topic_options()
    selected_topics: list[str] = []
    columns = st.columns(2)
    for index, topic in enumerate(options):
        with columns[index % 2]:
            checked = st.checkbox(
                topic["label"],
                value=topic["id"] in {"registration_admin", "legal_permits", "healthcare_insurance", "housing"},
                key=f"first365-topic-{topic['id']}",
                help=topic["timeframe"],
            )
            if checked:
                selected_topics.append(topic["id"])
    return selected_topics


def _render_selected_guidance(profile: dict[str, str], selected_topics: list[str]) -> None:
    items = load_first_365_content(profile["canton_code"], profile["user_type"], selected_topics)
    save_interaction(
        "first_365",
        f"{profile['canton_code']} / {profile['user_type']} / {', '.join(selected_topics)}",
        {"canton": profile["canton_code"], "user_type": profile["user_type"], "topics": selected_topics},
    )

    st.markdown(
        f"""
        <div class="first365-result-intro">
            <span>{len(items)}</span>
            <div>
                <b>{t('first365_result_title')}</b>
                <p>{profile['canton_name']} - {t(profile['user_type'])}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for item in items:
        _render_guidance_item(item)


def _render_guidance_item(item: dict) -> None:
    missing_class = " first365-topic-card--missing" if item.get("missing_content") else ""
    st.markdown(
        f"""
        <article class="first365-topic-card{missing_class}">
            <div class="first365-topic-card__head">
                <span>{item.get('priority', '')}</span>
                <div>
                    <h3>{item.get('title', '')}</h3>
                    <p>{t('timeframe')}: {item.get('timeframe', '')}</p>
                </div>
            </div>
            <p class="first365-topic-card__summary">{item.get('summary', '')}</p>
            <div class="first365-file-path">{t('editable_file')}: {item.get('source_file', '')}</div>
        </article>
        """,
        unsafe_allow_html=True,
    )

    actions = item.get("actions", [])
    if actions:
        with st.expander(t("actions"), expanded=True):
            for index, action in enumerate(actions):
                st.checkbox(str(action), key=f"{item.get('topic')}-action-{index}-{hash(str(action))}")

    services = item.get("services", [])
    if services:
        with st.expander(t("local_services"), expanded=False):
            for service in services:
                label = service.get("name") or service.get("title") or "Service"
                description = service.get("description", "")
                contact = service.get("contact") or service.get("url", "")
                st.markdown(f"**{label}**")
                if description:
                    st.caption(description)
                if contact:
                    st.link_button(t("open_source"), contact)

    sources = item.get("sources", [])
    if sources:
        with st.expander(t("sources"), expanded=False):
            for source in sources:
                title = source.get("title") or source.get("name") or "Source"
                url = source.get("url") or source.get("contact") or "https://www.ch.ch"
                st.link_button(title, url)
