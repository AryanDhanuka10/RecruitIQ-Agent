"""
LinkedIn Profile Parser — accepts JSON export and structures it.
"""
import json
from backend.app.parsers.resume_parser import CandidateProfile

def parse_linkedin_json(linkedin_data: dict) -> dict:
    """
    Parses a raw LinkedIn JSON export and maps it to CandidateProfile structure.
    In a real scenario, this would map fields or use an LLM if unstructured.
    Here we assume it's already semi-structured and we use an LLM to standardize it.
    """
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from backend.app.utils.config import settings
    from backend.app.security.sanitizer import sanitize

    # Dump to text
    raw_text = json.dumps(linkedin_data)
    safe_text = sanitize(raw_text)
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=settings.groq_api_key,
        temperature=0.1
    )
    
    structured_llm = llm.with_structured_output(CandidateProfile)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert HR extraction system. Extract structured data from this LinkedIn JSON export."),
        ("human", "LinkedIn JSON:\n\n{text}")
    ])
    
    chain = prompt | structured_llm
    result = chain.invoke({"text": safe_text})
    
    return result.model_dump()
