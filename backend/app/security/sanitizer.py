"""
Input sanitizer — strips prompt injection patterns before sending to LLM.
"""
import re

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all prior",
    r"system prompt",
    r"jailbreak",
    r"disregard",
    r"<\|.*?\|>",     # token boundary tricks
]

def sanitize(text: str) -> str:
    """Removes known prompt injection patterns from user-supplied text."""
    for pattern in INJECTION_PATTERNS:
        text = re.sub(pattern, "[REDACTED]", text, flags=re.IGNORECASE)
    return text.strip()
