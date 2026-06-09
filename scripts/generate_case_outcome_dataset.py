import math
import random
import sys
import zipfile
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import DATA_DIR
from services.case_outcome_service import COUNTRY_PROFILES, ORIGIN_COUNTRY_OPTIONS


OUTPUT_PATH = DATA_DIR / "case_outcome" / "synthetic_sem_ml_dataset.xlsx"
RANDOM_SEED = 20260609
ROW_COUNT = 4200
MIN_ROWS_PER_COUNTRY = 45
MIN_ASYLUM_ROWS_PER_COUNTRY = 45
MIN_FAMILY_ROWS_PER_COUNTRY = 15
MIN_TEMPORARY_PROTECTION_ROWS_PER_COUNTRY = 10

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
CANTONS = ["Zurich", "Geneva", "Vaud", "Bern", "Basel-Stadt", "Fribourg", "Ticino", "Neuchatel"]
LANGUAGES = ["English", "German", "French", "Italian", "Arabic", "Farsi", "Turkish", "Ukrainian", "Other"]
DOCUMENT_COMPLETENESS = ["Not started", "Some documents missing", "Mostly complete", "Complete", "Complete and certified"]


def sigmoid(value: float) -> float:
    return 1 / (1 + math.exp(-value))


def logit(probability: float) -> float:
    probability = min(0.97, max(0.03, probability))
    return math.log(probability / (1 - probability))


def yes_no(probability: float) -> str:
    return "Yes" if random.random() < probability else "No"


def bounded_normal(mean: float, spread: float, low: float = 0.0, high: float = 10.0) -> float:
    return round(min(high, max(low, random.gauss(mean, spread))), 1)


def choose_country() -> str:
    weights = [max(80, COUNTRY_PROFILES[country]["applications"]) for country in ORIGIN_COUNTRY_OPTIONS]
    return random.choices(ORIGIN_COUNTRY_OPTIONS, weights=weights, k=1)[0]


def choose_case_type(country: str) -> str:
    profile = COUNTRY_PROFILES[country]
    risk = profile["risk"]
    if country == "Ukraine":
        weights = [0.08, 0.62, 0.06, 0.06, 0.04, 0.08, 0.02, 0.04]
    elif risk >= 8:
        weights = [0.52, 0.13, 0.1, 0.04, 0.03, 0.06, 0.02, 0.1]
    elif risk >= 6:
        weights = [0.35, 0.08, 0.13, 0.09, 0.06, 0.12, 0.04, 0.13]
    else:
        weights = [0.14, 0.02, 0.12, 0.26, 0.14, 0.16, 0.07, 0.09]
    return random.choices(CASE_TYPES, weights=weights, k=1)[0]


def score_probability(row: dict[str, object]) -> float:
    case_type = str(row["case_type"])
    risk = float(row["country_risk_index"])
    origin_acceptance = float(row["origin_acceptance_baseline"])
    origin_protection = float(row["origin_protection_baseline"])
    docs = float(row["document_quality_score"])
    evidence = float(row["evidence_completeness_score"])
    translations = float(row["translation_readiness_score"])
    complexity = float(row["case_complexity_score"])

    if case_type == "Asylum":
        base = 0.02 + 0.92 * origin_acceptance
        score = logit(base) + 0.09 * (risk - 5) + 0.1 * (evidence - 5) + 0.05 * (docs - 5)
    elif case_type == "Temporary Protection":
        base = 0.08 + 0.86 * origin_protection
        score = logit(base) + 0.1 * (risk - 5) + 0.06 * (docs - 5)
    elif case_type == "Family Reunification":
        score = logit(0.34) + 0.18 * (docs - 5) + 0.12 * (evidence - 5)
        score += 0.8 if row["family_ties_in_ch"] == "Yes" else -0.4
    elif case_type == "Work Permit":
        score = logit(0.32) + 0.24 * (docs - 5) + 0.12 * (translations - 5) - 0.04 * (risk - 5)
    elif case_type == "Student Permit":
        score = logit(0.42) + 0.22 * (docs - 5) + 0.14 * (translations - 5) - 0.03 * (complexity - 5)
    elif case_type == "Residence Renewal":
        score = logit(0.55) + 0.18 * (docs - 5) + 0.14 * (evidence - 5)
    elif case_type == "Citizenship":
        score = logit(0.38) + 0.2 * (docs - 5) + 0.12 * (translations - 5) - 0.12 * (complexity - 5)
    else:
        score = logit(0.28) + 0.12 * (docs - 5) + 0.1 * (evidence - 5)

    if row["legal_representation"] == "Yes":
        score += 0.38
    if row["ngo_support"] == "Yes":
        score += 0.22
    if row["lawyer_support"] == "Yes":
        score += 0.28
    if row["previous_refusal"] == "Yes":
        score -= 0.7
    if row["missed_deadline"] == "Yes":
        score -= 1.25
    if row["has_interview"] == "Yes":
        score += 0.18
    if row["interview_issue_reported"] == "Yes":
        score -= 0.55
    if row["vulnerability_flag"] == "Yes" and case_type in {"Asylum", "Temporary Protection", "Family Reunification"}:
        score += 0.45
    if row["age_range"] == "Under 18" and case_type in {"Asylum", "Family Reunification"}:
        score += 0.35

    score -= 0.16 * (complexity - 5)
    score += random.gauss(0, 0.45)
    return min(0.97, max(0.02, sigmoid(score)))


