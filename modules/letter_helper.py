import streamlit as st

from services.llm_service import analyze_letter
from services.ocr_service import extract_text_from_upload
from services.security_service import mask_pii
from services.storage_service import save_interaction
from ui.components import render_page_hero
from utils.translations import current_language_name, t


def render_letter_helper() -> None:
    render_page_hero(t("letter_helper"), t("letter_helper_desc"), t("letter_helper"), st.session_state["canton_code"])

    left, right = st.columns([1.05, 0.95], gap="large")
    with left:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        consent = st.checkbox(t("upload_consent"))
        uploaded_file = st.file_uploader(t("upload_file"), type=["pdf", "png", "jpg", "jpeg"])
        pasted_text = st.text_area(t("paste_text"), height=220)
        analyze_clicked = st.button(t("analyze"), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            f"""
            <div class="soft-card">
                <h3>{t("privacy_first")}</h3>
                <p class="hero-copy">{t("privacy_first_desc")}</p>
                <p class="hero-copy">{t("safety_notice")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if analyze_clicked:
        if not consent:
            st.warning(t("missing_consent"))
            return

        extracted_text, warnings = extract_text_from_upload(uploaded_file)
        for warning in warnings:
            st.warning(warning)

        source_text = "\n\n".join(part for part in [extracted_text, pasted_text] if part.strip())
        if not source_text.strip():
            st.warning(t("missing_letter"))
            return

        masked = mask_pii(source_text)
        with st.spinner(t("analysis_result")):
            result = analyze_letter(masked.masked_text, current_language_name())

        save_interaction(
            "letter_helper",
            result.get("simple_explanation", ""),
            {"pii_counts": masked.counts, "urgency": result.get("urgency", "")},
        )

        st.markdown("")
        st.subheader(t("analysis_result"))
        if result.get("service_warning"):
            st.warning(result["service_warning"])
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**{t('simple_explanation')}**")
            st.write(result.get("simple_explanation", ""))
        with col2:
            st.metric(t("urgency"), result.get("urgency", ""))
            st.caption(f"{t('deadline')}: {result.get('deadline', '')}")

        st.markdown(f"**{t('actions')}**")
        for item in result.get("actions", []):
            st.checkbox(str(item), value=False)

        st.markdown(f"**{t('reply')}**")
        st.text_area(t("reply"), result.get("suggested_reply", ""), height=180, label_visibility="collapsed")

        with st.expander(t("masked_text")):
            st.code(masked.masked_text[:8000])
