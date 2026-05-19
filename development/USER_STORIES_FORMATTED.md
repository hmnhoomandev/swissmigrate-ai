# SwissMigrate AI — 10 Core User Stories (Formatted)

Each user story follows this structure:
1. **Standard user story** — As a [role], I want [feature], so that [benefit]
2. **Current situation & why improvement is needed** — Context and rationale
3. **Important considerations** — Technical and business notes
4. **Definition of done** — Acceptance criteria
5. **Additional explanations** — Implementation guidance

---

## Story 1: API-First Backend Architecture

### Standard User Story

**As a** product owner and developer  
**I want** the platform to use a FastAPI-based API-first backend architecture  
**So that** the application becomes scalable, modular, maintainable, and production-ready while remaining completely free during development and testing.

### Current Situation & Why This Improvement Is Needed

The current application is heavily dependent on **Streamlit for both frontend and backend logic**. While Streamlit is effective for rapid prototyping, it creates significant limitations:

- **Scalability**: Streamlit runs as a single process; scaling requires rebuilding the entire UI layer
- **Frontend performance**: UI logic is tightly coupled to backend; browser cannot cache or parallelize
- **State management**: Stateless server model makes session management and caching difficult
- **API integrations**: Hard to integrate external services or mobile apps
- **Authentication**: Streamlit has no built-in auth or session management
- **Mobile responsiveness**: Streamlit UI is not mobile-friendly
- **AI workflow separation**: AI pipelines are embedded in the UI layer, not isolated

### Important Considerations

- **FastAPI must become the main backend framework** — Async-first, automatic OpenAPI documentation, Python ecosystem compatibility
- **React or Vue must replace Streamlit** as the primary frontend layer — Component-based, responsive, PWA-capable
- **SQLite must be used initially** instead of PostgreSQL — Zero configuration; upgrade path to Postgres later
- **Uvicorn must run the backend locally** — ASGI application server with hot reload support
- **APIs must return structured JSON responses** — Consistent envelope with `{ "ok": bool, "data": {}, "error": {} }`
- **OpenAPI/Swagger documentation must be enabled** — Auto-generated at `/docs` and `/redoc`
- **Local `.env` configuration must manage secrets** — Never commit `.env` files; use `.env.example` template
- **AI features must support mock mode** — Set `LLM_MOCK=true` to reduce OpenAI API costs during development
- **Backend modules should remain independent and reusable** — Services can be called from CLI, tests, or scheduled tasks

### Definition of Done

- ✅ FastAPI backend is implemented with clean routers (`/auth`, `/cases`, `/documents`, `/ai`, `/admin`)
- ✅ React frontend communicates with backend APIs via HTTP (not Streamlit)
- ✅ SQLite database works locally with proper schema (users, cases, documents, audit logs)
- ✅ Swagger documentation is available at `/docs` and working for all endpoints
- ✅ File upload and retrieval work locally through REST endpoints
- ✅ Environment variables are configured securely via `.env.example`
- ✅ App runs locally without paid services (OpenAI API optional, mock mode available)
- ✅ Streamlit is no longer responsible for backend business logic
- ✅ All APIs follow REST conventions and return consistent JSON structure
- ✅ Tests exist for at least 50% of backend routes

### Additional Explanations

**Why this story is the foundation:**
- All other features (auth, RAG, document intelligence, dashboards) depend on a proper API contract
- Decoupling backend from frontend enables parallel development and faster iteration
- API-first architecture supports future integrations (mobile apps, partner platforms, CLI tools)

**Key implementation steps:**
1. Create FastAPI app with Uvicorn
2. Define SQLite schema and ORM (SQLAlchemy)
3. Implement basic CRUD routes for cases and documents
4. Set up environment configuration (`.env`, logging, error handling)
5. Enable OpenAPI documentation
6. Migrate current Streamlit logic into FastAPI services
7. Create React stub for frontend (can start with basic HTML)

**Technology checklist:**
- `fastapi` — Web framework
- `uvicorn` — ASGI server
- `sqlalchemy` — ORM for SQLite
- `pydantic` — Request/response validation
- `python-dotenv` — Environment variable management
- `pytest` — Testing framework

---

## Story 2: Secure Authentication & Role-Based Access Control

### Standard User Story

**As a** user, NGO staff member, or administrator  
**I want** secure authentication and role-based access control  
**So that** migration data remains protected and accessible only to authorized users.

