<div align="center">
  <img src="https://img.icons8.com/nolan/128/artificial-intelligence.png" alt="RecruitIQ Logo" width="100"/>
  <h1>RecruitIQ Agent 🤖💼</h1>
  <p><strong>An advanced, AI-powered HR Shortlisting Pipeline and Orchestrator</strong></p>
  
  <p>
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/LangGraph-FF4F00?style=for-the-badge" alt="LangGraph" />
    <img src="https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=groq" alt="Groq" />
  </p>

  <h3><a href="https://recruit-iq-agent.vercel.app/">🌐 View Live Demo</a></h3>
</div>

---

## 🌟 Overview

**RecruitIQ Agent** is a state-of-the-art HR automation platform designed to ingest Job Descriptions alongside multiple candidate resumes (PDF/DOCX), securely evaluate them across multiple dimensions, and generate a ranked shortlist. 

Powered by **LangGraph** for robust state management and **Groq (Llama 3.1)** for lightning-fast structured LLM extraction, RecruitIQ drastically reduces the time to hire while mitigating unconscious biases through rigorous PII masking.

## ✨ Key Features

- **🔐 Enterprise-Grade Security**: Automatic PII (Personally Identifiable Information) masking via *Microsoft Presidio* before any data touches the LLM.
- **🧠 Hybrid Scoring Engine**: Combines deterministic semantic search (`SentenceTransformers`) with qualitative, multi-dimensional LLM evaluation (Skills, Experience, Education, Projects, Communication).
- **🛤️ State-Machine Orchestrator**: Built on *LangGraph*, featuring conditional routing, automatic retries for low-confidence parses, and isolated job-state management.
- **⚡ Asynchronous API**: A highly scalable *FastAPI* backend utilizing Background Tasks, protected by *SlowAPI* rate limiting.
- **🎨 Premium Interface**: A stunning, responsive *React & Vite* frontend featuring Dark Mode Glassmorphism, real-time polling animations, and a Human-in-the-Loop (HITL) override system.
- **📊 Automated Reporting**: Generates downloadable, structured HTML and PDF candidate shortlist reports via *ReportLab* and *Jinja2*.

## 🛠️ Tech Stack

| Component | Technologies Used |
| :--- | :--- |
| **Backend Framework** | FastAPI, Uvicorn, Python 3.12 |
| **AI / Orchestration** | LangGraph, LangChain, Groq (Llama 3), SentenceTransformers |
| **Security & Parsing** | Microsoft Presidio, PyMuPDF (fitz), python-docx |
| **Frontend** | React, Vite, Tailwind CSS, Lucide React, Axios |
| **Observability** | LangSmith |

## 🚀 Quick Start (Local Development)

### 1. Clone & Setup
```bash
git clone https://github.com/AryanDhanuka10/RecruitIQ-Agent.git
cd RecruitIQ-Agent
```

### 2. Backend Configuration
Create a `.env` file in the root directory and add your API keys:
```env
# Core API Keys
GROQ_API_KEY="gsk_your_groq_key_here"

# LLM Configuration
LLM_MODEL="llama-3.1-8b-instant"
LLM_TEMPERATURE=0.0

# Security
MASKING_ENABLED=True

# Observability (Optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="lsv2_your_langsmith_key_here"
LANGCHAIN_PROJECT="RecruitIQ-Agent"
```

Start the FastAPI backend:
```bash
# Install dependencies using uv
uv pip install -r requirements.txt

# Download spaCy model for PII Masking
python -m spacy download en_core_web_lg

# Boot the server
PYTHONPATH=. uvicorn backend.main:app --reload
```
*The backend will be available at `http://localhost:8000`.*

### 3. Frontend Configuration
In a new terminal, navigate to the frontend directory:
```bash
cd frontend
npm install
npm run dev
```
*The React interface will be available at `http://localhost:5173`.*

## ☁️ Deployment

This project is fully containerized and configured for modern cloud deployment:
- **Backend**: Contains a highly optimized `Dockerfile` ready for deployment to **Hugging Face Docker Spaces** or AWS ECS.
- **Frontend**: Contains a `vercel.json` routing configuration. Simply connect the `frontend/` directory to **Vercel** and set the `VITE_API_BASE_URL` environment variable to point to your deployed backend.

## 🤝 Human-in-the-Loop (HITL)
RecruitIQ is an *agentic assistant*, not an autonomous decider. Recruiters have full control to view the AI's confidence scores, review the flagged anomalies, and utilize the UI's **Force Hire** functionality to override the LLM's recommendation at any time.

---
<div align="center">
  <i>Architected & Built by Aryan Dhanuka</i>
</div>
