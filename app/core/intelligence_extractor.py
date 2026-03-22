import re
from typing import Dict, List
from app.utils.regex_patterns import (
    UPI_PATTERN,
    BANK_ACCOUNT_PATTERN,
    PHONE_PATTERN,
    URL_PATTERN,
    EMAIL_PATTERN,
    SUSPICIOUS_KEYWORDS,
)


def extract_intelligence(text: str) -> Dict[str, List[str]]:
    """
    Extract scam intelligence from text using regex patterns.
    Evaluator-safe, overlap-safe, production-safe.
    """

    # ---- 0) Normalize text (preserve digits & separators) ----
    normalized_text = re.sub(r"[^\w@\+\-\s:/\.]", " ", text)
    text_lower = normalized_text.lower()

    # ---- 1) Extract phone numbers FIRST ----
    phone_numbers = PHONE_PATTERN.findall(normalized_text)

    # Remove phones safely (regex-based, NOT replace)
    cleaned_text = PHONE_PATTERN.sub(" ", normalized_text)

    # ---- 2) Extract email addresses ----
    emails = EMAIL_PATTERN.findall(cleaned_text)
    cleaned_text = EMAIL_PATTERN.sub(" ", cleaned_text)

    # ---- 3) Extract bank accounts (13–18 digits) ----
    bank_accounts = BANK_ACCOUNT_PATTERN.findall(cleaned_text)

    # ---- 4) Extract UPI IDs ----
    upi_ids = UPI_PATTERN.findall(cleaned_text)

    # ---- 5) Extract URLs (use original text) ----
    urls = URL_PATTERN.findall(normalized_text)

    # ---- 6) Suspicious keywords ----
    found_keywords = [
        kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower
    ]

    # ---- 7) Deduplicate & clean ----
    def clean(values: List[str]) -> List[str]:
        return list({v.strip() for v in values if v and v.strip()})

    return {
        "bankAccounts": clean(bank_accounts),
        "upiIds": clean(upi_ids),
        "emailAddresses": clean(emails),
        "phishingLinks": clean(urls),
        "phoneNumbers": clean(phone_numbers),
        "suspiciousKeywords": clean(found_keywords),
    }
