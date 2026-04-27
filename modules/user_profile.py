import streamlit as st

from services.storage_service import save_profile
from ui.components import render_page_hero, render_profile_chip
from utils.constants import SWISS_CANTONS, USER_TYPES
from utils.translations import t


def _current_profile() -> dict[str, str]:
    return {
        "language": st.session_state.get("language", "en"),
        "canton_code": st.session_state.get("canton_code", "ZH"),
        "canton_name": st.session_state.get("canton_name", "Zürich"),
        "user_type": st.session_state.get("user_type", "migrant"),
    }


def render_profile_gate(update_mode: bool = False) -> None:
    if not update_mode:
        render_page_hero(t("profile_title"), t("profile_help"), t("app_name"))
    else:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)

    canton_labels = [f"{item['name']} ({item['code']})" for item in SWISS_CANTONS]
    current_label = f"{st.session_state.get('canton_name', 'Zürich')} ({st.session_state.get('canton_code', 'ZH')})"
    canton = st.selectbox(
        t("select_canton"),
        canton_labels,
        index=canton_labels.index(current_label) if current_label in canton_labels else 25,
    )
    code = canton.split("(")[-1].replace(")", "")
    name = canton.rsplit("(", 1)[0].strip()
    render_profile_chip(name, code, st.session_state.get("user_type", "migrant"))

    user_type = st.selectbox(
        t("select_user_type"),
        USER_TYPES,
        format_func=lambda value: t(value),
        index=USER_TYPES.index(st.session_state.get("user_type", "migrant")),
    )

    if st.button(t("save_profile"), use_container_width=True):
        st.session_state["canton_code"] = code
        st.session_state["canton_name"] = name
        st.session_state["user_type"] = user_type
        st.session_state["profile_complete"] = True
        save_profile(_current_profile())
        if update_mode:
            st.success(t("saved"))
        else:
            st.rerun()

    if update_mode:
        st.markdown("</div>", unsafe_allow_html=True)


def render_profile_summary(compact: bool) -> None:
    profile = _current_profile()
    if compact:
        render_profile_chip(profile["canton_name"], profile["canton_code"], profile["user_type"])
    else:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        render_profile_chip(profile["canton_name"], profile["canton_code"], profile["user_type"])
        st.markdown("</div>", unsafe_allow_html=True)
