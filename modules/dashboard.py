import streamlit as st

from utils.translations import t


def show_dashboard_placeholder() -> None:
    st.subheader(t("dashboard"))
    st.write(t("app_tagline"))
