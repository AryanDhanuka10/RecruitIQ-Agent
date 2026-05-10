import os
import time
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_pipeline():
    print("\nStarting API Pipeline Test...")
    
    # 1. Health check
    response = client.get("/")
    assert response.status_code == 200
    print("Health check OK.")
    
    # 2. Start Shortlist Job
    jd_path = "data/sample_jds/senior_ml_engineer.txt"
    resume_dir = "data/sample_resumes"
    resumes = [os.path.join(resume_dir, f) for f in os.listdir(resume_dir) if f.endswith(".pdf")]
    
    with open(jd_path, "rb") as jd:
        files = [
            ("jd_file", ("jd.txt", jd, "text/plain"))
        ]
        # Have to do this because File(...) for List[UploadFile] expects multiple fields with the same name
        resume_handles = []
        for r in resumes:
            f = open(r, "rb")
            resume_handles.append(f)
            files.append(("resume_files", (os.path.basename(r), f, "application/pdf")))
            
        print("Sending POST /api/v1/shortlist...")
        response = client.post("/api/v1/shortlist", files=files)
        
        # Cleanup handles
        for f in resume_handles:
            f.close()
            
    assert response.status_code == 200
    data = response.json()
    job_id = data.get("job_id")
    print(f"Received Job ID: {job_id}")
    assert job_id is not None
    
    # 3. Poll Results
    max_retries = 30
    delay = 2
    for _ in range(max_retries):
        print(f"Polling GET /api/v1/results/{job_id}...")
        res = client.get(f"/api/v1/results/{job_id}")
        assert res.status_code == 200
        res_data = res.json()
        if res_data.get("status") == "completed":
            print("Job completed successfully!")
            print(f"PDF URL: {res_data.get('pdf_url')}")
            print(f"Top Candidates: {res_data.get('top_candidates')}")
            break
        elif res_data.get("status") == "failed":
            print(f"Job failed: {res_data.get('error')}")
            break
        time.sleep(delay)
    else:
        print("Polling timeout.")
        
    # 4. Override test
    candidate_id = "John Doe"
    override_res = client.post(
        f"/api/v1/override/{job_id}/{candidate_id}",
        json={"recommendation": "HIRE"}
    )
    assert override_res.status_code == 200
    print("Override successful:", override_res.json())

if __name__ == "__main__":
    test_api_pipeline()
