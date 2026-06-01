try:
    from fastapi import APIRouter
except ImportError:
    class APIRouter:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs) -> None:
            self.routes = []

        def post(self, *args, **kwargs):
            def decorator(function):
                return function

            return decorator

        def get(self, *args, **kwargs):
            def decorator(function):
                return function

            return decorator

from services.case_outcome_service import load_or_train_model, predict_case_outcome, retraining_workflow, trend_analysis, load_dataset


router = APIRouter(prefix="/case-outcome", tags=["case-outcome"])


@router.post("/predict/outcome")
def predict_outcome(payload: dict) -> dict:
    return predict_case_outcome(payload)


@router.post("/predict/appeal")
def predict_appeal(payload: dict) -> dict:
    result = predict_case_outcome(payload)
    return {
        "appeal_success_probability": result["appeal_probability"],
        "appeal_worthiness_score": result["appeal_worthiness_score"],
        "confidence": result["confidence"],
        "disclaimer": result["disclaimer"],
    }


@router.post("/similar-cases/search")
def search_similar_cases(payload: dict) -> dict:
    return predict_case_outcome(payload)["similar_cases"]


@router.get("/trends/acceptance")
def acceptance_trends(case_type: str = "Asylum", canton: str = "Zurich") -> dict:
    data = load_dataset()
    trends = trend_analysis(data, case_type, canton)
    return {
        "label": trends["acceptance_label"],
        "yearly": trends["yearly"].to_dict("records"),
    }


@router.get("/trends/appeals")
def appeal_trends(case_type: str = "Asylum", canton: str = "Zurich") -> dict:
    data = load_dataset()
    trends = trend_analysis(data, case_type, canton)
    return {
        "label": trends["appeal_label"],
        "yearly": trends["yearly"].to_dict("records"),
    }


@router.get("/models/metadata")
def model_metadata() -> dict:
    _, metadata = load_or_train_model()
    return metadata


@router.post("/models/retrain")
def retrain_models() -> dict:
    return retraining_workflow()
