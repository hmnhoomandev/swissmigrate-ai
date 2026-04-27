from io import BytesIO


def extract_text_from_upload(uploaded_file) -> tuple[str, list[str]]:
    if uploaded_file is None:
        return "", []

    warnings = []
    name = uploaded_file.name.lower()
    payload = uploaded_file.getvalue()

    if name.endswith(".pdf"):
        try:
            import pdfplumber

            with pdfplumber.open(BytesIO(payload)) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
            text = "\n\n".join(page.strip() for page in pages if page.strip())
            if text:
                return text, warnings
            warnings.append("No selectable text found in the PDF. OCR may be required.")
        except Exception as exc:
            warnings.append(f"PDF extraction failed: {exc}")

    try:
        from PIL import Image
        import pytesseract

        image = Image.open(BytesIO(payload))
        return pytesseract.image_to_string(image), warnings
    except Exception as exc:
        warnings.append(
            "Image OCR is unavailable. Install Pillow, pytesseract, and the Tesseract system package. "
            f"Details: {exc}"
        )
        return "", warnings
