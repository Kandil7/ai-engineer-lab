# Release Gate: ThanaweyaGPT (Capstone)

- **Project:** ThanaweyaGPT
- **Version:** 1.0.0
- **Created:** 2026-06-26
- **Status:** Not ready
- **Owner:** —

---

## Purpose

This checklist defines the criteria for releasing ThanaweyaGPT — the capstone project. As the final and most complex project, it requires passing criteria from all prior projects plus capstone-specific requirements.

---

## Gate Criteria

### 1. All Features Implemented

- [ ] AI Tutor chat (Arabic + English) — working end-to-end
- [ ] Question generator — generates questions by topic and difficulty
- [ ] Exam builder — creates custom exams with timer and auto-grading
- [ ] Analytics dashboard — tracks progress, identifies weak areas
- [ ] Admin panel — manages curriculum content and monitors usage
- [ ] User authentication — register, login, JWT tokens, refresh tokens
- [ ] Progress tracking — records and displays study history
- [ ] Offline support — basic Q&A available without internet

**Feature list verified by:** —
**Date:** —

### 2. Performance Benchmarks

| Metric | Target | Measured | Pass? |
|--------|--------|----------|-------|
| First response latency | < 2s | — | — |
| Question generation time | < 5s | — | — |
| Exam grading time | < 10s | — | — |
| App startup time | < 3s | — | — |
| API response time (p95) | < 1s | — | — |
| Concurrent users supported | ≥ 100 | — | — |
| Memory usage (mobile) | < 200MB | — | — |

**Test environment:** —
**Date tested:** —

### 3. Security Audit

- [ ] OWASP Top 10 checklist completed for all services
- [ ] Authentication & authorization reviewed (JWT, refresh tokens, role-based access)
- [ ] Input validation on all API endpoints
- [ ] SQL injection audit (Go backend)
- [ ] No hardcoded secrets (JWT_SECRET, API keys, database credentials)
- [ ] HTTPS enforced in production
- [ ] Rate limiting on all public endpoints
- [ ] LLM prompt injection defenses tested
- [ ] User data encryption at rest (PostgreSQL)
- [ ] PII handling compliant (student data privacy)

**Security auditor:** —
**Date completed:** —

### 4. User Acceptance Criteria

- [ ] Can register and login successfully
- [ ] Can ask a question in Arabic and receive a relevant answer
- [ ] Can ask a question in English and receive a relevant answer
- [ ] Can generate practice questions for Mathematics (Grade 12)
- [ ] Can generate practice questions for Physics (Grade 12)
- [ ] Can create a custom exam and complete it
- [ ] Can view progress dashboard with accurate data
- [ ] App works on Android 10+ and iOS 14+
- [ ] Response quality rated ≥ 4/5 by 3 test users
- [ ] No critical bugs during 1-hour usage session

**Test users:** —
**Test date:** —
**Feedback summary:** —

### 5. Code Quality

- [ ] All services have ≥ 80% test coverage
- [ ] AI code review completed with no Critical findings
- [ ] Flutter app passes `flutter analyze` with 0 errors
- [ ] Go services pass `go vet` and `staticcheck`
- [ ] Python AI service passes `ruff` and `mypy`
- [ ] No `TODO` or `FIXME` in production code
- [ ] All ADRs recorded for architectural decisions

**Code review date:** —
**Coverage report:** —

### 6. Documentation

- [ ] README.md with setup instructions for all services
- [ ] API documentation for all endpoints
- [ ] Architecture diagram updated
- [ ] Deployment guide exists
- [ ] User guide (Arabic + English)
- [ ] Developer onboarding guide
- [ ] Known limitations documented

**Documentation location:** `projects/07-capstone/thanaweyagpt/docs/`
**Date completed:** —

### 7. Infrastructure & Deployment

- [ ] Docker Compose works for full stack (all services)
- [ ] Kubernetes manifests ready (if applicable)
- [ ] CI/CD pipeline configured and passing
- [ ] Database migrations versioned and idempotent
- [ ] Health check endpoints on all services
- [ ] Graceful shutdown on all services
- [ ] Logging structured (JSON) across all services
- [ ] Monitoring dashboards configured (Prometheus + Grafana)
- [ ] Alerting configured for critical failures

**Infrastructure reviewer:** —
**Date completed:** —

### 8. RAG System Quality (AI-specific)

- [ ] Curriculum content indexed and retrievable
- [ ] Recall@5 > 0.85 on ThanaweyaGPT evaluation dataset
- [ ] Faithfulness > 0.95 (no hallucinated curriculum content)
- [ ] Arabic language support verified (retrieval + generation)
- [ ] Math formula rendering works correctly
- [ ] Physics problem step-by-step explanations verified
- [ ] Cost per query within budget

**RAG evaluation report:** —
**Date tested:** —

---

## Gate Decision

- [ ] **PASS** — All criteria met. ThanaweyaGPT is release-ready.
- [ ] **CONDITIONAL PASS** — Minor issues documented; release with monitoring.
- [ ] **BLOCK** — Critical issues found. Cannot release.

**Decision made by:** —
**Date:** —
**Rationale:** —

---

## Capstone-Specific Risks

| Risk | Mitigation | Status |
|------|-----------|--------|
| LLM hallucination in educational content | Faithfulness monitoring + curriculum grounding | — |
| Arabic language quality | Native speaker review + A/B testing | — |
| Math formula rendering failures | LaTeX validation + fallback to images | — |
| Cost overrun from LLM API calls | Budget alerts + caching + query deduplication | — |
| Student data privacy | Encryption + anonymization + compliance review | — |

---

## Notes

- This is the capstone — it should be the highest-quality release
- All prior project gates (rag-system) should be referenced
- Consider a beta release to 10 students before full launch
- Post-launch monitoring is critical for the first 30 days
- This gate criteria may evolve as the project matures
