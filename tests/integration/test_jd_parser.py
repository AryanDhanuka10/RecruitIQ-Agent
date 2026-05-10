import os
import pytest
from backend.app.parsers.jd_parser import parse_jd

def test_jd_parser_integration():
    """
    Integration test for the JD parser.
    Requires a valid GROQ_API_KEY in the .env file.
    """
    # Load the sample JD text
    sample_path = "data/sample_jds/senior_ml_engineer.txt"
    assert os.path.exists(sample_path), f"Sample JD file not found at {sample_path}"
    
    with open(sample_path, "r") as f:
        jd_text = f.read()

    # Call the parser
    result = parse_jd(jd_text)

    # Validate output structure
    assert isinstance(result, dict), "Result should be a dictionary"
    
    # Check that expected keys are present (matching JDStructure Pydantic model)
    expected_keys = {
        "role",
        "required_skills",
        "preferred_skills",
        "min_experience_years",
        "education_requirement",
        "domain"
    }
    assert expected_keys.issubset(result.keys()), f"Missing keys in result. Found: {result.keys()}"
    
    # Check data types of parsed fields
    assert isinstance(result["role"], str)
    assert isinstance(result["required_skills"], list)
    assert isinstance(result["min_experience_years"], (int, float))
