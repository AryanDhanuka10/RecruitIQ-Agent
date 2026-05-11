"""
Rubric definitions — weights, descriptors, Pydantic output models.
Dimensions: Skills Match (30%), Experience (25%), Education (15%),
            Project/Portfolio (20%), Communication (10%)
"""
from pydantic import BaseModel, Field
from typing import Optional

class DimensionScore(BaseModel):
    score: float = Field(..., ge=0, le=10)
    justification: str

class CandidateScore(BaseModel):
    candidate_id: str
    skills_match: DimensionScore
    experience_relevance: DimensionScore
    education_certs: DimensionScore
    project_portfolio: DimensionScore
    communication_quality: DimensionScore
    weighted_total: float
    recommendation: str          # HIRE | MAYBE | NO_HIRE
    confidence: float = Field(..., ge=0.0, le=1.0)   # 🆕 novelty: confidence layer
    red_flags: list[str] = []    # 🆕 novelty: surfaced anomalies

WEIGHTS = {
    "skills_match": 0.30,
    "experience_relevance": 0.25,
    "project_portfolio": 0.20,
    "education_certs": 0.15,
    "communication_quality": 0.10
}
