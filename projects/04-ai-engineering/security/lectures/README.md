# AI Security Lecture Series

## Overview

This directory contains a comprehensive 10-part lecture series on AI Security, covering the essential topics every AI engineer must understand to build secure, trustworthy AI systems. Each lecture includes detailed explanations, code examples, common pitfalls, and practice exercises. Companion glossary files provide quick reference for all key terms.

## What This Directory Contains

```
lectures/
├── README.md                                    # This file
├── 01-prompt-injection-lecture.md               # Lecture 1: Prompt Injection Attacks
├── 01-prompt-injection-glossary.md              # Glossary 1: Prompt Injection Terms
├── 02-content-moderation-lecture.md             # Lecture 2: Content Moderation
├── 02-content-moderation-glossary.md            # Glossary 2: Content Moderation Terms
├── 03-input-validation-lecture.md               # Lecture 3: Input Validation
├── 03-input-validation-glossary.md              # Glossary 3: Input Validation Terms
├── 04-output-filtering-lecture.md               # Lecture 4: Output Filtering
├── 04-output-filtering-glossary.md              # Glossary 4: Output Filtering Terms
├── 05-data-privacy-lecture.md                   # Lecture 5: Data Privacy & Protection
├── 05-data-privacy-glossary.md                  # Glossary 5: Data Privacy Terms
├── 06-authentication-authorization-lecture.md   # Lecture 6: Authentication & Authorization
├── 06-authentication-authorization-glossary.md  # Glossary 6: Auth Terms
├── 07-api-security-lecture.md                   # Lecture 7: API Security
├── 07-api-security-glossary.md                  # Glossary 7: API Security Terms
├── 08-model-security-lecture.md                 # Lecture 8: Model Security
├── 08-model-security-glossary.md                # Glossary 8: Model Security Terms
├── 09-infrastructure-security-lecture.md        # Lecture 9: Infrastructure Security
├── 09-infrastructure-security-glossary.md       # Glossary 9: Infrastructure Terms
├── 10-security-monitoring-lecture.md            # Lecture 10: Security Monitoring & Incident Response
└── 10-security-monitoring-glossary.md           # Glossary 10: Monitoring Terms
```

## All 10 Lecture Topics

| # | Topic | Lecture | Glossary | Key Focus |
|---|-------|---------|----------|-----------|
| 1 | **Prompt Injection** | [Lecture](01-prompt-injection-lecture.md) | [Glossary](01-prompt-injection-glossary.md) | Direct/indirect injection, jailbreaking, defense strategies |
| 2 | **Content Moderation** | [Lecture](02-content-moderation-lecture.md) | [Glossary](02-content-moderation-glossary.md) | Toxicity detection, NSFW filtering, policy enforcement |
| 3 | **Input Validation** | [Lecture](03-input-validation-lecture.md) | [Glossary](03-input-validation-glossary.md) | Sanitization, schema validation, adversarial inputs |
| 4 | **Output Filtering** | [Lecture](04-output-filtering-lecture.md) | [Glossary](04-output-filtering-glossary.md) | PII redaction, content filtering, safe completion |
| 5 | **Data Privacy** | [Lecture](05-data-privacy-lecture.md) | [Glossary](05-data-privacy-glossary.md) | GDPR, anonymization, differential privacy, federated learning |
| 6 | **Authentication & Authorization** | [Lecture](06-authentication-authorization-lecture.md) | [Glossary](06-authentication-authorization-glossary.md) | API keys, OAuth, RBAC, JWT tokens |
| 7 | **API Security** | [Lecture](07-api-security-lecture.md) | [Glossary](07-api-security-glossary.md) | Rate limiting, encryption, OWASP Top 10 |
| 8 | **Model Security** | [Lecture](08-model-security-lecture.md) | [Glossary](08-model-security-glossary.md) | Adversarial attacks, model theft, poisoning |
| 9 | **Infrastructure Security** | [Lecture](09-infrastructure-security-lecture.md) | [Glossary](09-infrastructure-security-glossary.md) | Container security, secrets management, network policies |
| 10 | **Security Monitoring** | [Lecture](10-security-monitoring-lecture.md) | [Glossary](10-security-monitoring-glossary.md) | Logging, alerting, incident response, forensics |

## Recommended Learning Order

The lectures are designed to be taken in order (01-10), as each builds on concepts from earlier lectures. However, you can also use them as standalone references.

### Phase 1: Foundation (Lectures 1-3)
Start here to understand the core attack vectors and basic defenses.

