from typing import Any, Callable

import streamlit as st

from services.case_outcome_service import (
    LEGAL_DISCLAIMER,
    ORIGIN_COUNTRY_OPTIONS,
    predict_case_outcome,
    retraining_workflow,
    validate_prediction_answers,
)
from services.storage_service import save_interaction
from ui.components import render_page_hero
from utils.constants import SWISS_CANTONS


CASE_TYPES = [
    "Asylum",
    "Temporary Protection",
    "Family Reunification",
    "Work Permit",
    "Student Permit",
    "Residence Renewal",
    "Citizenship",
    "Other",
]

STATUS_OPTIONS = [
    "Preparing application",
    "Waiting for decision",
    "Received positive decision",
    "Received negative decision",
    "Appeal stage",
    "Unsure",
]

VULNERABILITY_OPTIONS = [
    "Minor",
    "Medical condition",
    "Trauma-related vulnerability",
    "Family separation",
    "Other humanitarian factor",
    "Prefer not to say",
]

FIELD_EXPLANATIONS = {
    "Nationality": "Required. The current synthetic model maps this to a training region, such as Middle East or South Asia, so it can affect similar-case matching and model features.",
    "Country of origin": "Required. The app maps the country to the closest training region and uses it for origin context, country-risk score, similar cases, and model features.",
    "Age range": "Use the applicant's age group. This can matter for minors, older applicants, dependency, and vulnerability-related preparation.",
    "Family status": "Choose the closest family situation. This helps estimate whether dependency, children, or separation may be relevant.",
    "Main language": "Choose the language the applicant is most comfortable using. This helps estimate translation and interview-readiness needs.",
    "Family ties in Switzerland?": "Select Yes if close family members are already in Switzerland and may be relevant to the case.",
    "Vulnerability factors": "Select only factors that are actually relevant: minor age, medical need, trauma, family separation, or another humanitarian issue.",
    "Country risk index": "Rate general risk in the country of origin: 0 = no known safety concern, 3 = some instability or discrimination, 5 = let the app use its estimated baseline for the entered origin, 7 = serious regional or group-specific risk, 10 = severe widespread danger.",
    "Case complexity score": "Rate how hard the case is to explain and prove: 0 = very simple and well documented, 3 = mostly clear with a few missing details, 5 = average complexity, 7 = several legal/evidence issues, 10 = very complex with contradictions, missing identity proof, missed deadlines, or multiple procedures. If unsure, leave 5.",
    "Case type": "Select the legal pathway that best matches the current application so the estimate compares the right type of cases.",
    "Canton involved": "Select the canton handling the case or where the applicant lives. It is used for similar-case and trend comparison.",
    "Current case status": "Tells the app whether the estimate should include appeal-specific questions and risk factors.",
    "Date of application, if known": "Optional context for timing and process duration. Unknown dates are not required for prediction.",
    "Processing duration in days, if known": "Used when known to compare against historical processing durations. Leave 0 if unknown.",
    "Previous refusal?": "Previous negative decisions can affect both risk and appeal-related analysis.",
    "Legal representation?": "Indicates whether a lawyer or recognized representative is involved. This often correlates with stronger preparation.",
    "NGO support?": "Captures support from advice centers or NGOs that may help prepare evidence and documents.",
    "Lawyer support?": "Specific legal support can influence document quality, deadlines, and appeal preparation.",
    "Help preparing documents?": "Shows whether someone helped organize, translate, or check supporting documents.",
    "Have you received legal advice before?": "Adds preparation context, even if there is no current representative.",
    "Submitted supporting evidence?": "Evidence strength is one of the main preparation signals used by the estimate.",
    "How complete are your documents?": "Choose the current document state: Not started = little/no paperwork, Some missing = key items absent, Mostly complete = only minor gaps, Complete = all main documents ready, Complete and certified = main documents plus certified copies/translations where needed.",
    "Documents translated?": "Translation readiness can affect whether documents are usable by authorities.",
    "Translations certified?": "Certified translations can improve document reliability in many official processes.",
    "Identity documents available?": "Identity evidence can be important for credibility and case completeness.",
    "Proof supporting your claim": "No proof yet = only statements so far, Some proof = partial documents/messages/reports, Strong proof = multiple relevant documents or credible third-party evidence.",
    "Were additional documents requested?": "Requests for more documents can indicate missing evidence or an active clarification process.",
    "Did you attend an interview?": "Interview status is used for similar-case matching and preparation guidance.",
    "Interpreter provided?": "Interpreter availability affects communication quality and interview reliability.",
    "Problems during the interview?": "Reported interview issues can increase uncertainty or affect appeal preparation.",
    "Did you understand the interpreter?": "Understanding the interpreter helps assess whether the interview record may be reliable.",
    "Date of rejection": "Appeal timing depends on the rejection date when a negative decision exists.",
    "Reason provided": "The refusal reason helps frame appeal risk and what evidence may be needed.",
    "Appeal already submitted?": "Used to decide whether appeal-specific outcome estimates are relevant.",
    "Appeal deadline": "Deadlines are critical in appeal stages and can strongly affect options.",
    "Legal support for appeal?": "Appeal support can affect procedural quality and the chance of presenting new arguments well.",
    "New evidence available?": "New evidence can materially change appeal preparation and estimated appeal worthiness.",
    "Do you understand the reason for refusal?": "Understanding the refusal reason helps identify whether the next step can target the actual weakness.",
    "Any missed deadline?": "Missed deadlines can strongly weaken a case, so this is treated as a risk factor.",
}


