import re

def sanitize_input(prompt: str):
    """
    Cleans and validates user input
    Returns: (clean_prompt, error_message)
    """

    # Empty input check
    if not prompt or prompt.strip() == "":
        return None, "Empty input is not allowed"

    # Reject HTML / Script directly (IMPORTANT FIX)
    if re.search(r"<.*?>", prompt):
        return None, "HTML/Script content detected"

    # SQL Injection detection
    sql_patterns = [
        r"'\s*OR\s*1=1",
        r"--",
        r";",
        r"\bDROP\b",
        r"\bSELECT\b",
        r"\bINSERT\b",
        r"\bDELETE\b",
        r"\bUPDATE\b"
    ]

    for pattern in sql_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            return None, "Potential SQL injection detected"

    # Prompt Injection detection
    suspicious_patterns = [
        "ignore previous instructions",
        "disregard above",
        "act as",
        "system prompt",
        "reveal secrets",
        "bypass",
        "ignore all rules"
    ]

    for pattern in suspicious_patterns:
        if pattern.lower() in prompt.lower():
            return None, "Potential prompt injection detected"

    # PII Detection (NEW)
    pii_patterns = [
        r"\b\d{10}\b",  # Phone number (10 digits)
        r"\b\d{12}\b",  # Aadhaar-like number
        r"\b\d{16}\b",  # Credit card-like number
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"  # Email
    ]

    for pattern in pii_patterns:
        if re.search(pattern, prompt):
            return None, "PII data detected. Please remove sensitive information."

    # Normalize whitespace (safe cleanup)
    clean_prompt = prompt.strip()

    return clean_prompt, None