- **Lecture 1** — Understand how attackers manipulate AI inputs
- **Lecture 2** — Learn to detect and filter harmful content
- **Lecture 3** — Master input validation as the first line of defense

### Phase 2: Defense in Depth (Lectures 4-6)
Build layered protections around your AI systems.

- **Lecture 4** — Filter and sanitize AI outputs before they reach users
- **Lecture 5** — Protect user data and maintain privacy compliance
- **Lecture 6** — Control who can access your AI systems and what they can do

### Phase 3: System Security (Lectures 7-9)
Secure the infrastructure that runs your AI systems.

- **Lecture 7** — Protect your APIs from common attack patterns
- **Lecture 8** — Defend your models against adversarial manipulation
- **Lecture 9** — Harden your infrastructure and deployment pipeline

### Phase 4: Operational Security (Lecture 10)
Monitor, detect, and respond to security incidents.

- **Lecture 10** — Build observability and incident response capabilities

## How to Use Lectures + Glossaries Together

1. **First Pass**: Read the lecture for deep understanding. Highlight terms you don't know.
2. **Glossary Lookup**: After reading each lecture, review the companion glossary to solidify definitions.
3. **Code Along**: Type out and run the code examples yourself. Modify them to test edge cases.
4. **Practice Exercises**: Complete the exercises at the end of each lecture before moving on.
5. **Quick Reference**: Use glossary files as quick reference cards when working on real projects.

### Study Technique: Lecture + Glossary Pairing

```
For each topic:
  1. Read the lecture (30-45 min)
  2. Review the glossary (10-15 min)
  3. Complete practice exercises (30-60 min)
  4. Re-read glossary for terms you struggled with (5 min)
  5. Move to next topic
```

## Study Schedule

### Option A: Intensive (2 weeks)
One lecture per day, with practice exercises.

| Day | Lecture | Focus |
|-----|---------|-------|
| Mon | Lecture 01 | Prompt Injection |
| Tue | Lecture 02 | Content Moderation |
| Wed | Lecture 03 | Input Validation |
| Thu | Lecture 04 | Output Filtering |
| Fri | Lecture 05 | Data Privacy |
| Mon | Lecture 06 | Authentication & Authorization |
| Tue | Lecture 07 | API Security |
| Wed | Lecture 08 | Model Security |
| Thu | Lecture 09 | Infrastructure Security |
| Fri | Lecture 10 | Security Monitoring |
| Sat | Review | Revisit weak areas |
| Sun | Project | Build a secure AI endpoint |

### Option B: Part-time (4 weeks)
Two lectures per week, with extra time for exercises and projects.

| Week | Days | Lectures |
|------|------|----------|
| 1 | Mon/Thu | L01 + L02 |
| 2 | Mon/Thu | L03 + L04 |
| 3 | Mon/Thu | L05 + L06 |
| 4 | Mon/Thu | L07 + L08 |
| 5 | Mon/Thu | L09 + L10 |
| 6 | Any | Review & Project |

### Option C: Reference
Use individual lectures as needed when working on specific security challenges. Keep glossary files bookmarked for quick lookup.

## Prerequisites

### Technical Prerequisites
- **Python proficiency**: All code examples use Python 3.9+
- **Basic ML knowledge**: Understanding of how LLMs work at a high level
- **Web development basics**: HTTP, REST APIs, JSON
- **Command line**: Comfortable with terminal operations

### Recommended Background
- **Familiarity with LLM APIs**: Experience with OpenAI, Anthropic, or similar APIs
- **Basic security concepts**: Understanding of terms like "vulnerability," "exploit," "attack surface"
- **Docker basics**: For infrastructure security examples (Lecture 9)
- **Cloud fundamentals**: AWS/GCP/Azure basics (Lecture 9)

### Required Tools
```bash
# Python 3.9+
python --version

# pip packages used across lectures
pip install openai anthropic pydantic flask fastapi uvicorn
pip install hashlib secrets jwt cryptography
pip install pytest bandit safety
```

## Additional Resources

- **Exercises Directory**: See `../exercises/` for hands-on security labs
- **OWASP AI Security**: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- **NIST AI RMF**: https://www.nist.gov/artificial-intelligence/risk-management-framework
- **MITRE ATLAS**: https://atlas.mitre.org/

## Contributing

When updating these lectures:
1. Keep code examples working and tested
2. Update glossary terms when adding new concepts
3. Include real-world examples and recent incidents
4. Reference the latest OWASP/CWE/CVE databases
5. Test all exercises before committing

---

*Part of the [AI Engineer Lab](../../) curriculum.*