def _factor_widget(label: str, widget: Callable[..., Any], *args: Any, required: bool = False, **kwargs: Any) -> Any:
    label_text = f"{label} *" if required else label
    kwargs.setdefault("help", FIELD_EXPLANATIONS.get(label, "This factor helps the model compare your case with similar synthetic historical cases."))
    return widget(label_text, *args, **kwargs)


def _disclaimer() -> None:
    st.warning(f"Experimental informational estimate - not legal advice.\n\n{LEGAL_DISCLAIMER}")


def _workflow() -> None:
    steps = [
        ("1. Data Collection", "Your answers are collected for this estimate only."),
        ("2. Data Validation", "Completeness, missing values, and consistency are checked."),
        ("3. Feature Engineering", "Answers are converted into machine-learning features such as scores and yes/no flags."),
        ("4. Similar Case Retrieval", "The local anonymized dataset is searched for comparable synthetic cases."),
        ("5. Statistical Analysis", "Acceptance, appeal, and processing trends are calculated."),
        ("6. Prediction Engine", "A local Scikit-learn model estimates a probability."),
        ("7. Explainability Layer", "Feature importance and human-readable factors are shown."),
        ("8. Preparation Recommendations", "Practical improvement priorities are generated."),
    ]
    st.markdown("### Transparent analysis workflow")
    for title, body in steps:
        st.markdown(f"**{title}**  \n{body}")