### Current Situation & Why This Improvement Is Needed

The current platform has **no formal authentication or access control system**. This means:

- **Sensitive migration data is unprotected** — Anyone with network access can view or delete cases
- **No user isolation** — Multiple users cannot safely share the same instance
- **No audit trail** — Admin cannot track who accessed what data
- **No role separation** — A user cannot distinguish between personal and NGO staff views

The system must support secure login, registration, and role-based permissions without requiring paid identity platforms (OAuth, Auth0, etc.).

### Important Considerations

- **FastAPI authentication middleware must be used** — Dependency injection for protected routes
- **JWT authentication must manage sessions** — Access tokens + refresh tokens; 15-minute expiry for access, 7-day for refresh
- **Passlib and bcrypt must hash passwords** — Never store plaintext passwords; use `passlib[bcrypt]`
- **SQLite must store user accounts initially** — Upgrade to managed identity systems later
- **Roles must include**:
  - `user` — Individual migrant; access only their own cases
  - `ngo_staff` — NGO caseworker; access assigned cases and clients
  - `legal_assistant` — Specialized legal support; audit and review role
  - `admin` — Platform administrator; full access and audit logs
- **Access logs must be recorded locally** — Every action (login, upload, delete) logged to audit table
- **`.env` files must store secrets securely** — JWT secret key, encryption key; never committed to version control

### Definition of Done

