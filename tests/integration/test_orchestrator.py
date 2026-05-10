import os
import json
from backend.app.agents.orchestrator import orchestrator_app

def test_orchestrator():
    print("Starting LangGraph Orchestrator Test...")
    
    # 1. Load JD
    with open("data/sample_jds/senior_ml_engineer.txt", "r") as f:
        jd_text = f.read()
        
    # 2. Get resumes
    resume_dir = "data/sample_resumes"
    resume_paths = [os.path.join(resume_dir, f) for f in os.listdir(resume_dir) if f.endswith(".pdf")]
    
    # 3. Initial State
    initial_state = {
        "jd_text": jd_text,
        "resume_paths": resume_paths,
        "parsed_jd": None,
        "parsed_resumes": [],
        "scored_candidates": [],
        "retries": 0
    }
    
    # 4. Invoke Graph
    result = orchestrator_app.invoke(initial_state)
    
    print("\n================ FINAL RANKING ================")
    scored = result["scored_candidates"]
    for i, candidate in enumerate(scored):
        name = candidate.get("candidate_id")
        total = candidate.get("weighted_total")
        rec = candidate.get("recommendation")
        conf = candidate.get("confidence")
        print(f"{i+1}. {name} | Score: {total}/10 | Rec: {rec} | Conf: {conf:.2f}")
        
    print("\nDetailed Top Candidate:")
    if scored:
        print(json.dumps(scored[0], indent=2))

if __name__ == "__main__":
    test_orchestrator()