def _questionnaire() -> dict | None:
    canton_names = [canton["name"] for canton in SWISS_CANTONS]
    default_canton = st.session_state.get("canton_name", "Zurich")
    if default_canton not in canton_names:
        default_canton = "Zurich"

    with st.form("case-outcome-questionnaire"):
        st.progress(0.15, text="Section A - Personal information")
        a1, a2, a3 = st.columns(3)
        with a1:
            nationality = _factor_widget("Nationality", st.selectbox, ORIGIN_COUNTRY_OPTIONS, index=ORIGIN_COUNTRY_OPTIONS.index("Afghanistan"), required=True)
            country_of_origin = _factor_widget("Country of origin", st.selectbox, ORIGIN_COUNTRY_OPTIONS, index=ORIGIN_COUNTRY_OPTIONS.index(nationality), required=True)
            age_range = _factor_widget("Age range", st.selectbox, ["Under 18", "18-25", "26-40", "41-60", "60+"], index=2)
        with a2:
            family_status = _factor_widget("Family status", st.selectbox, ["Single", "Married/partnered", "With children", "Separated family", "Prefer not to say"])
            main_language = _factor_widget("Main language", st.selectbox, ["English", "German", "French", "Italian", "Arabic", "Farsi", "Turkish", "Ukrainian", "Other"])
            family_ties = _factor_widget("Family ties in Switzerland?", st.radio, ["No", "Yes"], horizontal=True)
        with a3:
            vulnerability_factors = _factor_widget("Vulnerability factors", st.multiselect, VULNERABILITY_OPTIONS)
            country_risk_index = _factor_widget("Country risk index", st.slider, 0.0, 10.0, 5.0, 0.5)
            case_complexity_score = _factor_widget("Case complexity score", st.slider, 0.0, 10.0, 5.0, 0.5)

        st.progress(0.32, text="Section B - Case information")
        b1, b2, b3 = st.columns(3)
        with b1:
            case_type = _factor_widget("Case type", st.selectbox, CASE_TYPES)
            canton = _factor_widget("Canton involved", st.selectbox, canton_names, index=canton_names.index(default_canton))
        with b2:
            current_status = _factor_widget("Current case status", st.selectbox, STATUS_OPTIONS)
            application_date = _factor_widget("Date of application, if known", st.date_input, value=None)
        with b3:
            processing_duration_days = _factor_widget("Processing duration in days, if known", st.number_input, min_value=0, value=0)
            previous_refusal = _factor_widget("Previous refusal?", st.radio, ["No", "Yes"], horizontal=True)

        st.progress(0.48, text="Section C - Legal support")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            legal_representation = _factor_widget("Legal representation?", st.radio, ["No", "Yes"], horizontal=True)
        with c2:
            ngo_support = _factor_widget("NGO support?", st.radio, ["No", "Yes"], horizontal=True)
        with c3:
            lawyer_support = _factor_widget("Lawyer support?", st.radio, ["No", "Yes"], horizontal=True)
        with c4:
            document_help = _factor_widget("Help preparing documents?", st.radio, ["No", "Yes"], horizontal=True)
        legal_advice_before = _factor_widget("Have you received legal advice before?", st.radio, ["No", "Yes"], horizontal=True)

        st.progress(0.64, text="Section D - Documents and evidence")
        d1, d2, d3 = st.columns(3)
        with d1:
            supporting_evidence = _factor_widget("Submitted supporting evidence?", st.radio, ["No", "Yes"], horizontal=True)
            document_completeness = _factor_widget(
                "How complete are your documents?",
                st.selectbox,
                ["Not started", "Some documents missing", "Mostly complete", "Complete", "Complete and certified"],
            )
        with d2:
            documents_translated = _factor_widget("Documents translated?", st.radio, ["No", "Yes"], horizontal=True)
            translations_certified = _factor_widget("Translations certified?", st.radio, ["No", "Yes"], horizontal=True)
        with d3:
            identity_documents = _factor_widget("Identity documents available?", st.radio, ["No", "Yes"], horizontal=True)
            proof_supporting_claim = _factor_widget("Proof supporting your claim", st.selectbox, ["No proof yet", "Some proof", "Strong proof"])
        additional_documents_requested = _factor_widget("Were additional documents requested?", st.radio, ["No", "Yes"], horizontal=True)

        st.progress(0.78, text="Section E - Interview information")
        e1, e2, e3 = st.columns(3)
        with e1:
            has_interview = _factor_widget("Did you attend an interview?", st.radio, ["No", "Yes"], horizontal=True)
        with e2:
            interpreter_provided = _factor_widget("Interpreter provided?", st.radio, ["No", "Yes"], horizontal=True)
        with e3:
            interview_issue_reported = _factor_widget("Problems during the interview?", st.radio, ["No", "Yes"], horizontal=True)
        understood_interpreter = _factor_widget("Did you understand the interpreter?", st.radio, ["No", "Yes"], index=1, horizontal=True)

        appeal_relevant = current_status in {"Received negative decision", "Appeal stage"}
        if appeal_relevant:
            st.progress(0.9, text="Section F - Appeal information")
            f1, f2, f3 = st.columns(3)
            with f1:
                rejection_date = _factor_widget("Date of rejection", st.date_input, value=None)
                refusal_reason = _factor_widget("Reason provided", st.text_area, height=90)
            with f2:
                appeal_filed = _factor_widget("Appeal already submitted?", st.radio, ["No", "Yes"], horizontal=True)
                appeal_deadline = _factor_widget("Appeal deadline", st.date_input, value=None)
            with f3:
                appeal_support = _factor_widget("Legal support for appeal?", st.radio, ["No", "Yes"], horizontal=True)
                new_evidence_available = _factor_widget("New evidence available?", st.radio, ["No", "Yes"], horizontal=True)
            understands_refusal = _factor_widget("Do you understand the reason for refusal?", st.radio, ["No", "Yes"], horizontal=True)
        else:
            rejection_date = None
            refusal_reason = ""
            appeal_filed = "No"
            appeal_deadline = None
            appeal_support = "No"
            new_evidence_available = "No"
            understands_refusal = "No"

        missed_deadline = _factor_widget("Any missed deadline?", st.radio, ["No", "Yes"], horizontal=True)
        submitted = st.form_submit_button("Run informational estimate", type="primary", use_container_width=True)

    if not submitted:
        return None

    answers = {
        "nationality": nationality.strip(),
        "country_of_origin": country_of_origin.strip(),
        "origin_region": country_of_origin.strip() or nationality.strip(),
        "age_range": age_range,
        "family_status": family_status,
        "main_language": main_language,
        "family_ties_in_switzerland": family_ties,
        "vulnerability_factors": vulnerability_factors,
        "country_risk_index": country_risk_index,
        "case_complexity_score": case_complexity_score,
        "case_type": case_type,
        "canton": canton,
        "current_status": current_status,
        "application_date": str(application_date) if application_date else "",
        "processing_duration_days": processing_duration_days,
        "previous_refusal": previous_refusal,
        "legal_representation": legal_representation,
        "ngo_support": ngo_support,
        "lawyer_support": lawyer_support,
        "document_help": document_help,
        "legal_advice_before": legal_advice_before,
        "supporting_evidence": supporting_evidence,
        "document_completeness": document_completeness,
        "documents_translated": documents_translated,
        "translations_certified": translations_certified,
        "identity_documents": identity_documents,
        "proof_supporting_claim": proof_supporting_claim,
        "additional_documents_requested": additional_documents_requested,
        "has_interview": has_interview,
        "interpreter_provided": interpreter_provided,
        "interview_issue_reported": interview_issue_reported,
        "understood_interpreter": understood_interpreter,
        "rejection_date": str(rejection_date) if rejection_date else "",
        "refusal_reason": refusal_reason,
        "appeal_filed": appeal_filed,
        "appeal_deadline": str(appeal_deadline) if appeal_deadline else "",
        "appeal_support": appeal_support,
        "new_evidence_available": new_evidence_available,
        "understands_refusal": understands_refusal,
        "missed_deadline": missed_deadline,
    }
    missing_required = validate_prediction_answers(answers)
    if missing_required:
        st.error(
            "Please complete the required fields before running the estimate: "
            + ", ".join(missing_required)
            + "."
        )
        return None

    return answers


