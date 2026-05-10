# Security Risk Mitigation — RecruitIQ Agent

| Risk | Mitigation |
|------|-----------|
| Prompt Injection | `security/sanitizer.py` strips known patterns; all inputs validated |
| PII in logs | `security/pii_masker.py` via Presidio (offline); logs masked before write |
| API Key Exposure | `.env` + `python-dotenv`; `.env` in `.gitignore`; HF Secrets in prod |
| Hallucination | Pydantic structured output; confidence score; HITL override step |
| Unauthorised Access | Bearer token auth on all endpoints; rate limiting via `slowapi` |
| Data at Rest | Resume files deleted after processing in prod; temp dir used |
