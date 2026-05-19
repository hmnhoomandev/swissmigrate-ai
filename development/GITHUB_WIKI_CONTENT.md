# SwissMigrate AI — Complete Wiki

> **SwissMigrate AI** is a local-first, secure migration assistance platform designed for migrants, asylum seekers, refugees, students, workers, and NGO staff navigating Swiss administrative processes.

---

## Table of Contents

1. [Overview](#overview)
2. [Product vision](#product-vision)
3. [MVP scope & architecture](#mvp-scope--architecture)
4. [Quick start](#quick-start)
5. [API & data](#api--data)
6. [AI system](#ai-system)
7. [Security & privacy](#security--privacy)
8. [Deployment & infrastructure](#deployment--infrastructure)
9. [Development workflow](#development-workflow)
10. [Roadmap](#roadmap)
11. [User stories (10 core features)](#user-stories-10-core-features)
12. [Glossary](#glossary)

---

## Overview

### What is SwissMigrate AI

SwissMigrate AI is an open-source, free-during-development migration support platform that helps people navigate complex Swiss migration processes securely, understand official letters, organize case files, and receive AI-assisted recommendations.

### Core capabilities

- **Document intelligence**: OCR and AI-powered analysis of migration letters and forms
- **Semantic knowledge retrieval**: Canton-specific guidance grounded in trusted sources
- **Secure case vault**: Organize and retrieve migration documents with encryption
- **Deadline management**: Automatic detection and reminders for critical dates
- **Multilingual support**: Interface and content in multiple languages
- **Role-based access**: Separate workflows for individuals, NGO staff, and administrators

### Design principles

- **Local-first & free**: Runs entirely locally during MVP; no paid services required
- **Open source**: Built transparently with community input
- **Privacy-forward**: Encryption at rest, minimal PII retention, GDPR-ready
- **Explainable AI**: All recommendations cite sources and show confidence scores
- **Secure by default**: Authentication, audit logging, and role-based access from day one

---

## Product vision

### Why this exists

Swiss migration processes are complex, time-sensitive, and language-sensitive. Migrants face:
- Difficult official letters with strict deadlines
- Canton-specific rules that change frequently
- Fragmented document management
- Limited access to trustworthy guidance
- Language and cultural barriers

SwissMigrate AI exists to reduce that friction by delivering practical, secure, and explainable support.

### Who it serves

**Primary users:**
- Migrants, asylum seekers, refugees, and students
- International workers
- NGO caseworkers and legal assistants
- Public-sector advisors and government teams

**Secondary users:**
- Product managers and policy makers
- ML engineers and security researchers
- Partner organizations and integration partners

### Success metrics

- Users successfully navigate migration tasks without professional legal help
- Documents are organized and retrievable
- Deadlines are met and no critical dates are missed
- NGO staff can manage multiple cases efficiently
- Zero unauthorized access to sensitive migration data

---

## MVP scope & architecture

### Architecture layers

```
┌─────────────────────────────────────┐
│  Frontend (React + TailwindCSS)     │  Mobile-first PWA
├─────────────────────────────────────┤
│  FastAPI Backend (Uvicorn)          │  REST APIs + OpenAPI docs
├─────────────────────────────────────┤
│  Services & Business Logic           │  Auth, RAG, OCR, storage
├─────────────────────────────────────┤
│  Data & AI Infrastructure            │  SQLite, FAISS, SentenceTransformers
├─────────────────────────────────────┤
│  Local Storage & File System         │  Documents, embeddings, models
└─────────────────────────────────────┘
```

### Technology stack (MVP)

| Layer | Technology | Why |
|-------|-----------|-----|
| **Backend** | FastAPI + Uvicorn | Async performance, auto OpenAPI docs, Python ML ecosystem |
| **Frontend** | React + TailwindCSS | Component-based, responsive, PWA-ready |
| **Database** | SQLite | Zero-config local storage; upgrade to PostgreSQL later |
| **Embeddings** | SentenceTransformers + FAISS | Free, local, deterministic |
| **OCR** | PaddleOCR | Local, multilingual, no API calls |
| **File storage** | Local filesystem | Encrypted, versioned, organized by user/case |
| **DevOps** | Docker + docker-compose | Reproducible local stack |

### API design

All endpoints follow REST conventions and return structured JSON:

```json
{
  "ok": true,
  "data": { /* result */ }
}
```

Error responses:

```json
{
  "ok": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "JWT token invalid or expired"
  }
}
```

### File structure

```
project/
├── app.py                    # FastAPI main entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Secrets template
├── docker-compose.yml       # Local stack definition
├── services/                # Business logic
│   ├── llm_service.py
│   ├── ocr_service.py
│   ├── rag_service.py
│   ├── security_service.py
│   └── storage_service.py
├── modules/                 # Feature workflows
│   ├── auth.py
│   ├── cases.py
│   ├── documents.py
│   └── dashboard.py
├── ui/                      # React frontend (later)
├── data/                    # Static data and corpus
│   ├── cantons/
│   ├── embeddings/
│   └── first_365_days/
└── tests/                   # Unit and integration tests
```

---

## Quick start

### Prerequisites

- Python 3.11+
- Node 18+ (for frontend)
- Docker & docker-compose (optional but recommended)

### Local development (backend only)

```bash
# Create venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit .env
cp .env.example .env
# Edit .env with your OpenAI key (if using) or leave blank for mock mode

# Run FastAPI
uvicorn app:app --reload --port 8000

# View API docs
# Open http://localhost:8000/docs (Swagger)
#   or http://localhost:8000/redoc (ReDoc)
```

### Full local stack (with docker-compose)

```bash
docker-compose up --build
```

This starts:
- FastAPI backend on `http://localhost:8000`
- React frontend on `http://localhost:3000` (when added)
- SQLite database (local file)
- FAISS vector store (local directory)

---

## API & data

### Core API routes

```
[Auth]
  POST   /v1/auth/register          Create user account
  POST   /v1/auth/login             Get JWT token
  POST   /v1/auth/refresh           Refresh access token
  GET    /v1/auth/me                Get current user profile

[Cases & Documents]
  POST   /v1/cases                  Create migration case
  GET    /v1/cases/{id}             Get case details
  POST   /v1/cases/{id}/documents   Upload document
  GET    /v1/cases/{id}/documents   List case documents
  DELETE /v1/cases/{id}             Delete case (with audit)

[AI & Analysis]
  POST   /v1/analyze/document       Analyze uploaded document
  POST   /v1/search/semantic        Query canton knowledge base
  GET    /v1/deadlines/upcoming     List upcoming deadlines

[Admin]
  GET    /v1/admin/audit            View audit logs
  GET    /v1/admin/users            List users (admin only)
  POST   /v1/admin/export           Export user data (GDPR)
```

### Database schema (SQLite)

```sql
-- Users & Auth
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT DEFAULT 'user',  -- user, ngo_staff, admin
  created_at DATETIME,
  updated_at DATETIME
);

-- Migration Cases
CREATE TABLE cases (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  title TEXT,
  canton TEXT,
  case_type TEXT,  -- asylum, work_permit, family_reunion, etc.
  created_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Documents & Uploads
CREATE TABLE documents (
  id TEXT PRIMARY KEY,
  case_id TEXT NOT NULL,
  filename TEXT,
  file_path TEXT,
  file_hash TEXT,
  extracted_text TEXT,
  extracted_entities JSON,  -- dates, deadlines, authorities
  upload_at DATETIME,
  FOREIGN KEY (case_id) REFERENCES cases(id)
);

-- Audit Logs
CREATE TABLE audit_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT,
  action TEXT,  -- login, upload, delete, access
  target TEXT,  -- case_id, document_id, etc.
  ip_address TEXT,
  created_at DATETIME
);

-- Reminders & Deadlines
CREATE TABLE reminders (
  id TEXT PRIMARY KEY,
  case_id TEXT NOT NULL,
  deadline_date DATE,
  description TEXT,
  sent BOOLEAN DEFAULT 0,
  FOREIGN KEY (case_id) REFERENCES cases(id)
);
```

### Embeddings & vectors

Embeddings are stored locally in `data/embeddings/`:

```
data/embeddings/
├── canton_law.faiss          # Index of canton law documents
├── first_365_days.faiss      # Index of first 365 days guidance
├── faq.faiss                 # Index of FAQ content
└── metadata.json             # Embedding metadata (source, date)
```

Each embedding is generated using `sentence-transformers/all-MiniLM-L6-v2` and cached for consistency.

---

## AI system

### Components

| Component | Purpose | Details |
|-----------|---------|---------|
| **OCR** | Extract text from scanned documents | PaddleOCR; supports handwriting and complex layouts |
| **PII masking** | Remove sensitive data before analysis | Regex + NLP-based detection |
| **Document classification** | Detect letter type and urgency | ML model (scikit-learn) with confidence scores |
| **Field extraction** | Extract dates, authorities, case IDs | NER + structured extraction rules |
| **Semantic retrieval** | Find relevant canton content | Embeddings + FAISS vector search |
| **Response generation** | Generate answers with sources | LLM with in-context retrieval (RAG) |
| **Outcome estimation** | Predict SEM/court decision | Scikit-learn models; experimental; requires legal disclaimer |

### Design principles

1. **Grounded in sources**: Every answer cites retrieved documents
2. **Confidence-aware**: Surface uncertainty and disclaimer where needed
3. **Explainable**: Show why a recommendation was made
4. **Language-aware**: Detect and process text in source language
5. **Privacy-first**: Mask PII before AI inference

### Mock mode (offline development)

Set `LLM_MOCK=true` in `.env` to use deterministic canned responses for testing and offline development without API calls.

---

## Security & privacy

### Authentication & authorization

- **JWT tokens**: Signed access + refresh tokens; 15-min expiry
- **Password hashing**: bcrypt with salt rounds = 12
- **Roles**: `user`, `ngo_staff`, `legal_assistant`, `admin`
- **Protected endpoints**: All routes require valid JWT (except `/auth/login`, `/auth/register`)

### Encryption & storage

- **In transit**: TLS 1.2+ for all connections
- **At rest**: Encrypt sensitive fields (case notes, PII) using `cryptography` library
- **Keys**: Store encryption keys in `.env`, use environment variables, never commit secrets

### Audit & compliance

- **Audit logs**: All access to cases, documents, and deletions are logged
- **Retention policy**: User data retained for 7 years (configurable via `.env`)
- **Export & delete**: Users can export all their data or request deletion (GDPR Article 17)
- **Consent tracking**: Record user consent for data processing

### GDPR controls

```
GET /v1/users/me/export       # Download all user data as ZIP
POST /v1/users/me/delete      # Request account deletion
GET /v1/admin/audit           # View audit logs (admin only)
```

---

## Deployment & infrastructure

### Local development

```bash
# Run FastAPI directly (with auto-reload)
uvicorn app:app --reload --port 8000

# Run React dev server (in ui/ folder)
npm run dev

# Run tests
pytest tests/

# Format & lint
black services/ modules/ utils/
isort services/ modules/ utils/
```

### Production-ready setup (future)

1. **Database**: Migrate to PostgreSQL with connection pooling
2. **Storage**: Use S3-compatible object storage (MinIO or AWS S3)
3. **Vector DB**: Upgrade to Pinecone, Weaviate, or Milvus
4. **Frontend**: Build React with Vite; host on CDN
5. **Scaling**: FastAPI + Gunicorn + load balancer; async workers for heavy tasks
6. **Monitoring**: Prometheus + Grafana for metrics; ELK stack for logs

### Docker deployment

```dockerfile
# Dockerfile (simplified)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml (local development)
version: '3.9'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SQLALCHEMY_DATABASE_URL=sqlite:///./data/app.db
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    volumes:
      - ./data:/app/data
  frontend:
    build: ./ui
    ports:
      - "3000:3000"
```

---

## Development workflow

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make changes following code style guidelines
4. Run tests: `pytest tests/`
5. Submit a PR with clear description and link to user story

### Code quality

- **Formatter**: Black (line length 88)
- **Import sort**: isort
- **Linter**: Pylint or flake8
- **Tests**: pytest with > 80% coverage for `services/` and `modules/`

### PR checklist

- [ ] Tests pass: `pytest`
- [ ] Code is formatted: `black` + `isort`
- [ ] No secrets in code or commits
- [ ] Documentation updated (wiki, docstrings, inline comments)
- [ ] User story reference included in PR title

---

## Roadmap

### Phase 1 (MVP) — Weeks 1–8

**Goal:** Core infrastructure + basic features

- Story 1: API-first FastAPI backend
- Story 2: Secure auth & RBAC
- Story 5: Secure document vault
- Story 4: AI document intelligence (OCR + extraction)
- Basic UI placeholder

### Phase 2 (Enhanced) — Weeks 9–16

**Goal:** Production-ready AI + user experience

- Story 3: Semantic retrieval & knowledge engine
- Story 6: Smart deadlines & reminders
- Story 8: Mobile-first PWA
- Story 9: GDPR audit infrastructure
- Advanced UI & mobile responsiveness

### Phase 3 (Future) — Weeks 17+

**Goal:** Predictive intelligence & enterprise features

- Story 7: Outcome estimation (experimental)
- Story 10: Production data pipeline
- Advanced personalization & ML monitoring
- Document authenticity validation
- NGO dashboards & KPI reporting

### Principles

- Deliver in vertical slices (backend + feature + storage)
- Keep AI grounded with sources
- Make every feature testable and auditable
- Avoid advanced features before infrastructure exists

---

## User stories (10 core features)

*See separate document: `USER_STORIES_FORMATTED.md` for full details on each story.*

Each story includes:
1. Standard user story template
2. Current situation & why improvement is needed
3. Important considerations
4. Definition of done
5. Implementation notes

**List of 10 core stories:**

1. API-First Backend Architecture
2. Secure Authentication & Role-Based Access Control
3. Semantic Retrieval & AI Knowledge Engine
4. AI-Powered Document Intelligence
5. Secure Migration Case Vault
6. Smart Deadline & Action Assistant
7. SEM & Federal Court Outcome Estimation
8. Mobile-First Progressive Web Application (PWA)
9. GDPR-Ready Privacy & Audit Infrastructure
10. Production AI & Data Pipeline

---

## Glossary

| Term | Definition |
|------|-----------|
| **RAG** | Retrieval-Augmented Generation; uses retrieved documents to ground AI responses |
| **RBAC** | Role-Based Access Control; restricts data access by user role |
| **JWT** | JSON Web Token; stateless authentication credential |
| **SEM** | Swiss State Secretariat for Migration |
| **PII** | Personally Identifiable Information; sensitive data requiring protection |
| **FAISS** | Facebook AI Similarity Search; local vector database |
| **Vector DB** | Database storing dense embeddings for semantic search |
| **Embeddings** | Numerical representations of text; used for semantic similarity |
| **Canton** | Swiss administrative region (26 total) |
| **PWA** | Progressive Web App; web app with app-like capabilities |
| **GDPR** | General Data Protection Regulation (EU/Swiss privacy law) |
| **OCR** | Optical Character Recognition; extract text from images/scans |
| **NER** | Named Entity Recognition; identify persons, dates, authorities in text |
| **Uvicorn** | ASGI server for running FastAPI |
| **TLS** | Transport Layer Security; encrypted network communication |

---

**Last updated:** May 2026  
**Maintained by:** SwissMigrate AI team  
**License:** Open source (TBD)

- **SEM** — State Secretariat for Migration
- **RAG** — Retrieval-Augmented Generation
- **PWA** — Progressive Web App
- **RBAC** — Role-Based Access Control
- **GDPR** — General Data Protection Regulation
- **OCR** — Optical Character Recognition
- **Embedding** — vector representation of text for semantic search

---

## Notes

This document is intended to represent the project as a real startup-grade product.
It separates what exists now from what is planned and what is future.
It is a practical guide for engineers, product owners, and stakeholders.
