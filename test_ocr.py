# test_ocr.py

from pathlib import Path
from services.ocr_service import extract_text_from_upload

class FakeUpload:
    def __init__(self, filepath):
        self.name = Path(filepath).name
        self.filepath = filepath

    def getvalue(self):
        return Path(self.filepath).read_bytes()


pdf = FakeUpload("test_documents/Appeal Response.pdf")

text, warnings = extract_text_from_upload(pdf)

print("TEXT:")
print(text)

print("\nWARNINGS:")
print(warnings)