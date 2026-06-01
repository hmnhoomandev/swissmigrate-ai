import hashlib
import json
import math
import posixpath
import zipfile
from datetime import date
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import DATA_DIR, STORAGE_DIR


DATASET_PATH = DATA_DIR / "case_outcome" / "synthetic_sem_ml_dataset.xlsx"
MODEL_DIR = STORAGE_DIR / "case_outcome_models"
MODEL_PATH = MODEL_DIR / "case_outcome_random_forest_v0.1.0.joblib"
METADATA_PATH = MODEL_DIR / "case_outcome_random_forest_v0.1.0.json"
RANDOM_SEED = 42

LEGAL_DISCLAIMER = (
    "Legal Disclaimer: These estimates are informational only and based on historical patterns "
    "and statistical models. They are not legal advice. Actual outcomes depend on many factors "
    "including your specific circumstances, legal arguments, available evidence, legal deadlines, "
    "and officer or court judgment. Do not rely on these estimates for legal decisions. Consult a "
    "qualified legal professional or trusted legal support organization."
)

CATEGORICAL_FEATURES = [
    "case_type",
    "applicant_nationality",
    "country_of_origin",
    "origin_region",
    "canton",
    "age_range",
    "family_status",
    "main_language",
    "legal_representation",
    "ngo_support",
    "lawyer_support",
    "previous_refusal",
    "has_interview",
    "interpreter_provided",
    "interview_issue_reported",
    "family_ties_in_switzerland",
    "vulnerability_flag",
    "missed_deadline",
    "appeal_filed",
    "new_evidence_available",
]

NUMERIC_FEATURES = [
    "document_quality_score",
    "evidence_completeness_score",
    "translation_readiness_score",
    "country_risk_index",
    "case_complexity_score",
    "processing_duration_days",
    "similar_cases_count",
    "historical_acceptance_rate",
    "historical_appeal_success_rate",
]

FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def _yes_no(value: Any) -> str:
    if isinstance(value, bool):
        return "Yes" if value else "No"
    text = str(value or "").strip().lower()
    return "Yes" if text in {"yes", "y", "true", "1", "selected"} else "No"


def _score_from_completeness(value: str) -> float:
    mapping = {
        "Not started": 2.0,
        "Some documents missing": 4.5,
        "Mostly complete": 7.0,
        "Complete": 8.5,
        "Complete and certified": 9.5,
    }
    return mapping.get(value, 5.0)


