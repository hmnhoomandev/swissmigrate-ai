# SwissMigrate AI

SwissMigrate AI is a multilingual assistant for migrants, refugees, asylum seekers,
workers, and students in Switzerland. It helps people understand official
letters, plan their first 365 days, and find canton-specific services.

## Product Scope

The app implements the required assignment flow:

1. Language selection in native language names: فارسی, العربية, Türkçe,
   Українська, 中文, English, Español, Français.
2. Profile setup with all 26 Swiss cantons and user type.
3. Multilingual dashboard.
4. Secure Letter Helper with upload or pasted text, OCR, PII masking, AI
   summary, urgency, actions, and suggested reply.
5. First 365 Days Guide using structured canton data plus AI personalization.
6. Canton Navigator using local RAG-style retrieval over trusted canton and
   federal sources.
7. Privacy and safety layer with consent, masking, no raw document storage,
   emergency warning, and disclaimers.
8. Storage layer that saves only profiles and masked interaction summaries.

## Tech Stack

- Streamlit: fast, accessible Python UI suitable for classroom review and real
  iteration.
- OpenAI API: structured JSON outputs for letter analysis, guide
  personalization, and grounded navigation.
- pdfplumber, Pillow, pytesseract: text extraction for PDFs and images.
- CSV storage: lightweight local persistence that can later be replaced by
  SQLite, Supabase, or Google Sheets.
- JSON knowledge base: easy canton data editing without code changes.

## Architecture

```text
app.py
  modules/
    language_selection.py
    user_profile.py
    letter_helper.py
    first_365_guide.py
    canton_navigator.py
  services/
    ocr_service.py
    security_service.py
    llm_service.py
    rag_service.py
    storage_service.py
    safety_service.py
  utils/
    constants.py
    translations.py
  data/
    canton_knowledge.json
    cantons/
      README.md
  storage/
    user_profiles.csv
    interactions.csv
```

## Data Design

`data/canton_knowledge.json` contains:

- `first_365_template`: reusable settlement checklist items with topic,
  priority, timeframe, audience, and actions.
- `cantons`: one independent object per canton code.
- Each canton can define `languages`, `integration_office`, `services`, and
  `sources`.

For deeper canton customization, add `data/cantons/<code>.json`, for example
`data/cantons/zh.json`. The loader merges this override over the base canton
record, so canton data can be edited independently.

## Security Implementation

- `.env` stores `OPENAI_API_KEY`; `.env.example` documents required variables.
- Uploads require explicit consent.
- Letter and question text pass through `mask_pii` before AI processing.
- Raw uploads and raw letter text are not saved.
- The storage layer saves only profile selections and short masked summaries.
- The assistant includes low-confidence fallback behavior and emergency contact
  warnings.

## RAG Pipeline

The current RAG pipeline is local and deterministic:

1. Load selected canton data.
2. Tokenize the masked question and trusted source/service descriptions.
3. Retrieve the highest scoring context entries.
4. Pass only retrieved context to the LLM.
5. Return answer, steps, services, sources, and confidence.

This can scale to vector search by replacing `retrieve_context` in
`services/rag_service.py` with embeddings and a vector database while keeping
the UI and LLM contract stable.

## Run Locally

```bash
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

On Windows PowerShell:

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

To enable image OCR, install the Tesseract system package and make sure the
`tesseract` command is available on PATH.

## UX Improvements Included

- Language is selected before anything else and controls all UI labels.
- Canton and user type are stored once, then reused across modules.
- Letter Helper shows masked text for transparency.
- First 365 Days Guide creates actionable checkbox steps.
- Canton Navigator shows sources and warns when confidence is low.
- Settings lets users update profile choices later.

## Suggested Next Features

- Add verified datasets for all cantons with contact names, opening hours, and
  supported languages.
- Add appointment reminders with calendar export.
- Add offline printable checklists per canton.
- Add Google Sheets or SQLite persistence for classroom evaluation.
- Add vector embeddings for larger PDF and website collections.
- Add human handoff links to legal aid, health services, and social workers.
