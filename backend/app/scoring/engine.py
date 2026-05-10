"""
Scoring engine — LLM + embedding similarity hybrid scoring.
"""
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.app.scoring.rubric import CandidateScore, WEIGHTS
from backend.app.utils.config import settings

# Load model globally to avoid reloading
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def score_candidate(jd_dict: dict, resume_dict: dict) -> dict:
    """
    Scores a candidate against a JD.
    1. Computes Embedding Similarity between JD and Resume.
    2. Uses LLM to evaluate 5 dimensions and outputs CandidateScore.
    """
    
    # 1. Embedding Similarity (Hybrid Signal)
    jd_text = json.dumps(jd_dict)
    resume_text = json.dumps(resume_dict)
    
    jd_emb = embedding_model.encode([jd_text])
    resume_emb = embedding_model.encode([resume_text])
    
    similarity_score = float(cosine_similarity(jd_emb, resume_emb)[0][0])
    
    # 2. LLM Qualitative Evaluation
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=settings.groq_api_key,
        temperature=0.1,
        max_retries=2
    )
    
    structured_llm = llm.with_structured_output(CandidateScore)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert technical recruiter and HR evaluator. Score the candidate against the Job Description.\n"
                   "Evaluate the following 5 dimensions out of 10:\n"
                   "1. Skills Match\n"
                   "2. Experience Relevance\n"
                   "3. Education & Certs\n"
                   "4. Project / Portfolio\n"
                   "5. Communication Quality\n\n"
                   "Provide a justification for each score. Note any red flags (employment gaps, inconsistencies).\n"
                   "Finally, calculate a weighted total and provide a recommendation (HIRE, MAYBE, NO_HIRE) and a confidence score (0.0 to 1.0)."),
        ("human", "--- JOB DESCRIPTION ---\n{jd}\n\n--- CANDIDATE PROFILE ---\n{resume}\n\n"
                  "--- METRICS ---\nEmbedding Similarity Score: {similarity_score:.2f} (Consider this as a baseline semantic match)\n"
                  "\nPlease provide the structured evaluation.")
    ])
    
    chain = prompt | structured_llm
    
    try:
        # Candidate ID can just be their name for now
        candidate_id = resume_dict.get("name", "Unknown")
        result = chain.invoke({
            "jd": jd_text,
            "resume": resume_text,
            "similarity_score": similarity_score
        })
        
        # Ensure candidate_id is set
        result.candidate_id = candidate_id
        
        # Recalculate weighted total manually to be strictly accurate
        weighted = (
            result.skills_match.score * WEIGHTS["skills_match"] +
            result.experience_relevance.score * WEIGHTS["experience_relevance"] +
            result.project_portfolio.score * WEIGHTS["project_portfolio"] +
            result.education_certs.score * WEIGHTS["education_certs"] +
            result.communication_quality.score * WEIGHTS["communication_quality"]
        )
        result.weighted_total = round(weighted, 2)
        
        return result.model_dump()
        
    except Exception as e:
        print(f"Error scoring candidate {resume_dict.get('name')}: {e}")
        return None
