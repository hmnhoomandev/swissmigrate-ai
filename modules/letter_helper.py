from html import escape

import streamlit as st

from services.llm_service import analyze_letter
from services.ocr_service import extract_text_from_upload
from services.security_service import mask_pii
from services.storage_service import ensure_user_id, save_interaction, save_letter_history
from ui.components import render_page_hero
from utils.translations import current_language_name, t


URGENCY_CLASS = {
    "VERY URGENT": "very-urgent",
    "URGENT": "urgent",
    "MEDIUM": "medium",
    "LOW": "low",
    "No clear deadline found": "none",
}


def _result_card(title: str, icon: str, body: str, class_name: str = "") -> None:
    st.markdown(
        f"""
        <div class="letter-result-card {class_name}">
            <div class="letter-card-kicker"><span>{icon}</span>{escape(title)}</div>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _summary_markup(summary: dict) -> str:
    fields = [
        ("What is the letter about?", summary.get("topic", "Not specified in the letter")),
        ("Sender", summary.get("sender", "Not specified in the letter")),
        ("Date", summary.get("date", "Not specified in the letter")),
        ("Recipient", summary.get("recipient", "Not specified in the letter")),
    ]
    rows = "".join(
        f"<div class='summary-row'><span>{escape(label)}</span><b>{escape(str(value or 'Not specified in the letter'))}</b></div>"
        for label, value in fields
    )
    short_summary = escape(str(summary.get("summary", "Not specified in the letter")))
    return f"{rows}<p class='letter-summary-copy'>{short_summary}</p>"


def _urgency_markup(urgency: dict) -> tuple[str, str]:
    level = str(urgency.get("level") or "No clear deadline found")
    days_left = str(urgency.get("days_left") or "Not specified in the letter")
    css_class = URGENCY_CLASS.get(level.upper(), URGENCY_CLASS.get(level, "none"))
    body = (
        f"<div class='urgency-badge urgency-badge--{css_class}'>{escape(level)}</div>"
        f"<div class='deadline-pill'>Days left: <b>{escape(days_left)}</b></div>"
    )
    return body, css_class


def _render_action_steps(steps: list) -> None:
    _result_card("Action Steps", "✓", "<p class='letter-summary-copy'>Clear next actions from the masked letter.</p>")
    for index, step in enumerate(steps or ["Not specified in the letter"], start=1):
        st.checkbox(str(step), value=False, key=f"letter-action-{index}")


def render_letter_helper() -> None:
    render_page_hero(t("letter_helper"), t("letter_helper_desc"), t("letter_helper"), st.session_state["canton_code"])
    ensure_user_id(st.session_state)

    st.markdown(
        """
        <div class="letter-trust-strip">
            <div><b>Private by design</b><span>Personal details are masked before analysis.</span></div>
            <div><b>Strict JSON output</b><span>Summary, urgency, translation, and checklist are structured.</span></div>
            <div><b>No guessing</b><span>Missing details stay marked as not specified.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.02, 0.98], gap="large")
    with left:
        st.markdown("<div class='letter-input-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='letter-panel-title'>✉ Letter input</div>", unsafe_allow_html=True)
        consent = st.checkbox(t("upload_consent"))
        uploaded_file = st.file_uploader(
            "Upload a PDF, Word file, or image",
            type=["pdf", "png", "jpg", "jpeg", "webp", "docx"],
            help="PDF, DOCX, JPG, JPEG, PNG, and WEBP are supported.",
        )
        pasted_text = st.text_area(
            t("paste_text"),
            height=250,
            placeholder="Paste the full letter here. You can also combine pasted text with a file upload.",
        )
        target_language = st.selectbox(
            "Translation language",
            [current_language_name(), "English", "German", "French", "Italian", "Spanish", "Turkish", "Ukrainian", "Arabic", "Farsi"],
            index=0,
        )
        analyze_clicked = st.button(t("analyze"), use_container_width=True)
        st.caption("Only the masked text is stored. The temporary privacy mapping is kept in memory for this request only.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            f"""
            <div class="letter-output-shell">
                <div class="letter-panel-title">Analysis workspace</div>
                <p>{escape(t("privacy_first_desc"))}</p>
                <div class="privacy-flow">
                    <span>Extract</span><span>Mask</span><span>Analyze</span><span>Save masked history</span>
                </div>
                <p class="letter-small-note">{escape(t("safety_notice"))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if not analyze_clicked:
        return

    if not consent:
        st.warning(t("missing_consent"))
        return

    with st.spinner("Extracting text and masking sensitive information..."):
        extracted_text, warnings = extract_text_from_upload(uploaded_file)

    for warning in warnings:
        st.warning(warning)

    source_text = "\n\n".join(part for part in [extracted_text, pasted_text] if part.strip())
    if not source_text.strip():
        st.warning(t("missing_letter"))
        return

    masked = mask_pii(source_text)

    with st.spinner("Analyzing the masked letter..."):
        result = analyze_letter(masked.masked_text, target_language)

    save_letter_history(st.session_state["user_id"], masked.masked_text, result)
    save_interaction(
        "letter_helper",
        result.get("summary", {}).get("summary", ""),
        {"pii_counts": masked.counts, "urgency": result.get("urgency", {})},
    )

    st.markdown("<div class='letter-results-grid'>", unsafe_allow_html=True)
    if result.get("service_warning"):
        st.warning(result["service_warning"])

    summary = result.get("summary", {})
    urgency = result.get("urgency", {})
    urgency_body, urgency_class = _urgency_markup(urgency)

    col1, col2 = st.columns([1.25, 0.75], gap="large")
    with col1:
        _result_card("Summary", "i", _summary_markup(summary))
    with col2:
        _result_card("Urgency", "!", urgency_body, f"urgency-card--{urgency_class}")

    steps_col, privacy_col = st.columns([1.08, 0.92], gap="large")
    with steps_col:
        _render_action_steps(result.get("action_steps", []))
    with privacy_col:
        pii_rows = "".join(
            f"<span>{escape(label.replace('_', ' ').title())}: <b>{count}</b></span>"
            for label, count in masked.counts.items()
        )
        _result_card("Privacy Gate", "◼", f"<div class='pii-counts'>{pii_rows}</div>")
        with st.expander(t("masked_text")):
            st.code(masked.masked_text[:12000])

    with st.expander("Full translation", expanded=True):
        st.text_area(
            "Full translation text",
            result.get("translation", "Not specified in the letter"),
            height=420,
            label_visibility="collapsed",
        )

    st.markdown("</div>", unsafe_allow_html=True)
