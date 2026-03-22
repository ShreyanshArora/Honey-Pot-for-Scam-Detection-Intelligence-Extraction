from app.utils.regex_patterns import SUSPICIOUS_KEYWORDS
from app.config import settings


def detect_scam(text: str) -> bool:
    """
    Simple scoring-based scam detection.
    Counts suspicious keywords and returns True if threshold crossed.
    """
    text_lower = text.lower()
    score = 0

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in text_lower:
            score += 1

    # Extra signals
    if "http://" in text_lower or "https://" in text_lower:
        score += 1

    if "otp" in text_lower:
        score += 1

    if "upi" in text_lower:
        score += 1

    return score >= settings.SCAM_KEYWORD_THRESHOLD
