import streamlit as st

from services.case_outcome_service import LEGAL_DISCLAIMER, predict_case_outcome, retraining_workflow
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
            nationality = st.text_input("Nationality", value="")
            country_of_origin = st.text_input("Country of origin", value="")
            age_range = st.selectbox("Age range", ["Under 18", "18-25", "26-40", "41-60", "60+"], index=2)
        with a2:
            family_status = st.selectbox("Family status", ["Single", "Married/partnered", "With children", "Separated family", "Prefer not to say"])
            main_language = st.selectbox("Main language", ["English", "German", "French", "Italian", "Arabic", "Farsi", "Turkish", "Ukrainian", "Other"])
            family_ties = st.radio("Family ties in Switzerland?", ["No", "Yes"], horizontal=True)
        with a3:
            vulnerability_factors = st.multiselect("Vulnerability factors", VULNERABILITY_OPTIONS)
            country_risk_index = st.slider("Country risk index", 0.0, 10.0, 5.0, 0.5)
            case_complexity_score = st.slider("Case complexity score", 0.0, 10.0, 5.0, 0.5)

        st.progress(0.32, text="Section B - Case information")
        b1, b2, b3 = st.columns(3)
        with b1:
            case_type = st.selectbox("Case type", CASE_TYPES)
            canton = st.selectbox("Canton involved", canton_names, index=canton_names.index(default_canton))
        with b2:
            current_status = st.selectbox("Current case status", STATUS_OPTIONS)
            application_date = st.date_input("Date of application, if known", value=None)
        with b3:
            processing_duration_days = st.number_input("Processing duration in days, if known", min_value=0, value=0)
            previous_refusal = st.radio("Previous refusal?", ["No", "Yes"], horizontal=True)

        st.progress(0.48, text="Section C - Legal support")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            legal_representation = st.radio("Legal representation?", ["No", "Yes"], horizontal=True)
        with c2:
            ngo_support = st.radio("NGO support?", ["No", "Yes"], horizontal=True)
        with c3:
            lawyer_support = st.radio("Lawyer support?", ["No", "Yes"], horizontal=True)
        with c4:
            document_help = st.radio("Help preparing documents?", ["No", "Yes"], horizontal=True)
        legal_advice_before = st.radio("Have you received legal advice before?", ["No", "Yes"], horizontal=True)

        st.progress(0.64, text="Section D - Documents and evidence")
        d1, d2, d3 = st.columns(3)
        with d1:
            supporting_evidence = st.radio("Submitted supporting evidence?", ["No", "Yes"], horizontal=True)
            document_completeness = st.selectbox(
                "How complete are your documents?",
                ["Not started", "Some documents missing", "Mostly complete", "Complete", "Complete and certified"],
            )
        with d2:
            documents_translated = st.radio("Documents translated?", ["No", "Yes"], horizontal=True)
            translations_certified = st.radio("Translations certified?", ["No", "Yes"], horizontal=True)
        with d3:
            identity_documents = st.radio("Identity documents available?", ["No", "Yes"], horizontal=True)
            proof_supporting_claim = st.selectbox("Proof supporting your claim", ["No proof yet", "Some proof", "Strong proof"])
        additional_documents_requested = st.radio("Were additional documents requested?", ["No", "Yes"], horizontal=True)

        st.progress(0.78, text="Section E - Interview information")
        e1, e2, e3 = st.columns(3)
        with e1:
            has_interview = st.radio("Did you attend an interview?", ["No", "Yes"], horizontal=True)
        with e2:
            interpreter_provided = st.radio("Interpreter provided?", ["No", "Yes"], horizontal=True)
        with e3:
            interview_issue_reported = st.radio("Problems during the interview?", ["No", "Yes"], horizontal=True)
        understood_interpreter = st.radio("Did you understand the interpreter?", ["No", "Yes"], index=1, horizontal=True)

        appeal_relevant = current_status in {"Received negative decision", "Appeal stage"}
        if appeal_relevant:
            st.progress(0.9, text="Section F - Appeal information")
            f1, f2, f3 = st.columns(3)
            with f1:
                rejection_date = st.date_input("Date of rejection", value=None)
                refusal_reason = st.text_area("Reason provided", height=90)
            with f2:
                appeal_filed = st.radio("Appeal already submitted?", ["No", "Yes"], horizontal=True)
                appeal_deadline = st.date_input("Appeal deadline", value=None)
            with f3:
                appeal_support = st.radio("Legal support for appeal?", ["No", "Yes"], horizontal=True)
                new_evidence_available = st.radio("New evidence available?", ["No", "Yes"], horizontal=True)
            understands_refusal = st.radio("Do you understand the reason for refusal?", ["No", "Yes"], horizontal=True)
        else:
            rejection_date = None
            refusal_reason = ""
            appeal_filed = "No"
            appeal_deadline = None
            appeal_support = "No"
            new_evidence_available = "No"
            understands_refusal = "No"

        missed_deadline = st.radio("Any missed deadline?", ["No", "Yes"], horizontal=True)
        submitted = st.form_submit_button("Run informational estimate", type="primary", use_container_width=True)

    if not submitted:
        return None

    return {
        "nationality": nationality or "Unknown",
        "country_of_origin": country_of_origin or "Unknown",
        "origin_region": country_of_origin or nationality or "Unknown",
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
    st.json(
        {
            "model_type": metadata.get("model_type"),
            "model_version": metadata.get("model_version"),
            "trained_on": metadata.get("trained_on"),
            "training_data_hash": metadata.get("training_data_hash"),
            "metrics": metadata.get("metrics"),
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
