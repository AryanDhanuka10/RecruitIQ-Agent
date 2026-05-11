"""
Human-in-the-loop override logger — stores HR adjustments with reason.
"""
import json, datetime

def log_override(candidate_id: str, dimension: str, old_score: float,
                 new_score: float, reason: str, log_path: str = "data/outputs/overrides.jsonl"):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "candidate_id": candidate_id,
        "dimension": dimension,
        "old_score": old_score,
        "new_score": new_score,
        "reason": reason,
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
