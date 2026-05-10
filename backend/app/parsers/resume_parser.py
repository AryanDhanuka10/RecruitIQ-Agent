"""
Resume Parser — handles PDF/DOCX ingestion via PyMuPDF + LLM extraction.
"""
import fitz  # PyMuPDF
import docx
from pydantic import BaseModel, Field
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.app.security.pii_masker import mask_pii
from backend.app.security.sanitizer import sanitize
from backend.app.utils.config import settings

class CandidateProfile(BaseModel):
    name: str = Field(description="The candidate's full name")
    skills: List[str] = Field(description="List of all technical and soft skills")
    experience_years: float = Field(description="Total years of professional experience")
    experience_details: List[str] = Field(description="Details of work experience, including achievements and responsibilities")
    education: str = Field(description="Highest degree or education level obtained")
    projects: List[str] = Field(description="Key projects or roles the candidate has worked on")

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text

def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def parse_resume(file_path: str) -> dict:
    """Extracts raw text from a resume and parses it into structured JSON."""
    if file_path.lower().endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")

    # Mask PII for security/privacy before sending to LLM
    # Wait, the prompt says "Presidio setup, mask names/emails before any logging"
    # Actually, if we mask before sending to LLM, the LLM won't be able to extract the candidate's real name.
    # So we should extract using LLM on the RAW sanitized text, then we can mask the raw text if we want to log it.
    # The requirement is: "PII masked in logs." We will mask the parsed JSON if needed, or mask the raw text for logs.
    
    safe_text = sanitize(raw_text)
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=settings.groq_api_key,
        temperature=0.1,
        max_retries=2
    )
    
    structured_llm = llm.with_structured_output(CandidateProfile)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert HR extraction system. Extract structured data from the candidate's resume below."),
        ("human", "Resume Content:\n\n{text}")
    ])
    
    chain = prompt | structured_llm
    result = chain.invoke({"text": safe_text})
    
    # Return structured dict
    data = result.model_dump()
    return data