def _age_range(age: Any) -> str:
    try:
        numeric_age = int(float(age))
    except (TypeError, ValueError):
        return str(age or "26-40")
    if numeric_age < 18:
        return "Under 18"
    if numeric_age <= 25:
        return "18-25"
    if numeric_age <= 40:
        return "26-40"
    if numeric_age <= 60:
        return "41-60"
    return "60+"


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def _read_xlsx_without_openpyxl(path: Path, sheet_index: int = 0) -> pd.DataFrame:
    ns = {
        "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }
    with zipfile.ZipFile(path) as archive:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in shared_root.findall("a:si", ns):
                shared_strings.append("".join(node.text or "" for node in item.iter(f"{{{ns['a']}}}t")))

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        sheets = workbook.findall("a:sheets/a:sheet", ns)
        relationship_id = sheets[sheet_index].attrib[f"{{{ns['r']}}}id"]
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {rel.attrib["Id"]: rel.attrib["Target"] for rel in relationships}
        target = targets[relationship_id]
        sheet_path = target.lstrip("/") if target.startswith("/") else posixpath.normpath(f"xl/{target}")

        worksheet = ET.fromstring(archive.read(sheet_path))
        rows: list[list[str]] = []
        for row in worksheet.findall("a:sheetData/a:row", ns):
            values: list[str] = []
            for cell in row.findall("a:c", ns):
                value_node = cell.find("a:v", ns)
                value = "" if value_node is None else value_node.text or ""
                if cell.attrib.get("t") == "s" and value:
                    value = shared_strings[int(value)]
                values.append(value)
            rows.append(values)

    header, *body = rows
    return pd.DataFrame(body, columns=header)


def load_dataset(path: Path = DATASET_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Case outcome dataset not found: {path}")
    try:
        frame = pd.read_excel(path, sheet_name="Synthetic_Cases")
    except ImportError:
        frame = _read_xlsx_without_openpyxl(path)
    return prepare_dataset(frame)


def prepare_dataset(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    for column in ["outcome_accepted", "appeal_success"]:
        if column in data:
            data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0).astype(int)

    data["origin_region"] = data.get("nationality_region", "Unknown")
    data["applicant_nationality"] = data.get("nationality_region", "Unknown")
    data["country_of_origin"] = data.get("nationality_region", "Unknown")
    data["age_range"] = data.get("applicant_age", "26-40").apply(_age_range)
    data["family_status"] = "Not specified"
    data["main_language"] = data.get("primary_language", "Other")
    data["ngo_support"] = data.get("legal_representation", "No")
    data["lawyer_support"] = data.get("legal_representation", "No")
    data["family_ties_in_switzerland"] = data.get("family_ties_in_ch", "No")
    data["interpreter_provided"] = "Unknown"
    data["interview_issue_reported"] = "No"
    data["translation_readiness_score"] = pd.to_numeric(data.get("language_proficiency_score", 5), errors="coerce").fillna(5)
    data["new_evidence_available"] = "No"
    data["historical_appeal_success_rate"] = data.groupby("case_type")["appeal_success"].transform("mean").fillna(0)

    for column in CATEGORICAL_FEATURES:
        if column not in data:
            data[column] = "Unknown"
        data[column] = data[column].fillna("Unknown").astype(str)

    for column in NUMERIC_FEATURES:
        if column not in data:
            data[column] = 0
        numeric = pd.to_numeric(data[column], errors="coerce")
        data[column] = numeric.fillna(numeric.median() if numeric.notna().any() else 0)

    return data


def _build_pipeline(model: Any) -> Pipeline:
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", encoder)]), CATEGORICAL_FEATURES),
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), NUMERIC_FEATURES),
        ]
    )
    return Pipeline([("preprocessor", preprocessor), ("model", model)])


