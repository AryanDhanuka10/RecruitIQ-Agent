# RecruitIQ Agent — Architecture

## Component Map

```
HR User
  │
  ▼
[Frontend — Vite/React/Tailwind — Vercel]
  │   REST + multipart/form-data
  ▼
[FastAPI Backend — HuggingFace Spaces Docker]
  │
  ├── /api/v1/shortlist  ──► JD Parser Agent
  │                          Resume/LinkedIn Parser
  │                          Scoring Engine (LLM + Embeddings)
  │                          Report Generator
  │
  └── /api/v1/override   ──► Override Logger (HITL)
```

## Agent Architecture: LangGraph Plan-and-Execute

Nodes: parse_jd → parse_profiles → score_candidates → generate_report
Edge: conditional retry on low-confidence scores (< 0.6)
