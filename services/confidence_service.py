from utils.constants import LOW_CONFIDENCE_THRESHOLD


class ConfidenceService:

    @staticmethod
    def requires_review(extracted):

        low_confidence_fields = []

        def inspect(obj, path=""):
            if isinstance(obj, dict):
                if "confidence" in obj:
                    if obj["confidence"] < LOW_CONFIDENCE_THRESHOLD:
                        low_confidence_fields.append(path)

                for key, value in obj.items():
                    inspect(value, f"{path}.{key}" if path else key)

            elif isinstance(obj, list):
                for idx, item in enumerate(obj):
                    inspect(item, f"{path}[{idx}]")

        inspect(extracted)

        return {
            "manual_review_required": len(low_confidence_fields) > 0,
            "low_confidence_fields": low_confidence_fields
        }