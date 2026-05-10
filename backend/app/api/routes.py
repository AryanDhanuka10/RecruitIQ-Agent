import os
import uuid
import json
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from typing import List
from pydantic import BaseModel
from backend.app.agents.orchestrator import orchestrator_app

router = APIRouter()

# Temporary in-memory store for job statuses (use Redis/DB in prod)
jobs = {}

def process_shortlist(job_id: str, jd_path: str, resume_paths: List[str]):
    try:
        with open(jd_path, "r") as f:
            jd_text = f.read()
            
        initial_state = {
            "job_id": job_id,
            "jd_text": jd_text,
            "resume_paths": resume_paths,
            "parsed_jd": None,
            "parsed_resumes": [],
            "scored_candidates": [],
            "retries": 0
        }
        
        result = orchestrator_app.invoke(initial_state)
        
        # Save results to memory
        jobs[job_id] = {
            "status": "completed",
            "pdf_url": f"/api/v1/download/{job_id}_shortlist_report.pdf",
            "html_url": f"/api/v1/download/{job_id}_shortlist_report.html",
            "top_candidates": [c["candidate_id"] for c in result.get("scored_candidates", [])]
        }
    except Exception as e:
        jobs[job_id] = {"status": "failed", "error": str(e)}

@router.post("/shortlist")
async def create_shortlist(
    background_tasks: BackgroundTasks,
    jd_file: UploadFile = File(...),
    resume_files: List[UploadFile] = File(...)
):
    job_id = str(uuid.uuid4())
    job_dir = f"data/jobs/{job_id}"
    os.makedirs(job_dir, exist_ok=True)
    
    # Save JD
    jd_path = os.path.join(job_dir, "jd.txt")
    with open(jd_path, "wb") as f:
        f.write(await jd_file.read())
        
    # Save resumes
    resume_paths = []
    for resume in resume_files:
        path = os.path.join(job_dir, resume.filename)
        with open(path, "wb") as f:
            f.write(await resume.read())
        resume_paths.append(path)
        
    jobs[job_id] = {"status": "processing"}
    
    background_tasks.add_task(process_shortlist, job_id, jd_path, resume_paths)
    
    return {"job_id": job_id, "status": "processing"}

@router.get("/results/{job_id}")
async def get_results(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

class OverrideRequest(BaseModel):
    recommendation: str

@router.post("/override/{job_id}/{candidate_id}")
async def override_candidate(job_id: str, candidate_id: str, request: OverrideRequest):
    # In a real app, we would update the DB and regenerate the reports.
    # For now, we'll just acknowledge the override.
    return {"message": f"Candidate {candidate_id} for job {job_id} overridden to {request.recommendation}."}