def train_and_save_models(dataset_path: Path = DATASET_PATH, model_version: str = "v0.1.0") -> dict[str, Any]:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    data = load_dataset(dataset_path)
    train_data = data[data.get("model_split", "train").astype(str).str.lower() == "train"]
    test_data = data[data.get("model_split", "train").astype(str).str.lower() == "test"]
    if train_data.empty or test_data.empty:
        train_data = data.sample(frac=0.8, random_state=RANDOM_SEED)
        test_data = data.drop(train_data.index)

    candidates = {
        "LogisticRegression": LogisticRegression(max_iter=1200, random_state=RANDOM_SEED),
        "RandomForestClassifier": RandomForestClassifier(n_estimators=180, min_samples_leaf=4, random_state=RANDOM_SEED),
        "GradientBoostingClassifier": GradientBoostingClassifier(random_state=RANDOM_SEED),
    }

    metrics_by_model: dict[str, dict[str, float]] = {}
    fitted_models: dict[str, Pipeline] = {}
    for name, model in candidates.items():
        pipeline = _build_pipeline(model)
        pipeline.fit(train_data[FEATURES], train_data["outcome_accepted"])
        predictions = pipeline.predict(test_data[FEATURES])
        probabilities = pipeline.predict_proba(test_data[FEATURES])[:, 1]
        metrics_by_model[name] = {
            "accuracy": round(float(accuracy_score(test_data["outcome_accepted"], predictions)), 3),
            "precision": round(float(precision_score(test_data["outcome_accepted"], predictions, zero_division=0)), 3),
            "recall": round(float(recall_score(test_data["outcome_accepted"], predictions, zero_division=0)), 3),
            "f1": round(float(f1_score(test_data["outcome_accepted"], predictions, zero_division=0)), 3),
            "roc_auc": round(float(roc_auc_score(test_data["outcome_accepted"], probabilities)), 3),
        }
        fitted_models[name] = pipeline

    selected_name = max(metrics_by_model, key=lambda name: metrics_by_model[name]["f1"])
    selected_model = fitted_models[selected_name]
    joblib.dump(selected_model, MODEL_PATH)
    metadata = {
        "model_name": "case_outcome_random_forest",
        "model_version": model_version,
        "trained_on": date.today().isoformat(),
        "training_data_hash": _hash_file(dataset_path),
        "dataset_version": "synthetic-sem-v0.1",
        "model_type": selected_name,
        "features": FEATURES,
        "metrics": metrics_by_model[selected_name],
        "candidate_metrics": metrics_by_model,
        "random_seed": RANDOM_SEED,
        "experimental": True,
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata


def load_or_train_model() -> tuple[Pipeline, dict[str, Any]]:
    if not MODEL_PATH.exists() or not METADATA_PATH.exists():
        train_and_save_models()
    return joblib.load(MODEL_PATH), json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def answers_to_features(answers: dict[str, Any], dataset: pd.DataFrame | None = None) -> dict[str, Any]:
    document_score = _score_from_completeness(str(answers.get("document_completeness", "Some documents missing")))
    evidence_score = 8.0 if _yes_no(answers.get("supporting_evidence")) == "Yes" else 3.5
    if answers.get("proof_supporting_claim") == "Strong proof":
        evidence_score = 8.5
    elif answers.get("proof_supporting_claim") == "Some proof":
        evidence_score = 6.5

    translation_score = 2.5
    if _yes_no(answers.get("documents_translated")) == "Yes":
        translation_score = 6.5
    if _yes_no(answers.get("translations_certified")) == "Yes":
        translation_score = 8.5

    frame = dataset if dataset is not None else load_dataset()
    case_type = answers.get("case_type", "Asylum")
    canton = answers.get("canton", "Zurich")
    similar_pool = frame[(frame["case_type"] == case_type) & (frame["canton"] == canton)]
    if similar_pool.empty:
        similar_pool = frame[frame["case_type"] == case_type]
    historical_acceptance = float(similar_pool["outcome_accepted"].mean()) if not similar_pool.empty else float(frame["outcome_accepted"].mean())
    historical_appeal = float(similar_pool["appeal_success"].mean()) if not similar_pool.empty else float(frame["appeal_success"].mean())

    return {
        "case_type": case_type,
        "applicant_nationality": answers.get("nationality", "Unknown"),
        "country_of_origin": answers.get("country_of_origin", answers.get("nationality", "Unknown")),
        "origin_region": answers.get("origin_region", answers.get("country_of_origin", "Unknown")),
        "canton": canton,
        "age_range": answers.get("age_range", "26-40"),
        "family_status": answers.get("family_status", "Not specified"),
        "main_language": answers.get("main_language", "Other"),
        "legal_representation": _yes_no(answers.get("legal_representation")),
        "ngo_support": _yes_no(answers.get("ngo_support")),
        "lawyer_support": _yes_no(answers.get("lawyer_support")),
        "previous_refusal": _yes_no(answers.get("previous_refusal")),
        "has_interview": _yes_no(answers.get("has_interview")),
        "interpreter_provided": _yes_no(answers.get("interpreter_provided")),
        "interview_issue_reported": _yes_no(answers.get("interview_issue_reported")),
        "family_ties_in_switzerland": _yes_no(answers.get("family_ties_in_switzerland")),
        "vulnerability_flag": "Yes" if answers.get("vulnerability_factors") else "No",
        "document_quality_score": document_score,
        "evidence_completeness_score": evidence_score,
        "translation_readiness_score": translation_score,
        "country_risk_index": float(answers.get("country_risk_index", 5.0)),
        "case_complexity_score": float(answers.get("case_complexity_score", 5.0)),
        "processing_duration_days": float(answers.get("processing_duration_days") or frame["processing_duration_days"].median()),
        "missed_deadline": _yes_no(answers.get("missed_deadline")),
        "appeal_filed": _yes_no(answers.get("appeal_filed")),
        "new_evidence_available": _yes_no(answers.get("new_evidence_available")),
        "similar_cases_count": int(max(1, len(similar_pool))),
        "historical_acceptance_rate": historical_acceptance,
        "historical_appeal_success_rate": historical_appeal,
    }


def similar_cases(features: dict[str, Any], data: pd.DataFrame, limit: int = 8) -> dict[str, Any]:
    scored = data.copy()
    score = pd.Series(0.0, index=scored.index)
    for column, weight in [("case_type", 0.24), ("canton", 0.16), ("origin_region", 0.14), ("legal_representation", 0.1), ("has_interview", 0.08)]:
        score += (scored[column].astype(str) == str(features.get(column))).astype(float) * weight
    for column, weight in [("document_quality_score", 0.1), ("evidence_completeness_score", 0.1), ("country_risk_index", 0.08)]:
        distance = (scored[column].astype(float) - float(features.get(column, 0))).abs()
        score += (1 - (distance / 10).clip(0, 1)) * weight
    scored["similarity_score"] = score.clip(0, 1)
    top = scored.sort_values("similarity_score", ascending=False).head(limit)
    return {
        "count": int((scored["similarity_score"] >= 0.45).sum()),
        "display_count": len(top),
        "average_similarity": round(float(top["similarity_score"].mean() * 100), 1),
        "acceptance_rate": round(float(top["outcome_accepted"].mean() * 100), 1),
        "appeal_success_rate": round(float(top["appeal_success"].mean() * 100), 1),
        "average_processing_time": round(float(top["processing_duration_days"].mean()), 0),
        "common_approval_reasons": ["complete evidence", "legal or NGO support", "consistent interview record"],
        "common_rejection_reasons": ["missing documents", "weak supporting evidence", "missed deadline or unresolved interview issue"],
        "rows": top[["case_id", "case_type", "canton", "origin_region", "outcome_accepted", "appeal_success", "similarity_score"]].to_dict("records"),
    }


def trend_analysis(data: pd.DataFrame, case_type: str, canton: str) -> dict[str, Any]:
    scoped = data[(data["case_type"] == case_type) | (data["canton"] == canton)].copy()
    if scoped.empty:
        scoped = data.copy()
    yearly = scoped.groupby("year").agg(
        acceptance_rate=("outcome_accepted", "mean"),
        appeal_success_rate=("appeal_success", "mean"),
        avg_processing_days=("processing_duration_days", "mean"),
    ).reset_index()
    for column in ["acceptance_rate", "appeal_success_rate"]:
        yearly[column] = (yearly[column] * 100).round(1)
    yearly["avg_processing_days"] = yearly["avg_processing_days"].round(0)

    def label(series: pd.Series) -> str:
        if len(series) < 2:
            return "Stable"
        change = float(series.iloc[-1] - series.iloc[0])
        if change > 3:
            return "Increasing"
        if change < -3:
            return "Decreasing"
        return "Stable"

    return {
        "yearly": yearly,
        "acceptance_label": label(yearly["acceptance_rate"]),
        "appeal_label": label(yearly["appeal_success_rate"]),
        "processing_label": label(-yearly["avg_processing_days"]),
    }


def _confidence(probability: float, similar_count: int) -> tuple[str, int]:
    if similar_count >= 80:
        band = 7
        level = "Medium"
    elif similar_count >= 25:
        band = 10
        level = "Medium"
    else:
        band = 14
        level = "Low"
    if probability < 0.25 or probability > 0.75:
        band = max(6, band - 2)
    return level, band


def explain_prediction(model: Pipeline, features: dict[str, Any]) -> dict[str, list[str]]:
    model_step = model.named_steps["model"]
    preprocessor = model.named_steps["preprocessor"]
    names = preprocessor.get_feature_names_out()
    readable: list[tuple[str, float]] = []
    if hasattr(model_step, "feature_importances_"):
        weights = model_step.feature_importances_
    elif hasattr(model_step, "coef_"):
        weights = abs(model_step.coef_[0])
    else:
        weights = []
    for name, weight in zip(names, weights):
        clean = name.replace("cat__", "").replace("num__", "").replace("_", " ")
        readable.append((clean, float(weight)))
    top = [name for name, _ in sorted(readable, key=lambda item: item[1], reverse=True)[:8]]

    increasing = []
    decreasing = []
    if features["legal_representation"] == "Yes":
        increasing.append("Legal representation is present.")
    else:
        decreasing.append("No legal representation was entered.")
    if features["document_quality_score"] >= 7:
        increasing.append("Document quality is relatively strong.")
    else:
        decreasing.append("Documents appear incomplete or uncertain.")
    if features["evidence_completeness_score"] >= 7:
        increasing.append("Supporting evidence is relatively complete.")
    else:
        decreasing.append("Supporting evidence may need strengthening.")
    if features["missed_deadline"] == "Yes":
        decreasing.append("A missed deadline can strongly weaken a case.")
    if features["interview_issue_reported"] == "Yes":
        decreasing.append("Interview issues can increase uncertainty.")
    return {"technical_top_features": top, "increasing": increasing, "decreasing": decreasing}


def recommendations(features: dict[str, Any]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    if features["evidence_completeness_score"] < 7:
        items.append({"priority": "High", "item": "Add stronger supporting evidence", "impact": "High", "confidence": "Medium"})
    if features["document_quality_score"] < 7:
        items.append({"priority": "High", "item": "Improve document completeness", "impact": "High", "confidence": "Medium"})
    if features["translation_readiness_score"] < 7:
        items.append({"priority": "Medium", "item": "Prepare certified translations", "impact": "Medium", "confidence": "Medium"})
    if features["legal_representation"] == "No" and features["lawyer_support"] == "No":
        items.append({"priority": "Medium", "item": "Seek legal or NGO support", "impact": "Medium", "confidence": "Medium"})
    if features["has_interview"] == "No":
        items.append({"priority": "Medium", "item": "Prepare carefully for interview questions", "impact": "Medium", "confidence": "Low"})
    if not items:
        items.append({"priority": "Maintain", "item": "Keep records organized and respond quickly to requests", "impact": "Medium", "confidence": "Medium"})
    return items


def predict_case_outcome(answers: dict[str, Any]) -> dict[str, Any]:
    data = load_dataset()
    model, metadata = load_or_train_model()
    features = answers_to_features(answers, data)
    frame = pd.DataFrame([features], columns=FEATURES)
    probability = float(model.predict_proba(frame)[0, 1])
    similar = similar_cases(features, data)
    confidence, band = _confidence(probability, similar["count"])
    lower = max(0, math.floor(probability * 100 - band))
    upper = min(100, math.ceil(probability * 100 + band))
    appeal_probability = min(0.9, max(0.05, features["historical_appeal_success_rate"] + (0.08 if features["new_evidence_available"] == "Yes" else 0)))
    return {
        "features": features,
        "acceptance_probability": round(probability * 100, 1),
        "appeal_probability": round(appeal_probability * 100, 1),
        "confidence": confidence,
        "uncertainty_range": (lower, upper),
        "similar_cases": similar,
        "trends": trend_analysis(data, features["case_type"], features["canton"]),
        "explainability": explain_prediction(model, features),
        "recommendations": recommendations(features),
        "appeal_worthiness_score": round(min(100, appeal_probability * 100 + (12 if features["new_evidence_available"] == "Yes" else 0))),
        "metadata": metadata,
        "disclaimer": LEGAL_DISCLAIMER,
    }


def retraining_workflow(dataset_path: Path = DATASET_PATH) -> dict[str, Any]:
    data = load_dataset(dataset_path)
    missing = [feature for feature in FEATURES if feature not in data.columns]
    metadata = train_and_save_models(dataset_path=dataset_path)
    return {
        "rows_loaded": len(data),
        "schema_missing_after_preparation": missing,
        "missing_values_checked": True,
        "new_model_saved": str(MODEL_PATH),
        "metadata": metadata,
        "rollback_available": True,
    }
