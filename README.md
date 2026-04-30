# SwissMigrate AI

SwissMigrate AI is a multilingual Streamlit assistant for migrants, refugees, asylum seekers, workers, and students in Switzerland. It helps users choose a language, set their canton and migration situation, understand official letters, follow a first-year settlement guide, and ask canton-specific questions using only trusted local source material.

The app is designed around one core principle: users can receive AI help, but the AI should stay grounded in files, canton data, and trusted sources that the project owner controls.

## Table of Contents

- [What the App Does](#what-the-app-does)
- [Current User Flow](#current-user-flow)
- [Core Modules](#core-modules)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Run Locally](#run-locally)
- [Environment Variables](#environment-variables)
- [Content and Knowledge Design](#content-and-knowledge-design)
- [First 365 Days Guide](#first-365-days-guide)
- [Canton Navigator RAG](#canton-navigator-rag)
- [Adding a PDF, Word, Text, or Markdown Source](#adding-a-pdf-word-text-or-markdown-source)
- [Letter Helper](#letter-helper)
- [Privacy, Safety, and Storage](#privacy-safety-and-storage)
- [Translations](#translations)
- [Development Notes](#development-notes)
- [Known Limitations](#known-limitations)
- [Suggested Next Steps](#suggested-next-steps)

## What the App Does

SwissMigrate AI currently includes:

- Language selection before the user enters the app.
- Profile setup with all 26 Swiss cantons.
- Migration situation selection: asylum seeker, refugee, migrant, worker, or student.
- Dashboard with the main support modules.
- Letter Helper for official letters, PDFs, images, and Word documents.
- PII masking before AI processing.
- First 365 Days Guide for settlement topics by canton and situation.
- Canton Navigator for grounded Q&A over local documents and canton data.
- Saved masked interaction history.
- Settings page to update canton, situation, and preferences later.

## Current User Flow

1. The user chooses their preferred language.
2. The user chooses a canton.
3. The user chooses their current situation.
4. The app opens the dashboard.
5. The user can open:
   - Letter Helper
   - First 365 Days Guide
   - Canton Navigator
   - History
   - Settings

The selected language, canton, and situation are reused across the app.

## Core Modules

### Letter Helper

The Letter Helper helps users understand official letters. Users can upload or paste text, then the app extracts text, masks sensitive details, and asks the AI to return structured JSON.

It can return:

- Simple explanation
- Sender/topic/date summary
- Deadline and urgency
- Action checklist
- Translation
- Masked text shown back to the user for transparency

### First 365 Days Guide

The First 365 Days Guide shows topic-based settlement guidance. The user selects topics such as housing, health insurance, education, employment, legal permits, registration, language learning, and social integration.

The guide currently reads structured Markdown guidance from the `data/first_365_days` folder structure.

### Canton Navigator

The Canton Navigator is the grounded Q&A experience. A user asks a question, and the app retrieves relevant local context before calling the AI. The AI is instructed to use only the retrieved context, not its own general memory.

The navigator can retrieve from:

- Canton JSON data
- Canton services
- Canton source records
- Markdown files
- Text files
- PDF files
- Word `.docx` files

## Tech Stack

- Python
- Streamlit
- OpenAI API
- pdfplumber for PDF text extraction
- python-docx for Word document extraction
- Pillow and pytesseract for image OCR
- spaCy for optional person-name detection during PII masking
- CSV and SQLite for local storage
- JSON and file-based content folders for editable knowledge

## Project Structure

```text
firststep-ai/
  app.py
  config.py
  requirements.txt
  README.md
  .env.example

  assets/
    brand/
    cantons/
    flags/

  data/
    canton_knowledge.json
    cantons/
      README.md
      template_canton.json
      geneva.json
      vaud.json
    documents/
    first_365_days/
      _shared/
        all/
          education/
            content.md
          housing/
            content.md
      bern/
        migrant/
          education/
            content.md
            example.pdf

  modules/
    canton_navigator.py
    dashboard.py
    first_365_guide.py
    language_selection.py
    letter_helper.py
    user_profile.py

  services/
    first_365_content_service.py
    llm_service.py
    ocr_service.py
    rag_service.py
    safety_service.py
    security_service.py
    storage_service.py
    translation_service.py

  storage/
    interactions.csv
    user_profiles.csv
    swissmigrate.db

  ui/
    brand.py
    cantons.py
    components.py
    flags.py
    sidebar.py
    styles.py

  utils/
    constants.py
    translations.py
```

## Run Locally

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

### macOS or Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Environment Variables

Create a `.env` file from `.env.example`.

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
APP_ENV=local
STORE_MASKED_INTERACTIONS=true
```

### Variable Reference

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | Recommended | Enables AI analysis, translation, and grounded answers. |
| `OPENAI_MODEL` | Optional | Model used by `services/llm_service.py`. Defaults to `gpt-4o-mini`. |
| `APP_ENV` | Optional | Local environment marker. |
| `STORE_MASKED_INTERACTIONS` | Optional | If `true`, saves masked summaries/history locally. |

If `OPENAI_API_KEY` is not configured, parts of the app still render, but AI-powered analysis and translation will fall back or show warnings.

## Content and Knowledge Design

The project has two complementary knowledge systems.

### 1. Structured Canton Data

Main file:

```text
data/canton_knowledge.json
```

This contains:

- `first_365_template`: reusable settlement checklist records.
- `cantons`: one record per canton code.
- Canton languages, integration office names, services, and source links.

Optional override files can be added here:

```text
data/cantons/<canton-code>.json
```

Example:

```text
data/cantons/zh.json
data/cantons/ge.json
data/cantons/vd.json
```

The loader merges the override file over the base canton record from `canton_knowledge.json`.

### 2. File-Based Knowledge

Main folder:

```text
data/first_365_days/
```

This folder is used by:

- First 365 Days Guide
- Canton Navigator RAG

The folder structure follows this pattern:

```text
data/first_365_days/<canton>/<user_type>/<topic>/
data/first_365_days/<canton>/_shared/<topic>/
data/first_365_days/_shared/all/<topic>/
data/first_365_days/_shared/<user_type>/<topic>/
```

## First 365 Days Guide

The First 365 Days Guide is topic-based and currently expects a Markdown content file for each displayed topic.

Preferred file:

```text
content.md
```

Example path:

```text
data/first_365_days/bern/migrant/education/content.md
```

Recommended Markdown format:

```markdown
# Education
Timeframe: Days 30-180
Priority: 7

Short practical summary for this canton, situation, and topic.

## Actions
- Contact the relevant school or education office.
- Collect certificates and previous school records.
- Ask about language or bridging support.

## Services
- [Service name](https://example.ch) - Short description.

## Sources
- [Official source](https://example.ch) - Short description.
```

If `content.md` is missing, the First 365 Days Guide shows a placeholder and tells the editor where to add the file.

## Canton Navigator RAG

The Canton Navigator retrieves context from the selected canton and user situation before calling the AI.

Retrieval priority:

1. Exact canton + exact user type
2. Exact canton + `_shared`
3. Shared content for the user type
4. Shared content for all users
5. Canton services and source links from JSON data

For example, if the user is:

```text
Canton: Bern
Situation: migrant
Topic: education
```

The navigator can read from:

```text
data/first_365_days/bern/migrant/education/
data/first_365_days/bern/_shared/education/
data/first_365_days/_shared/migrant/education/
data/first_365_days/_shared/all/education/
```

Supported RAG file formats:

```text
.md
.txt
.pdf
.docx
```

The current retriever is local and deterministic:

1. Load relevant local documents.
2. Extract text from supported files.
3. Split text into chunks.
4. Score chunks with token overlap.
5. Prefer exact canton/situation content using boost scores.
6. Pass retrieved context to the LLM.
7. Ask the LLM to answer only from that context.

The implementation lives in:

```text
services/rag_service.py
services/llm_service.py
modules/canton_navigator.py
```

## Adding a PDF, Word, Text, or Markdown Source

### Example: Add a PDF about education for Bern migrants

Put the file here:

```text
data/first_365_days/bern/migrant/education/tahsilat.pdf
```

Result:

- Canton Navigator will use `tahsilat.pdf` for Bern + migrant education questions.
- First 365 Days Guide will not display the PDF as guide content by itself.
- To show content in First 365 Days Guide, add a `content.md` in the same folder.

Recommended folder:

```text
data/first_365_days/bern/migrant/education/
  content.md
  tahsilat.pdf
```

Use `content.md` for the human-readable guide card, checklist, services, and source links. Use the PDF as deeper reference material for RAG.

### When to Use Each Folder

Use this when the file is only for one canton and one situation:

```text
data/first_365_days/bern/migrant/education/tahsilat.pdf
```

Use this when the file is for all user types in one canton:

```text
data/first_365_days/bern/_shared/education/tahsilat.pdf
```

Use this when the file is for one user type across all cantons:

```text
data/first_365_days/_shared/migrant/education/tahsilat.pdf
```

Use this when the file is general for everyone:

```text
data/first_365_days/_shared/all/education/tahsilat.pdf
```

## Topic Names

Current First 365 Days Guide topics:

```text
healthcare_insurance
housing
legal_permits
employment
education
language_learning
financial_support
public_transport
social_integration
mental_health
registration_admin
family_reunification
digital_tools
```

Use these exact folder names so both the guide and the navigator can classify content cleanly.

## Canton Names and Slugs

The app supports all 26 Swiss cantons. Most content folders use readable lowercase canton slugs, for example:

```text
bern
geneva
zurich
vaud
basel_stadt
basel_landschaft
neuchatel
st_gallen
```

The service also supports canton-code aliases where available, such as `be`, `zh`, `vd`, and `ge`.

Preferred style for new content:

```text
data/first_365_days/bern/migrant/education/content.md
```

## User Types

Supported user types:

```text
asylum_seeker
refugee
migrant
worker
student
```

Use these exact folder names.

## Letter Helper

Supported upload types:

```text
.pdf
.png
.jpg
.jpeg
.webp
.docx
```

Extraction behavior:

- PDFs with selectable text are read with `pdfplumber`.
- Scanned PDFs attempt OCR.
- Images use OCR.
- Word documents are read with `python-docx`.
- Uploaded text and extracted text are masked before AI processing.

OCR notes:

- Tesseract must be installed on the system for image OCR.
- On Windows, the code checks the common path:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

## Privacy, Safety, and Storage

Privacy behavior:

- Uploads require user consent.
- Letter text and questions are masked before AI processing.
- Sensitive values such as emails, phone numbers, IDs, IBANs, credit card-like numbers, addresses, and likely names are redacted.
- Raw uploaded files are not stored by the app.
- Saved history uses masked summaries and masked analysis data.

Storage files:

```text
storage/user_profiles.csv
storage/interactions.csv
storage/swissmigrate.db
```

Safety behavior:

- Emergency language triggers a visible warning.
- The app reminds users that it provides practical guidance, not legal or medical advice.
- Low-confidence RAG answers show a warning and encourage checking official sources or qualified advisors.

## Translations

Translation and UI strings live in:

```text
utils/translations.py
```

Current languages:

- Persian
- Arabic
- Turkish
- Ukrainian
- Chinese
- English
- Spanish
- French

Language metadata lives in:

```text
utils/constants.py
```

## Development Notes

### Important Files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit entry point and page routing. |
| `modules/canton_navigator.py` | Canton Navigator UI. |
| `modules/first_365_guide.py` | First 365 Days Guide UI. |
| `modules/letter_helper.py` | Letter upload, extraction, masking, and analysis UI. |
| `services/rag_service.py` | Local document loading and retrieval. |
| `services/llm_service.py` | OpenAI calls and JSON contracts. |
| `services/first_365_content_service.py` | First 365 content loading and Markdown parsing. |
| `services/security_service.py` | PII masking. |
| `services/storage_service.py` | CSV and SQLite persistence. |
| `ui/styles.py` | Global visual design. |
| `utils/translations.py` | UI translations. |

### Run Syntax Checks

```powershell
python -m compileall modules services utils ui
```

If Windows blocks writing to `__pycache__`, validate changed files directly:

```powershell
@'
import ast
from pathlib import Path
for name in ["app.py", "services/rag_service.py", "modules/canton_navigator.py"]:
    ast.parse(Path(name).read_text(encoding="utf-8"))
    print(f"OK {name}")
'@ | python -
```

### Start the App on a Specific Port

```powershell
streamlit run app.py --server.port 8501
```

## Current RAG Behavior in Plain Language

If a Bern migrant asks about education, the app looks first in:

```text
data/first_365_days/bern/migrant/education/
```

Then it also checks broader folders such as:

```text
data/first_365_days/bern/_shared/education/
data/first_365_days/_shared/migrant/education/
data/first_365_days/_shared/all/education/
```

If `tahsilat.pdf` is in the Bern migrant education folder, Canton Navigator can use it. If `content.md` is also there, First 365 Days Guide can display the guide content too.

## Known Limitations

- The current RAG retriever is token-overlap based, not embeddings-based.
- First 365 Days Guide displays Markdown guide content, not full PDFs.
- Canton Navigator reads PDFs at query time; very large collections may need indexing or caching later.
- OCR quality depends on scan quality and local Tesseract installation.
- The app is not a substitute for legal, medical, or emergency services.
- Some older translation strings may contain encoding artifacts and should be normalized over time.

## Suggested Next Steps

- Add verified canton content for all 26 cantons.
- Add `content.md` guide files for high-priority topics in each canton.
- Add official source PDFs and links by topic.
- Add an admin upload screen for PDFs and Word files.
- Add embeddings and a vector database for larger RAG collections.
- Add source freshness dates and review status.
- Add a content QA workflow before publishing new guidance.
- Add printable PDF checklists for First 365 Days Guide.
- Add human handoff links for legal aid, social work, health, and emergency support.

## Content Editor Checklist

Before adding a new source:

- Choose the correct canton folder.
- Choose the correct user type folder.
- Choose the correct topic folder.
- Add a short `content.md` if the First 365 Days Guide should show the content.
- Add PDF/DOCX/TXT files if Canton Navigator should use them for deeper answers.
- Prefer official or trusted sources.
- Include source links in the Markdown file when possible.
- Keep instructions practical, calm, and clear.

## Example Complete Content Folder

```text
data/first_365_days/bern/migrant/education/
  content.md
  tahsilat.pdf
  school-system-notes.docx
  useful-links.txt
```

In this example:

- `content.md` powers the First 365 Days Guide card.
- `tahsilat.pdf`, `school-system-notes.docx`, and `useful-links.txt` are available to Canton Navigator RAG.
- All files can support grounded education-related answers for Bern migrants.
