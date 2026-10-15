---
id: reliability_track_built
reported_by: builder
created_at: 2026-10-14T18:06:04.724Z
---

BUILT: reliability track, 5 files under D:\AI\Projects\ai-engineer-lab\projects\06-devops\reliability\
- README.md (123 lines), lectures\01-reliability-patterns-lecture.md (600, target 600-750), lectures\01-reliability-patterns-glossary.md (558, 47-term table, target 450-650), quizzes\01-reliability-patterns-quiz.md (346, 15 Q: Easy Q1,2,5,7,11; Medium Q3,4,6,8,9,10,12; Hard Q13,14,15), exercises\01-reliability-patterns.py (704).

EXERCISE DESIGN (key discovery for future agents):
- Rule engine: REL001 no timeout (critical), REL002 fixed backoff (warning), REL003 retry on 4xx/validation (warning), REL004 breaker disabled/no threshold (critical), REL005 queue maxsize<=0 (critical), REL006 side_effect without idempotency_key (critical), REL007 jitter none (warning), REL008 rate_limit bucket_key in {global,all,shared,""} (warning).
- Line resolution: _declared_line(label, marker) scans Path(__file__) for "# BAD:timeout" style marker comments placed on each pack entry line. Needles are full marker names (retry.backoff not retry) to avoid substring collisions.
- Finding dataclass fields: severity, code, line, message (field named "line", not "line_number").
- Packs are module dicts PACK_BAD / PACK_GOOD; packs define "service" plus "call" object; _call() accepts a bare config dict too, so external JSON can be either shape.
- JSON path arg: read with encoding="utf-8-sig" (Windows BOM breaks plain utf-8 in json.loads). Exits 0 clean, 1 if critical findings, 2 missing/invalid file. Findings show "line -" for files (no markers).
- GOOD pack passes clean first try: ZERO rule fixes were needed. Verified twice.
- Determinism: seeded random.Random(1729/2026) + _FakeClock class (callable returning float, .advance()). Two consecutive runs byte-identical (verified True).

DEMO OUTPUT FACTS (verified): jitter spread none=0.00s equal=3.98s full=7.96s at attempt 3 ceiling 8.0s; breaker opens after 10 failures (rate .5, min 10), allow() False while open, True after 31s cooldown -> half-open, probe success -> closed; token bucket cap 5 rate 2/s: u1 7 rapid calls = 5 allowed 2 denied, u2 own bucket True, shared "global" bucket u2 False; deadline 2.0s/0.5s slice runs attempts 1-2, refuses attempt 3.

VERIFICATION (all observed this session): py_compile 0; demo 0 (BAD 4 critical+4 warning = 8 findings, GOOD 0); CRLF pairs 0 all 5 files, no BOM; tests\repo-structure\validate.ps1 Passed:75 Failed:0 Warnings:0 exit 0; tests\knowledge\validate.ps1 Passed:11 Failed:0 exit 0.

CORRECTIONS MADE: 2 lecture typos (Dead-Lit-Danger -> Dead-Letter Queues: Capture, Inspect, Alert, Replay; Dead-LLetter -> Dead-Letter); README glossary count 50 -> 47 (measured); JSON loader utf-8 -> utf-8-sig (BOM test failed first).

GROUNDING PATHS used: llm/client.py:146,157-162,214-219,773-775; index/embeddings.py:73,246,342; retrieve/retriever.py:56; index/vector_store.py:101 (gap no timeout); api/main.py:65,146; infra/docker/docker-compose.yml:66-70,141-152 (compose is at REPO ROOT, not under devmate); ci.yml:71-77,140-154. Gaps asserted: no circuit breaker, no DLQ, no SIGTERM in devmate/src (repo-wide search). Complements: knowledge-registry data.reliability (line ~454) and system-design.failure-modes (line ~613).

NOT DONE: nothing committed (user decides); no registry entry added (validators pass without one).