def build_rows() -> list[dict[str, object]]:
    random.seed(RANDOM_SEED)
    rows: list[dict[str, object]] = []
    start_date = date(2019, 1, 1)
    case_sequence: list[tuple[str, str | None]] = []
    for country in ORIGIN_COUNTRY_OPTIONS:
        case_sequence.extend([(country, "Asylum")] * MIN_ASYLUM_ROWS_PER_COUNTRY)
        case_sequence.extend([(country, "Family Reunification")] * MIN_FAMILY_ROWS_PER_COUNTRY)
        case_sequence.extend([(country, "Temporary Protection")] * MIN_TEMPORARY_PROTECTION_ROWS_PER_COUNTRY)
        case_sequence.extend([(country, None)] * MIN_ROWS_PER_COUNTRY)
    remaining_rows = max(0, ROW_COUNT - len(case_sequence))
    country_weights = [max(80, COUNTRY_PROFILES[country]["applications"]) for country in ORIGIN_COUNTRY_OPTIONS]
    case_sequence.extend((country, None) for country in random.choices(ORIGIN_COUNTRY_OPTIONS, weights=country_weights, k=remaining_rows))
    random.shuffle(case_sequence)

    for index, (country, forced_case_type) in enumerate(case_sequence):
        profile = COUNTRY_PROFILES[country]
        case_type = forced_case_type or choose_case_type(country)
        risk = float(profile["risk"])
        docs = bounded_normal(5.5 + random.random() * 1.3, 2.0)
        evidence = bounded_normal(4.8 + (risk - 5) * 0.15 + random.random() * 1.8, 2.1)
        translations = bounded_normal(5.2 + random.random() * 2.0, 2.0)
        complexity = bounded_normal(4.7 + (risk - 5) * 0.25 + random.random() * 1.8, 2.0)
        legal = yes_no(0.35 + 0.03 * max(0, complexity - 5))
        ngo = yes_no(0.22 + 0.035 * max(0, risk - 5))
        lawyer = "Yes" if legal == "Yes" and random.random() < 0.72 else yes_no(0.12)
        previous_refusal = yes_no(0.12 + 0.04 * max(0, complexity - 5))
        missed_deadline = yes_no(0.045 + (0.05 if previous_refusal == "Yes" else 0))
        interview = yes_no(0.72 if case_type in {"Asylum", "Temporary Protection"} else 0.42)
        interview_issue = "Yes" if interview == "Yes" and random.random() < 0.08 + 0.02 * max(0, complexity - 5) else "No"
        family_ties = yes_no(0.58 if case_type == "Family Reunification" else 0.18)
        vulnerability = yes_no(0.18 + 0.045 * max(0, risk - 5))
        age = random.choices(["Under 18", "18-25", "26-40", "41-60", "60+"], weights=[0.12, 0.2, 0.42, 0.2, 0.06], k=1)[0]
        document_completeness = DOCUMENT_COMPLETENESS[min(4, max(0, round(docs / 2.3)))]
        supporting_evidence = "Yes" if evidence >= 5.4 else "No"
        proof_supporting_claim = "Strong proof" if evidence >= 7.2 else "Some proof" if evidence >= 4.6 else "No proof yet"
        documents_translated = "Yes" if translations >= 5.6 else "No"
        translations_certified = "Yes" if translations >= 7.4 else "No"

        row = {
            "case_id": f"SYN-C-{index + 1:05d}",
            "decision_date": (start_date + timedelta(days=random.randint(0, 2550))).isoformat(),
            "year": random.choices([2019, 2020, 2021, 2022, 2023, 2024, 2025], weights=[0.08, 0.1, 0.11, 0.16, 0.18, 0.23, 0.14], k=1)[0],
            "case_type": case_type,
            "applicant_age": {"Under 18": 16, "18-25": 23, "26-40": 32, "41-60": 48, "60+": 66}[age] + random.randint(-2, 2),
            "age_range": age,
            "gender": random.choice(["Female", "Male", "Other"]),
            "country_of_origin": country,
            "applicant_nationality": country,
            "nationality_region": profile["region"],
            "origin_region": profile["region"],
            "origin_acceptance_baseline": profile["acceptance"],
            "origin_protection_baseline": profile["protection"],
            "canton": random.choice(CANTONS),
            "application_channel": random.choice(["Online", "Paper", "Legal representative", "NGO referral"]),
            "primary_language": random.choice(LANGUAGES),
            "main_language": random.choice(LANGUAGES),
            "family_status": random.choice(["Single", "Married/partnered", "With children", "Separated family", "Prefer not to say"]),
            "legal_representation": legal,
            "ngo_support": ngo,
            "lawyer_support": lawyer,
            "previous_refusal": previous_refusal,
            "has_interview": interview,
            "interpreter_provided": "Yes" if interview == "Yes" and random.random() < 0.82 else "No",
            "interview_issue_reported": interview_issue,
            "family_ties_in_ch": family_ties,
            "family_ties_in_switzerland": family_ties,
            "vulnerability_flag": vulnerability,
            "document_quality_score": docs,
            "evidence_completeness_score": evidence,
            "translation_readiness_score": translations,
            "country_risk_index": risk,
            "case_complexity_score": complexity,
            "language_proficiency_score": translations,
            "processing_duration_days": max(25, int(random.gauss(185 + 12 * complexity + 5 * risk, 70))),
            "missed_deadline": missed_deadline,
            "appeal_filed": "No",
            "new_evidence_available": "No",
            "document_completeness": document_completeness,
            "supporting_evidence": supporting_evidence,
            "proof_supporting_claim": proof_supporting_claim,
            "documents_translated": documents_translated,
            "translations_certified": translations_certified,
            "identity_documents": "Yes" if docs >= 4.5 else "No",
            "additional_documents_requested": yes_no(0.36 + 0.05 * max(0, complexity - 5)),
            "historical_acceptance_rate": 0.0,
            "historical_appeal_success_rate": 0.0,
            "similar_cases_count": 0,
            "outcome_accepted": 0,
            "appeal_success": 0,
            "model_split": "test" if index % 5 == 0 else "train",
            "notes": "Synthetic row generated from public asylum-pattern anchors; not real SEM personal data.",
        }
        probability = score_probability(row)
        accepted = 1 if random.random() < probability else 0
        row["outcome_accepted"] = accepted
        appeal_probability = sigmoid(logit(0.16) + 0.25 * (evidence - 5) + (0.55 if legal == "Yes" else 0) - (0.5 if missed_deadline == "Yes" else 0))
        row["appeal_filed"] = "Yes" if accepted == 0 and random.random() < 0.52 else "No"
        row["new_evidence_available"] = "Yes" if row["appeal_filed"] == "Yes" and random.random() < 0.38 else "No"
        row["appeal_success"] = 1 if row["appeal_filed"] == "Yes" and random.random() < appeal_probability else 0
        rows.append(row)

    key_counts = Counter((row["case_type"], row["country_of_origin"]) for row in rows)
    acceptance_by_key: dict[tuple[object, object], float] = {}
    appeal_by_key: dict[tuple[object, object], float] = {}
    for key in key_counts:
        matching = [row for row in rows if (row["case_type"], row["country_of_origin"]) == key]
        acceptance_by_key[key] = sum(int(row["outcome_accepted"]) for row in matching) / len(matching)
        appeal_by_key[key] = sum(int(row["appeal_success"]) for row in matching) / max(1, sum(1 for row in matching if row["appeal_filed"] == "Yes"))

    for row in rows:
        key = (row["case_type"], row["country_of_origin"])
        row["similar_cases_count"] = key_counts[key]
        row["historical_acceptance_rate"] = round(acceptance_by_key[key], 3)
        row["historical_appeal_success_rate"] = round(appeal_by_key[key], 3)

    return rows


