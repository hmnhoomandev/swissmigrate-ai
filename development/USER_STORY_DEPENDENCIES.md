# SwissMigrate AI User Story Dependency Guide

This file shows the simplest execution order for the 16 core user stories.
The table below identifies which stories should come first, which can start independently, and which require earlier work.

---

## Execution table

| Story | Must wait for | Can start before | Why it matters |
|---|---|---|---|
| 1. API-first FastAPI backend | none | 2, 3, 4, 10, 11 | Foundation for all service logic and real frontend integration |
| 2. Secure authentication and RBAC | 1 | 11, 12 | Needed before storing sensitive migration data or building dashboards |
| 3. Production-grade data pipeline | 1 | 7, 11, 14, 15 | Required for semantic search, analytics, personalization, predictions |
| 4. Secure migration document vault | 1 | 5, 6, 12, 16 | Needed for safe file storage and document metadata |
| 5. Automatic letter classification and field extraction | 4 | 7, 9, 13, 14, 16 | Provides structured case data for AI, reminders, and trust features |
| 6. Deep learning OCR | 4 | 7, 13, 16 | Improves text extraction for documents, forms, handwriting, and tables |
| 7. Semantic retrieval with embeddings | 3, 5, 6 | 8, 13, 14, 15 | Core trust layer for canton-specific answers and AI grounding |
| 8. Multilingual and localized guidance | 7 | 13 | Enhances user experience once AI retrieval is reliable |
| 9. Smart reminders and deadline detection | 5 | 13 | Depends on extracted dates and case metadata |
| 10. Mobile-first PWA interface | 1 | 8 | Can begin once backend APIs exist; UI can evolve in parallel with AI work |
| 11. NGO dashboards with KPIs | 1, 2, 3 | 12 | Requires backend, auth, and analytic data infrastructure |
| 12. GDPR-ready audit logs and deletion workflows | 2, 3, 4 | 11 | Compliance layer that should be added early, alongside infrastructure |
| 13. AI legal assistant | 7, 8, 9 | 14, 15 | Advanced AI feature built on stable document and retrieval flows |
| 14. ML-based personalization | 3, 5, 7 | 15 | Requires event data and semantic understanding to tailor recommendations |
| 15. Predictive SEM and court outcome estimation | 3, 7, 14 | none | Advanced predictive service that needs mature data and explainable models |
| 16. Document authenticity validation | 3, 4, 5 | none | Trust feature that depends on secure storage and structured extraction |

---

## How to read this table

- **Must wait for**: these stories are prerequisites.
- **Can start before**: these can move forward after the story is completed.
- **No direct conflict**: none of the stories prevent another from being built, but some are clearly dependent.

---

## Simple staging plan

### Stage 1: Build platform foundation
- Story 1: API-first backend
- Story 2: Secure auth and RBAC
- Story 3: Data pipeline
- Story 4: Document vault
- Story 12: GDPR / audit workflows (early compliance)

### Stage 2: Build core intelligence
- Story 5: Letter classification and field extraction
- Story 6: Deep learning OCR
- Story 7: Semantic retrieval
- Story 8: Multilingual guidance

### Stage 3: Add product value
- Story 9: Smart reminders and deadline detection
- Story 10: Mobile-first PWA interface
- Story 11: NGO dashboards with KPIs

### Stage 4: Add advanced production features
- Story 13: AI legal assistant
- Story 14: ML-based personalization
- Story 15: Predictive SEM/court estimation
- Story 16: Document authenticity validation

---

## Key dependency notes

- **Story 1 must come first.** Without API-first architecture, the platform stays a Streamlit prototype.
- **Story 2 is required before dashboards or any shared data access.**
- **Story 3 is required for all AI, analytics, and prediction work.**
- **Story 4 must be in place before document-focused features like 5, 6, and 16.**
- **Story 7 is the core trust layer for advanced AI stories.**
- **Story 10 can begin earlier than some AI features because it is mostly UI work once APIs exist.**

---

## Practical recommendation

The team should sequence work as:
1 → 2 → 3 → 4 → 12 → 5, 6 → 7 → 8 → 9, 10, 11 → 13, 14, 15, 16

This keeps the product stable, secure, and ready for advanced intelligence without blocking parallel work where possible.
