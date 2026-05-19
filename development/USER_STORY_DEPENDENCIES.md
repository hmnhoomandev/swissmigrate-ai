# SwissMigrate AI User Story Dependency Guide

This file shows the simplest execution order for the 10 core user stories. The table below identifies which stories should come first, which can start independently, and which require earlier work.

---

## Execution table

| Story | Must wait for | Can start before | Why it matters |
|---|---|---|---|
| 1. API-First Backend Architecture | none | 2, 5, 8 | Foundation for all backend logic, auth, and frontend integration |
| 2. Secure Authentication & Role-Based Access Control | 1 | 5, 8, 9 | Protects case data and enables protected user flows |
| 5. Secure Migration Case Vault | 1, 2 | 4, 6, 9, 10 | Provides safe storage for documents and metadata before analysis |
| 4. AI-Powered Document Intelligence | 1, 5 | 3, 6, 10 | Extracts structured case data needed for retrieval and reminders |
| 10. Production AI & Data Pipeline | 1, 4, 5 | 3, 7 | Enables reliable ingestion, embeddings, and ML model workflows |
| 3. Semantic Retrieval & AI Knowledge Engine | 1, 4, 5 | 6, 7 | Grounds AI answers in trusted documents and enables RAG workflows |
| 9. GDPR-Ready Privacy & Audit Infrastructure | 1, 2, 5 | 6, 7, 10 | Adds compliance and user rights early while data storage exists |
| 6. Smart Deadline & Action Assistant | 4, 5 | 8 | Depends on extracted deadlines and case metadata |
| 8. Mobile-First Progressive Web Application (PWA) | 1, 2 | 3, 4, 6 | UI work that can start once APIs and auth are defined |
| 7. SEM & Federal Court Outcome Estimation | 10 | none | Experimental predictive layer that depends on mature data infrastructure |

---

## How to read this table

- **Must wait for**: prerequisites required before meaningful progress can begin.
- **Can start before**: stories that can move forward after the current story completes.
- **No direct conflict**: none of the stories block another completely, but some should be sequenced to reduce rework.

---

## Recommended staging plan

### Stage 1: Foundation and security
- Story 1: API-First Backend Architecture
- Story 2: Secure Authentication & Role-Based Access Control
- Story 5: Secure Migration Case Vault
- Story 9: GDPR-Ready Privacy & Audit Infrastructure

### Stage 2: Document intelligence and data
- Story 4: AI-Powered Document Intelligence
- Story 10: Production AI & Data Pipeline
- Story 3: Semantic Retrieval & AI Knowledge Engine

### Stage 3: User value and experience
- Story 6: Smart Deadline & Action Assistant
- Story 8: Mobile-First Progressive Web Application (PWA)

### Stage 4: Experimental intelligence
- Story 7: SEM & Federal Court Outcome Estimation

---

## Key dependency notes

- **Story 1 is the core enabler.** Without an API-first backend, the platform cannot become a scalable product.
- **Story 2 must follow quickly.** Authentication and RBAC are required before storing sensitive case documents or enabling role-based access.
- **Story 5 should be in place before document-centric AI.** A secure case vault provides the data foundation for extraction, search, and reminders.
- **Story 4 unlocks later intelligence.** Document intelligence is required for semantic retrieval, deadlines, and case analysis.
- **Story 10 makes AI work reliable and repeatable.** The pipeline is the operating system for embeddings, models, and data quality.
- **Story 7 should be last.** Outcome estimation is experimental and should only be built after mature data pipelines and compliance controls.

---

## Practical recommendation

The team should sequence work as:
1 → 2 → 5 → 9 → 4 → 10 → 3 → 6 → 8 → 7

This sequence keeps the platform secure, data-driven, and ready for advanced AI while allowing UI and reminder work to move forward once APIs and storage are stable.