def column_letter(index: int) -> str:
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def write_xlsx(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = list(rows[0])
    shared_strings: list[str] = []
    shared_index: dict[str, int] = {}

    def string_id(value: object) -> int:
        text = str(value)
        if text not in shared_index:
            shared_index[text] = len(shared_strings)
            shared_strings.append(text)
        return shared_index[text]

    sheet_rows: list[str] = []
    for row_number, values in enumerate([dict(zip(columns, columns)), *rows], start=1):
        cells: list[str] = []
        for column_number, column in enumerate(columns, start=1):
            value = values[column]
            ref = f"{column_letter(column_number)}{row_number}"
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                cells.append(f'<c r="{ref}"><v>{value}</v></c>')
            else:
                cells.append(f'<c r="{ref}" t="s"><v>{string_id(value)}</v></c>')
        sheet_rows.append(f'<row r="{row_number}">{"".join(cells)}</row>')

    shared_items = "".join(f"<si><t>{escape(text)}</t></si>" for text in shared_strings)
    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"<sheetData>{''.join(sheet_rows)}</sheetData></worksheet>"
    )
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
</Types>""")
        archive.writestr("_rels/.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>""")
        archive.writestr("xl/workbook.xml", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="Synthetic_Cases" sheetId="1" r:id="rId1"/></sheets>
</workbook>""")
        archive.writestr("xl/_rels/workbook.xml.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>""")
        archive.writestr("xl/sharedStrings.xml", f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(shared_strings)}" uniqueCount="{len(shared_strings)}">{shared_items}</sst>""")
        archive.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def main() -> None:
    rows = build_rows()
    write_xlsx(rows, OUTPUT_PATH)
    accepted = sum(int(row["outcome_accepted"]) for row in rows) / len(rows)
    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")
    print(f"Synthetic acceptance rate: {accepted:.3f}")


if __name__ == "__main__":
    main()
