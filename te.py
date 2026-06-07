# final_test.py

from services.document_classifier_service import DocumentClassifierService
from services.field_extraction_service import FieldExtractionService

letter = """
State Secretariat for Migration (SEM)

Case Number: SEM-2026-123456

Please submit the following documents:

- Passport copy
- Residence permit copy

The documents must be submitted before 30.06.2026.

Failure to respond may affect your application.


"""

print("\nFIELDS")
print(FieldExtractionService.extract_all(letter))