"""
RecruitIQ Agent — FastAPI entry point
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from backend.app.api.routes import router

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="RecruitIQ Agent API",
    description="AI-powered HR shortlisting agent",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
os.makedirs("data/reports", exist_ok=True)
app.mount("/api/v1/download", StaticFiles(directory="data/reports"), name="reports")

app.include_router(router, prefix="/api/v1")

@app.get("/")
@limiter.limit("5/minute")
def health(request: Request):
    return {"status": "ok", "service": "RecruitIQ Agent"}
