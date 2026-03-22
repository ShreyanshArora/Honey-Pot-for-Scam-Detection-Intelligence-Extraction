import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # ================== API SECURITY ==================
    API_KEY: str = os.getenv("API_KEY", "your_default_api_key")

    # ================== LLM / AGENT ==================
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")

    # ================== SCAM DETECTION ==================
    SCAM_KEYWORD_THRESHOLD: int = 2

    # ================== GUVI CALLBACK ==================
    GUVI_CALLBACK_URL: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    CALLBACK_TIMEOUT_SECONDS: int = 5

    # ================== AGENT CONTROL ==================
    MAX_MESSAGES_BEFORE_CALLBACK: int = 6
    MIN_INTEL_ITEMS_FOR_CALLBACK: int = 1

    # ================== MONGODB (NEW) ==================
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB: str = os.getenv("MONGO_DB", "honeypot")
    MONGO_COLLECTION: str = os.getenv("MONGO_COLLECTION", "conversations")


settings = Settings()