- ✅ Users can register with email and password
- ✅ Users can log in and receive JWT access token
- ✅ Passwords are hashed with bcrypt (salt rounds = 12)
- ✅ JWT tokens include expiry and role information
- ✅ Protected endpoints reject unauthorized users (return 401 Unauthorized)
- ✅ Role permissions function properly (user cannot access other users' cases)
- ✅ Authentication works entirely locally (no external OAuth provider)
- ✅ Refresh token endpoint allows long-lived sessions without storing passwords
- ✅ Audit logs record login attempts, successful access, and failed authentication
- ✅ Password reset workflow exists (email-based or security questions)

### Additional Explanations

**Why this matters for migrants:**
- Migrants are vulnerable populations; data breaches can have real-world consequences (deportation, legal exposure)
- NGO staff need to manage multiple clients securely
- Legal confidentiality requires strong access controls

**Key implementation steps:**
1. Create `User` model in SQLite (id, email, password_hash, role, created_at)
2. Implement JWT token generation and validation
3. Create login endpoint that validates email/password and returns JWT
4. Add authentication dependency to FastAPI routers
5. Create RBAC middleware that checks user role for sensitive endpoints
6. Implement audit logging for all database changes
7. Add password reset workflow

**Security checklist:**
- ✅ Passwords hashed with bcrypt (never store plaintext)
- ✅ JWT tokens signed with secret key (never expose key)
- ✅ Access tokens are short-lived (15 minutes)
- ✅ Refresh tokens are long-lived (7 days) and revocable
- ✅ All password reset links are one-time use and time-limited
- ✅ Account lockout after 5 failed login attempts
- ✅ Audit logs include timestamp, user ID, IP address, action, outcome

---

## Story 3: Semantic Retrieval & AI Knowledge Engine

### Standard User Story

**As a** user seeking migration guidance  
**I want** semantic retrieval powered by embeddings and vector search  
**So that** migration answers are contextual, multilingual, and grounded in trusted sources.

### Current Situation & Why This Improvement Is Needed

Current retrieval relies on **keyword matching and weak contextual search**, which causes:

- **Inaccurate answers** — Keyword overlap doesn't mean semantic relevance (e.g., "refugee" vs. "asylum seeker" are synonyms but different keywords)
- **Weak multilingual support** — Translations don't always preserve keyword overlap
- **Poor contextual understanding** — "Deadline" in German ("Frist") doesn't match English keyword queries
- **Hallucination risks** — LLM generates plausible-sounding but incorrect answers without grounding

The system requires **semantic AI retrieval** using free local infrastructure (no paid embeddings API).

### Important Considerations

- **Sentence Transformers must generate embeddings** — Use `sentence-transformers/all-MiniLM-L6-v2` (multi-lingual, 384-dim, fast)
- **FAISS or ChromaDB must store vectors locally** — FAISS recommended for MVP (simpler, no dependencies); ChromaDB optional if you need persistence UI
- **Chunking pipelines must be implemented carefully** — Documents split into overlapping chunks (256 tokens, 50% overlap) to preserve context
- **Retrieval scores must be exposed** — Show relevance scores so users understand confidence
- **Sources must appear alongside answers** — Every answer includes retrieved document fragment and metadata (source, date, canton)
- **Embeddings must be cached locally** — Generated once, reused many times; store in `data/embeddings/`
- **OpenAI embeddings should be avoided during MVP** — Save costs by using free local embeddings

### Definition of Done

- ✅ Semantic search works locally (no API calls required)
- ✅ Similar-meaning queries retrieve relevant content (test: "asylum deadline" and "refugee deadline" return same results)
- ✅ Vector database integration works (FAISS index loads and searches in < 100ms)
- ✅ Retrieval confidence scores are visible in API responses
- ✅ Source grounding appears in responses (document fragment + source metadata)
- ✅ No paid vector infrastructure is required
- ✅ Embeddings are cached locally in `data/embeddings/`
- ✅ Multi-language support works (German, French, Italian queries retrieve English documents)
- ✅ Chunking strategy is documented and reproducible
- ✅ Retrieval evaluation metrics are defined (e.g., precision@5, recall@10)

### Additional Explanations

**Why high-quality retrieval is critical:**
- Trustworthy AI systems depend on grounded facts, not hallucination
- Legal/migration advice without citations is unreliable
- Users need to understand *why* the system recommended something

**Key implementation steps:**
1. Create chunking pipeline that splits canton documents into overlapping segments
2. Generate embeddings for all chunks using SentenceTransformers
3. Create FAISS index and save to `data/embeddings/`
4. Implement `/search/semantic` endpoint that queries FAISS and returns top-k results
5. Integrate retrieval results into RAG prompt for LLM
6. Add retrieval score and source metadata to API response
7. Create evaluation dataset to measure retrieval quality

**Vector database choice:**
- **FAISS**: Simple, fast, no dependencies, good for MVP
- **ChromaDB**: Better UX, persistence, multi-tenant support, good for production

**Embedding model evaluation:**
- `all-MiniLM-L6-v2` — Fast, multilingual, 384 dimensions (good for MVP)
- `all-mpnet-base-v2` — Higher quality, slower, 768 dimensions (optional for production)

---

## Story 4: AI-Powered Document Intelligence

### Standard User Story

**As a** user or case manager  
**I want** AI-powered document analysis and structured extraction  
**So that** migration documents can be understood automatically and efficiently.

### Current Situation & Why This Improvement Is Needed

The current system has **limited OCR and weak structured extraction**, struggling with:

- **Scanned PDFs** — Low-quality or rotated scans cannot be read
- **Forms and tables** — Complex layouts lose structure during text extraction
- **Handwritten text** — OCR often fails on handwriting
- **Special formats** — Swiss forms with specific layouts not recognized

Users must manually re-type information or work with incomplete document analysis.

### Important Considerations

- **PaddleOCR must handle OCR processing** — Free, multilingual, handles handwriting and complex layouts better than Tesseract
- **PyMuPDF must extract PDF text** — Fast PDF parsing with layout preservation
- **python-docx must process DOCX files** — Extract text and structure from Microsoft Word documents
- **Structured extraction must identify**:
  - Dates (application date, deadline, hearing date)
  - Case numbers (dossier ID, case reference)
  - Authorities (SEM, cantonal office, appeal board)
  - Required actions (what user must do and by when)
  - Document type (decision, request, summons, letter)
- **Confidence scoring must exist** — Flag low-confidence extractions for manual review
- **Low-confidence extraction must trigger warnings** — Alert user if OCR quality is poor

### Definition of Done

- ✅ OCR works locally for PDFs, images, and scanned documents
- ✅ PDF/image/document uploads work through REST endpoint
- ✅ Structured extraction works reliably (dates, case numbers, deadlines)
- ✅ Document categories are detected automatically (decision, letter, form, etc.)
- ✅ Important fields are highlighted or extracted separately
- ✅ Confidence scores show extraction reliability
- ✅ No paid OCR services (Google Cloud Vision, AWS Textract) are required
- ✅ Pipeline handles rotated, low-quality, and multilingual documents
- ✅ Extracted data is stored in structured format (JSON)
- ✅ OCR errors are logged for future model improvements

### Additional Explanations

**Why this creates real-world value:**
- Migration users often struggle most with understanding official documents
- Correct deadline extraction prevents missed appeals and legal failures
- Automatic classification saves manual triage time for NGO staff

**Key implementation steps:**
1. Create document upload endpoint that accepts PDF, image, DOCX
2. Implement OCR pipeline using PaddleOCR
3. Add PII masking (redact names, IDs, addresses)
4. Implement NER (Named Entity Recognition) for authorities, dates, case numbers
5. Create field extraction rules (regex + ML) for structured data
6. Generate confidence scores for each extracted field
7. Store original + extracted data in document table
8. Create test dataset with representative migration documents

**OCR model selection:**
- **PaddleOCR**: Best for complex layouts, multilingual, free
- **Tesseract**: Lightweight, but lower accuracy for handwriting
- **EasyOCR**: Good multilingual support, slower than PaddleOCR

**Structured extraction approach:**
1. Rule-based first (regex for dates, case number patterns)
2. NER second (identify authority names, locations)
3. ML fallback (train classifier if rule-based fails)

---

## Story 5: Secure Migration Case Vault

### Standard User Story

**As a** user or case manager  
**I want** a secure migration case vault  
**So that** my documents and migration records are safely stored and easily retrievable.

### Current Situation & Why This Improvement Is Needed

Current document storage is **fragile and unsuitable for long-term case management**:

- **Lost documents** — Files scattered across computer or email; no central location
- **No versioning** — If a file is overwritten, no way to recover previous version
- **Poor organization** — Documents not tagged or categorized
- **No backup** — Single copy means one computer failure loses all data
- **Shared access difficult** — NGO staff cannot securely view client documents

The platform needs organized storage while remaining free during MVP.

### Important Considerations

- **Local file storage must organize uploads by user ID** — Structure: `uploads/{user_id}/{case_id}/{filename}`
- **SQLite must track document metadata** — filename, upload date, document type, associated deadlines
- **Sensitive metadata should be encrypted** — Case notes, extracted PII encrypted at rest
- **Local backup/export functionality must exist** — Users can download all their data as ZIP
- **File version tracking should be supported later** — For now, simple overwrite is acceptable; prepare schema for versioning
- **Access control must be enforced** — Users can only access their own documents; NGO staff can access assigned cases only

### Definition of Done

- ✅ Users can upload files (PDF, image, DOCX, TXT)
- ✅ Files persist locally in organized directory structure
- ✅ Metadata tracking works (filename, upload date, document type, extracted entities)
- ✅ Access permissions function correctly (RBAC enforced)
- ✅ Users can list, view, and download their documents
- ✅ File deletion is soft (flagged as deleted, not immediately removed)
- ✅ Local backups can be exported (ZIP with file + metadata manifest)
- ✅ Audit logs record all document access
- ✅ File quotas prevent abuse (e.g., 500MB per user)
- ✅ No cloud storage required; everything local

### Additional Explanations

**Why this transforms the platform:**
- Transforms from temporary chatbot to persistent migration workspace
- Users can revisit case history months/years later
- NGO staff can coordinate on shared cases
- Backup/export gives users control over their data

**Key implementation steps:**
1. Create file upload endpoint (`POST /cases/{id}/documents`)
2. Implement local file storage system with directory organization
3. Add document metadata to SQLite schema
4. Implement list/download endpoints with RBAC
5. Add soft delete (flag as deleted, don't remove file)
6. Implement export endpoint that zips all user documents + manifest
7. Add disk usage tracking and quotas
8. Create audit logs for all document access

**File structure:**
```
data/uploads/
├── user_1/
│   └── case_abc/
│       ├── document_1.pdf
│       ├── document_2.jpg
│       └── metadata.json
└── user_2/
    └── case_xyz/
        ├── form_1.docx
        └── metadata.json
```

**Metadata schema:**
```json
{
  "id": "doc_123",
  "filename": "decision_letter.pdf",
  "uploaded_at": "2026-05-15T10:30:00Z",
  "document_type": "decision",
  "extracted_entities": {
    "deadline": "2026-06-15",
    "case_number": "ABC123456",
    "authority": "SEM"
  },
  "file_size": 2048,
  "file_hash": "sha256:..."
}
```

---

## Story 6: Smart Deadline & Action Assistant

### Standard User Story

**As a** user  
**I want** automatic deadline detection and action recommendations  
**So that** I do not miss important migration tasks or legal deadlines.

### Current Situation & Why This Improvement Is Needed

Users frequently miss:
- **Response deadlines** — 30-day reply windows to official letters
- **Appointments** — Scheduled interviews with SEM or cantonal authorities
- **Required submissions** — Document uploads or form submissions

Current interaction history is **passive and not actionable**. Users must manually track deadlines in calendars or notes.

### Important Considerations

- **NLP extraction must identify deadlines automatically** — Parse "within 30 days", "by 15 June", "deadline: 2026-06-30"
- **SQLite must store reminders locally** — Reminder table with deadline_date, description, sent flag
- **React dashboard widgets must display upcoming tasks** — Show top 3 upcoming actions on home screen
- **Browser notifications must provide reminders** — If user opts in, show notification 7 days before deadline
- **Recommendation logic must remain informational only** — Never give legal advice; only show "You have 7 days to respond"
- **Timezone handling required** — Store dates in UTC; display in user's local timezone
- **Recurring reminders optional** — For MVP, simple one-time deadline reminders

### Definition of Done

- ✅ Important dates are extracted automatically from documents
- ✅ Users receive reminder notifications (email or browser)
- ✅ Upcoming actions appear on dashboard (top 3 upcoming deadlines)
- ✅ Urgent tasks (within 7 days) are highlighted visually (red/orange)
- ✅ Reminder workflows function locally
- ✅ Users can dismiss or snooze reminders
- ✅ Reminders are logged in audit trail
- ✅ Timezone handling works correctly
- ✅ No paid notification services required
- ✅ Users can configure reminder preferences (email, SMS, in-app only)

### Additional Explanations

**Why even simple reminders create enormous value:**
- Missing a 30-day deadline means losing the right to appeal
- One missed deadline can change case outcome significantly
- Most vulnerable users rely on phones, not calendars

**Key implementation steps:**
1. Create deadline extraction NLP logic (regex + rule-based patterns)
2. Add reminders table to SQLite
3. Create `/deadlines/upcoming` endpoint that returns reminders for next 90 days
4. Implement email notification sender (SMTP)
5. Add browser push notifications (PWA feature)
6. Display reminders on dashboard with visual urgency indicators
7. Add snooze/dismiss functionality
8. Create audit logs for reminder interactions

**Deadline extraction patterns:**
- "within 30 days" → current_date + 30 days
- "by 15 June 2026" → 2026-06-15
- "deadline: 2026-06-30" → 2026-06-30
- "within 2 weeks" → current_date + 14 days

**Notification preferences:**
- Email notification 7 days before
- Email notification 1 day before
- In-app notification (always)
- Browser push notification (if enabled)

---

## Story 7: SEM & Federal Court Outcome Estimation

### Standard User Story

**As a** claimant or asylum seeker  
**I want** AI-assisted outcome estimation based on historical migration patterns  
**So that** I can better understand possible case outcomes and prepare realistically.

### Current Situation & Why This Improvement Is Needed

Users currently have little visibility into:
- **Likely outcomes** — What percentage of cases like mine succeed?
- **Historical trends** — Are acceptance rates rising or falling?
- **Appeal risks** — Is appealing a decision worth the effort?
- **Preparation expectations** — What should I focus on in my application?

The system requires **lightweight predictive intelligence** without expensive ML infrastructure.

### Important Considerations

- **Scikit-learn must train initial ML models** — Logistic regression, random forest, gradient boosting
- **Small local datasets must be used initially** — Start with anonymized SEM data; expand over time
- **Model inference must run locally** — No external ML API calls required
- **Confidence scores must appear** — Show prediction probability (e.g., "60% acceptance likelihood")
- **Legal disclaimers are mandatory** — Every prediction must include "This is not legal advice"
- **Explainability must exist for predictions** — Show which factors contributed to prediction
- **Model reproducibility required** — Save trained models with version info, training data hash
- **Retraining workflow must exist** — Update models monthly/quarterly as new data arrives

### Definition of Done

- ✅ Prediction prototype works locally
- ✅ Users receive informational estimates with disclaimer
- ✅ Confidence levels appear (prediction probability + uncertainty intervals)
- ✅ Historical similarity references exist (show comparable cases)
- ✅ Legal disclaimers are visible on every prediction page
- ✅ Model explainability exists (SHAP/LIME feature importance)
- ✅ No paid ML infrastructure is required
- ✅ Models are versioned and reproducible
- ✅ Predictions include key factors driving the estimate
- ✅ Validation metrics show model performance (accuracy, precision, recall)

### Additional Explanations

**Why this should remain experimental:**
- Outcome prediction is inherently uncertain; small data = low accuracy
- Legal/migration outcomes depend on many unmeasured factors
- Liability risk if predictions are taken as legal advice
- Start with low confidence and high disclaimers

**Key implementation steps:**
1. Collect and anonymize historical SEM decision data
2. Engineer features (case type, nationality, canton, representation, etc.)
3. Train baseline models (logistic regression, random forest)
4. Calculate prediction confidence and uncertainty
5. Implement `/predict/outcome` endpoint with disclaimer
6. Add feature importance explanation (SHAP values)
7. Create validation dataset to measure model performance
8. Document model training process and versioning

**Feature examples:**
- Case type (asylum, family reunion, work permit)
- Applicant nationality
- Canton of processing
- Legal representation (yes/no)
- Presence of interview
- Document quality score
- Processing duration

**Disclaimer example:**
> ⚠️ **Legal Disclaimer**
> These estimates are informational only and based on historical patterns. They are not legal advice. Actual outcomes depend on many factors including your specific circumstances, legal arguments, and officer judgment. Do not rely on these estimates for legal decisions. Consult a qualified legal professional.

---

## Story 8: Mobile-First Progressive Web Application (PWA)

### Standard User Story

**As a** user  
**I want** a mobile-first progressive web application  
**So that** I can access migration services easily from my smartphone.

### Current Situation & Why This Improvement Is Needed

Many migration users rely mainly on **smartphones rather than desktop devices**. Current UI limitations include:

- **Weak mobile responsiveness** — Layouts break on small screens
- **Confusing navigation** — Too many options, poor mobile UX patterns
- **Poor accessibility** — Small text, hard-to-hit buttons for thumbs
- **Inconsistent layouts** — Different screens look different, no design system
- **No offline capability** — App doesn't work if connection drops

The platform requires a **modern frontend optimized for mobile users** with PWA features.

### Important Considerations

- **React must power the frontend** — Component-based, performance optimized
- **TailwindCSS must manage responsive styling** — Utility-first CSS; ensures consistency
- **PWA support must allow app installation** — Add manifest.json, service worker for offline
- **Navigation must remain simple and multilingual** — Bottom nav or hamburger menu; language toggle
- **Frontend assets must remain lightweight** — Target < 50KB gzip for bundle size
- **Accessibility must meet WCAG 2.1 AA** — Keyboard navigation, screen reader support, color contrast
- **Performance targets**: Page load < 3 seconds on 4G network
- **Offline mode should cache essential pages** — Service worker pre-caches home, about, FAQ

### Definition of Done

- ✅ Mobile responsiveness works correctly (tests on iPhone, Android, tablet)
- ✅ PWA installation works (user can "add to home screen")
- ✅ Navigation is intuitive and accessible (bottom nav or side menu)
- ✅ Accessibility improvements implemented (WCAG 2.1 AA)
- ✅ App performs well on low-end devices (2GB RAM, 3G network)
- ✅ Offline mode shows cached content
- ✅ Multilingual navigation works (language toggle)
- ✅ Form inputs are mobile-friendly (large touch targets)
- ✅ Loading states and errors are visible
- ✅ Bundle size < 100KB (gzip)

### Additional Explanations

**Why PWA architecture is right for migrations:**
- Many migrants don't own personal computers
- Network connectivity varies by location (rural areas, refugee camps)
- App-like experience reduces friction vs. browser tabs
- No app store approval delays or fees

**Key implementation steps:**
1. Create React project with Vite or Create React App
2. Design responsive layout using TailwindCSS (mobile-first)
3. Implement bottom navigation or hamburger menu
4. Add PWA support (manifest.json, service worker)
5. Pre-cache critical pages and assets
6. Implement language toggle in header
7. Add accessibility features (ARIA labels, keyboard nav)
8. Test on real devices (iOS, Android, different screen sizes)

**PWA checklist:**
- ✅ manifest.json with app name, icons, colors
- ✅ Service worker for offline caching
- ✅ HTTPS enforcement
- ✅ App icons (192x192, 512x512)
- ✅ Splash screen (iOS)
- ✅ Install prompt (Android)

**Responsive breakpoints (TailwindCSS):**
```
sm: 640px   -- Phones
md: 768px   -- Tablets
lg: 1024px  -- Desktops
xl: 1280px  -- Large screens
```

---

## Story 9: GDPR-Ready Privacy & Audit Infrastructure

### Standard User Story

**As a** compliance-focused product owner  
**I want** GDPR-ready privacy controls and audit infrastructure  
**So that** user data rights and privacy requirements are respected properly.

### Current Situation & Why This Improvement Is Needed

The current platform lacks:
- **Audit logging** — No way to track who accessed what data
- **Deletion workflows** — No process for users to delete accounts
- **Consent tracking** — No record of what users consented to
- **Retention policies** — No automatic data cleanup

Migration data is **highly sensitive** and requires strong privacy controls to meet GDPR and Swiss privacy laws.

### Important Considerations

- **SQLite must store audit logs** — Every access, modification, deletion logged with timestamp, actor, target
- **User consent records must be tracked** — Record what user agreed to and when
- **Data export workflows must exist** — Endpoint `/users/me/export` returns JSON + files as ZIP
- **Account deletion workflows must exist** — Soft delete (flag as deleted); hard delete after 30-day retention
- **Python encryption libraries must secure sensitive fields** — `cryptography` package for at-rest encryption
- **Privacy policy must be documented** — Explain data usage, retention, rights
- **Retention policy must be configurable** — Via `.env`: `DATA_RETENTION_DAYS=2555` (7 years)

### Definition of Done

- ✅ Audit logs function correctly (all database changes logged)
- ✅ Users can export data (`GET /users/me/export`)
- ✅ Users can delete accounts (`POST /users/me/delete`)
- ✅ Consent tracking works (records stored with timestamp)
- ✅ Privacy workflows are documented
- ✅ Sensitive data is encrypted at rest
- ✅ Data retention policy is automated (old records deleted after N days)
- ✅ GDPR subject access request (SAR) can be fulfilled in < 30 days
- ✅ Data processor agreement (DPA) template exists
- ✅ Privacy policy is clear and accessible

### Additional Explanations

**Why this matters for migrants:**
- Migrants are vulnerable; strong privacy policies build trust
- Legal confidentiality requires strong controls
- Swiss law and GDPR require explicit consent and deletion capabilities

**Key implementation steps:**
1. Create audit_logs table that captures all database changes
2. Implement logging middleware in FastAPI
3. Create data export endpoint (JSON + files ZIP)
4. Implement soft-delete for users (deleted_at flag)
5. Add automatic hard-delete after retention period
6. Encrypt sensitive fields using `cryptography` library
7. Create privacy policy document
8. Implement consent tracking for new users
9. Add GDPR request handling (export, delete, rectify)

**Audit log schema:**
```sql
CREATE TABLE audit_logs (
  id INTEGER PRIMARY KEY,
  user_id TEXT,
  action TEXT,           -- create, read, update, delete
  resource TEXT,         -- cases, documents, users
  resource_id TEXT,
  ip_address TEXT,
  timestamp DATETIME,
  result TEXT            -- success, failure
);
```

**Sensitive fields to encrypt:**
- Case notes
- Extracted PII (names, IDs, addresses)
- Medical information
- Legal advice notes

**Export format:**
```
export_user_123.zip
├── profile.json
├── cases/
│   ├── case_abc.json
│   └── case_xyz.json
├── documents/
│   ├── document_1.pdf
│   └── document_2.jpg
└── consent_log.json
```

---

## Story 10: Production AI & Data Pipeline

### Standard User Story

**As a** developer and ML engineer  
**I want** a production-ready local AI and data pipeline  
**So that** document processing, embeddings, analytics, and ML workflows can run reliably and reproducibly.

### Current Situation & Why This Improvement Is Needed

Current AI workflows are **fragmented and manual**:

- **No automated ingestion** — Documents manually imported; no batch processing
- **No embedding pipeline** — Embeddings generated on-demand; not cached
- **Fragile preprocessing** — No standard validation or quality checks
- **No retraining workflow** — Models are static; don't improve over time
- **No monitoring** — Pipeline failures go unnoticed

The platform requires **automated, reliable AI pipelines** without expensive MLOps infrastructure (Kubernetes, MLflow, etc.).

### Important Considerations

- **Python scripts must automate ingestion workflows** — Scheduled tasks (cron or APScheduler) for batch processing
- **Local folder structures must separate**:
  - `data/raw/` — Original documents as uploaded
  - `data/processed/` — Cleaned, normalized text
  - `data/embeddings/` — Generated vectors and FAISS indices
  - `models/` — Trained model artifacts (pickle, joblib)
- **FAISS or ChromaDB must manage embeddings** — Versioned indices with metadata
- **Logging pipelines must monitor failures** — Errors logged; failures trigger alerts
- **GitHub Free must manage version control** — No paid CI/CD services required
- **Data lineage must be tracked** — Know which embeddings are from which documents

### Definition of Done

- ✅ Automated ingestion pipeline works (batch processes new documents)
- ✅ Embeddings generate automatically (scheduled daily)
- ✅ Local model retraining works (monthly refresh)
- ✅ Logs track pipeline failures
- ✅ Data folders remain organized and versioned
- ✅ Entire pipeline works locally and free
- ✅ Pipeline is reproducible (same input → same output)
- ✅ Data quality metrics are computed (embedding distribution, OCR confidence)
- ✅ Pipeline errors are logged and alertable
- ✅ Pipeline performance is monitored (runtime, throughput)

### Additional Explanations

**Why production pipelines are critical:**
- Manual processes don't scale
- Reproducibility is required for ML model validation
- Data quality directly impacts AI system quality
- Monitoring prevents silent failures

**Key implementation steps:**
1. Create `ingestion.py` script that processes new documents
2. Set up scheduling (cron or APScheduler)
3. Implement data validation and quality checks
4. Create embedding generation pipeline
5. Implement FAISS index update logic
6. Create model training script with hyperparameter logging
7. Add comprehensive logging and error handling
8. Create monitoring dashboard or alerts
9. Document pipeline architecture and data flow

**Pipeline architecture:**
```
documents uploaded
  ↓
ingestion.py (batch process)
  ↓
validate data (quality checks)
  ↓
preprocess (normalize, clean, deduplicate)
  ↓
generate embeddings (SentenceTransformers)
  ↓
update FAISS index
  ↓
log metrics (size, distribution, errors)
```

**Folder structure:**
```
data/
├── raw/                    -- Original documents
│   └── 2026-05-19/
│       ├── doc_1.pdf
│       └── doc_2.txt
├── processed/              -- Cleaned text
│   ├── texts.json
│   └── metadata.json
├── embeddings/             -- Vector indices
│   ├── canton_law.faiss
│   ├── faq.faiss
│   └── metadata.json
└── models/                 -- Trained models
    ├── doc_classifier.pkl
    └── model_metadata.json
```

**Pipeline monitoring:**
- Document ingestion rate (docs/day)
- Embedding generation time (ms/doc)
- FAISS index size (MB)
- Data quality metrics (OCR confidence, extraction success rate)
- Pipeline runtime (total hours/run)

---

## Implementation Priority Matrix

| Story | Depends On | Phase | Duration | Priority |
|-------|-----------|-------|----------|----------|
| 1. API Backend | None | 1 | 3 weeks | Critical |
| 2. Auth & RBAC | Story 1 | 1 | 2 weeks | Critical |
| 5. Document Vault | Story 1, 2 | 1 | 2 weeks | High |
| 4. Document Intelligence | Story 1, 5 | 2 | 3 weeks | High |
| 3. Semantic Retrieval | Story 4 | 2 | 2 weeks | High |
| 6. Deadlines & Reminders | Story 3, 5 | 2 | 2 weeks | Medium |
| 8. PWA Frontend | Story 2 | 2 | 3 weeks | Medium |
| 9. GDPR & Audit | Story 2, 5 | 2 | 2 weeks | High |
| 10. Data Pipeline | Story 3, 4 | 3 | 2 weeks | Medium |
| 7. Outcome Estimation | Story 10 | 3 | 3 weeks | Low |

---

**Total MVP effort:** ~12-15 weeks (estimated 2-3 developers)  
**Total with Phase 2:** ~20-24 weeks  
**Total with Phase 3:** ~25-30 weeks