def _scenario_simulation(result: dict) -> None:
    features = result["features"]
    base = result["acceptance_probability"]
    scenarios = []
    if features["legal_representation"] == "No":
        scenarios.append(("If legal representation is added", min(95, base + 6)))
    if features["evidence_completeness_score"] < 8:
        scenarios.append(("If additional evidence is provided", min(95, base + 9)))
    if features["document_quality_score"] < 7:
        scenarios.append(("If documents remain incomplete", max(5, base - 8)))
    if not scenarios:
        scenarios.append(("If records stay complete and deadlines are met", min(95, base + 3)))
    for label, value in scenarios:
        st.markdown(f"- **{label}:** acceptance likelihood may be around **{value:.1f}%**. This is a simulation, not a guarantee.")


def _render_results(result: dict) -> None:
    _disclaimer()
    low, high = result["uncertainty_range"]
    st.subheader("Estimated Outcome")
    m1, m2, m3 = st.columns(3)
    m1.metric("Acceptance likelihood", f"{result['acceptance_probability']}%")
    m2.metric("Confidence level", result["confidence"])
    m3.metric("Uncertainty range", f"{low}% - {high}%")
    st.caption("This range is deliberately conservative because migration outcomes are uncertain and the current dataset is synthetic.")

    similar = result["similar_cases"]
    st.subheader("Similar Case Analysis")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Similar cases found", similar["count"])
    c2.metric("Average similarity", f"{similar['average_similarity']}%")
    c3.metric("Acceptance in similar cases", f"{similar['acceptance_rate']}%")
    c4.metric("Average processing", f"{similar['average_processing_time']:.0f} days")
    st.write("These cases are similar based on case type, canton, country or region of origin, legal representation, evidence completeness, and interview status.")
    with st.expander("Comparable synthetic cases"):
        st.dataframe(similar["rows"], use_container_width=True)

    st.subheader("Historical Trend Analysis")
    trends = result["trends"]
    t1, t2, t3 = st.columns(3)
    t1.metric("Acceptance trend", trends["acceptance_label"])
    t2.metric("Appeal success trend", trends["appeal_label"])
    t3.metric("Processing time trend", trends["processing_label"])
    st.line_chart(trends["yearly"].set_index("year")[["acceptance_rate", "appeal_success_rate"]])
    st.bar_chart(trends["yearly"].set_index("year")[["avg_processing_days"]])

    st.subheader("Explainable AI")
    explanation = result["explainability"]
    inc, dec = st.columns(2)
    with inc:
        st.markdown("**Factors increasing estimated success**")
        for item in explanation["increasing"] or ["No strong positive factor was detected from your answers."]:
            st.markdown(f"- {item}")
    with dec:
        st.markdown("**Factors decreasing estimated success or confidence**")
        for item in explanation["decreasing"] or ["No major weakening factor was detected from your answers."]:
            st.markdown(f"- {item}")
    with st.expander("Model feature importance"):
        for item in explanation["technical_top_features"]:
            st.markdown(f"- {item}")

    st.subheader("Scenario Simulation")
    _scenario_simulation(result)

    if result["features"]["appeal_filed"] == "Yes" or result["features"]["previous_refusal"] == "Yes":
        st.subheader("Appeal Risk Analysis")
        _disclaimer()
        a1, a2, a3 = st.columns(3)
        a1.metric("Appeal worthiness score", f"{result['appeal_worthiness_score']}/100")
        a2.metric("Appeal success probability", f"{result['appeal_probability']}%")
        a3.metric("Estimated effort", "High")
        st.write("An appeal may be worth considering based on historical patterns, but this is not legal advice.")

    st.subheader("Preparation Guidance")
    for item in result["recommendations"]:
        st.markdown(
            f"**{item['priority']} priority:** {item['item']}  \n"
            f"Expected impact: {item['impact']} | Confidence: {item['confidence']}"
        )

    st.subheader("Model Transparency")
    metadata = result["metadata"]
    st.caption(
        "Origin mapping: "
        f"{result['features'].get('raw_country_of_origin') or result['features'].get('raw_nationality')} "
        f"was evaluated as {result['features'].get('origin_region')} for this synthetic model."
    )
    st.json(
        {
            "model_type": metadata.get("model_type"),
            "model_version": metadata.get("model_version"),
            "trained_on": metadata.get("trained_on"),
            "training_data_hash": metadata.get("training_data_hash"),
            "metrics": metadata.get("metrics"),
            "model_probability": result.get("model_probability"),
            "structured_prior_probability": result.get("structured_prior_probability"),
            "feature_count": len(metadata.get("features", [])),
        }
    )


