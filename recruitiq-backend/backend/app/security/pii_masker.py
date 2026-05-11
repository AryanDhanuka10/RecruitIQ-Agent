"""
PII Masker — masks personal identifiers before logging / sending to cloud LLM.
Uses Presidio Analyzer (offline, no external call).
"""
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Initialize globally to avoid reloading the model on every call
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def mask_pii(text: str) -> str:
    """Detects and masks PII in the given text."""
    # Entities to mask
    entities = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "LOCATION", "ORGANIZATION"]
    
    # Analyze text
    results = analyzer.analyze(text=text, entities=entities, language="en")
    
    # Define anonymization operators
    operators = {
        "PERSON": OperatorConfig("replace", {"new_value": "[NAME]"}),
        "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[EMAIL]"}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[PHONE]"}),
        "LOCATION": OperatorConfig("replace", {"new_value": "[LOCATION]"}),
        "ORGANIZATION": OperatorConfig("replace", {"new_value": "[ORG]"})
    }
    
    # Anonymize
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    )
    
    return anonymized_result.text
