"""
JD Parser — extracts skills, experience, qualifications from a JD text.
Uses structured LLM output (Pydantic).
"""
import json
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.app.security.sanitizer import sanitize
from backend.app.utils.config import settings
from backend.app.memory.cache import init_cache

# Initialize cache globally for dev
init_cache()

class JDStructure(BaseModel):
    role: str = Field(description="The job title or role")
    required_skills: List[str] = Field(description="List of required skills")
    preferred_skills: List[str] = Field(description="List of preferred or nice-to-have skills")
    min_experience_years: float = Field(description="Minimum years of experience required")
    education_requirement: str = Field(description="Education requirement, e.g., Bachelor's, Master's")
    domain: str = Field(description="The industry or domain of the job")

def parse_jd(jd_text: str) -> dict:
    """Parses a raw job description string into structured JSON."""
    
    # 1. Sanitize input to prevent prompt injection
    safe_text = sanitize(jd_text)
    
    # 2. Setup LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=settings.groq_api_key,
        temperature=0.1,
        max_retries=2
    )
    
    # 3. Setup Structured Output
    structured_llm = llm.with_structured_output(JDStructure)
    
    # 4. Setup Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert HR analyst. Extract structured requirements from the job description below."),
        ("human", "Extract from this JD:\n\n{text}")
    ])
    
    # 5. Chain and Invoke
    chain = prompt | structured_llm
    
    # Execute
    result = chain.invoke({"text": safe_text})
    
    return result.model_dump()