def render_case_outcome_intelligence() -> None:
    render_page_hero(
        "Case Outcome Intelligence",
        "Explore possible outcomes, historical trends, appeal risks, and preparation recommendations based on similar cases.",
        "Experimental informational estimate",
        st.session_state["canton_code"],
    )
    _disclaimer()

    st.markdown(
        """
        <div class="soft-card">
            <b>How this works</b><br>
            You answer a guided questionnaire. The app converts answers into privacy-preserving features,
            compares them with anonymized synthetic historical cases, runs a local Scikit-learn model,
            and explains the estimate in plain language.
        </div>
        """,
        unsafe_allow_html=True,
    )

    _workflow()
    answers = _questionnaire()
    if answers is None:
        return

    with st.spinner("Running local prediction, similarity, trends, and explainability analysis..."):
        result = predict_case_outcome(answers)

    save_interaction(
        "case_outcome_intelligence",
        f"{answers['case_type']} in {answers['canton']} - estimate generated",
        {"case_type": answers["case_type"], "canton": answers["canton"], "confidence": result["confidence"]},
    )
    _render_results(result)

    with st.expander("Admin: retraining workflow"):
        st.write("Use this when a new anonymized dataset is added.")
        if st.button("Retrain local models now"):
            retraining = retraining_workflow()
            st.success("Retraining completed and metadata saved.")
            st.json(retraining)
