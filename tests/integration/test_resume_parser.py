import os
import json
import pytest
from backend.app.parsers.resume_parser import parse_resume
from backend.app.security.pii_masker import mask_pii

def test_resume_parser_and_masking():
    """
    Test that parses 5 generated resumes and verifies PII masking on the raw text.
    """
    resume_dir = "data/sample_resumes"
    resumes = [f for f in os.listdir(resume_dir) if f.endswith(".pdf")]
    
    assert len(resumes) == 5, "Expected 5 sample resumes to be generated."
    
    for filename in resumes:
        filepath = os.path.join(resume_dir, filename)
        
        # 1. Test parsing
        parsed_data = parse_resume(filepath)
        assert isinstance(parsed_data, dict)
        assert "name" in parsed_data
        assert "skills" in parsed_data
        
        print(f"\n--- Parsed {filename} ---")
        print(json.dumps(parsed_data, indent=2))
        
        # 2. Test PII masking (Simulating logging)
        from backend.app.parsers.resume_parser import extract_text_from_pdf
        raw_text = extract_text_from_pdf(filepath)
        masked_text = mask_pii(raw_text)
        
        # Verify that emails and phones are masked
        assert "[EMAIL]" in masked_text or "Email:  " not in raw_text
        assert "[PHONE]" in masked_text or "Phone:  " not in raw_text
        
        print(f"\n--- Masked Text for {filename} (Sample) ---")
        # Print just the first few lines of masked text
        print("\n".join(masked_text.split("\n")[:3]))

if __name__ == "__main__":
    test_resume_parser_and_masking()
