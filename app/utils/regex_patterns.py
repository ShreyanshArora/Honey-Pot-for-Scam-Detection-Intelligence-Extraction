import re

# ------------------ PHONE NUMBERS ------------------
PHONE_PATTERN = re.compile(
    r'(?<!\d)(?:\+91[\-\s]?)?[6-9]\d{9}(?!\d)'
)

# ------------------ BANK ACCOUNT NUMBERS ------------------
BANK_ACCOUNT_PATTERN = re.compile(
    r'(?<!\d)\d{13,18}(?!\d)'
)

# ------------------ UPI IDs ------------------
UPI_PATTERN = re.compile(
    r'\b[a-zA-Z0-9._-]{2,}@[a-zA-Z]{2,}\b'
)

# ------------------ EMAIL ADDRESSES ------------------
EMAIL_PATTERN = re.compile(
    r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
)

# ------------------ URLs ------------------
URL_PATTERN = re.compile(
    r'https?://[^\s]+'
)

# ------------------ SUSPICIOUS KEYWORDS ------------------
SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify now",
    "account blocked",
    "suspended",
    "limited time",
    "click link",
    "share otp",
    "upi id",
    "bank details",
    "prize",
    "reward",
    "lottery",
    "refund",
    "kyc",
    "immediately",
    "update kyc"
]
