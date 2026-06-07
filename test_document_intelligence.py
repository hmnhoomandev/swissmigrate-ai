# test_document_intelligence.py

from services.document_classifier_service import DocumentClassifierService
from services.field_extraction_service import FieldExtractionService

sample_text = """
State Secretariat for Migration (SEM)

Case Number: SEM-2025-123456

Please submit the missing residence permit documents
before 15.06.2026.

Failure to respond may affect your application.
"""

classification = DocumentClassifierService.classify(sample_text)

fields = {
    "dates": FieldExtractionService.extract_dates(sample_text),
    "authorities": FieldExtractionService.extract_authorities(sample_text),
}

print("CLASSIFICATION")
print(classification)

print("\nFIELDS")
print(fields)

print(FieldExtractionService.extract_all(sample_text))