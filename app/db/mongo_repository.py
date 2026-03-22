from pymongo import MongoClient
from datetime import datetime
from app.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
collection = db[settings.MONGO_COLLECTION]


def save_conversation(session_id: str, session: dict):
    document = {
        "sessionId": session_id,
        "endedAt": datetime.utcnow(),
        "scamDetected": session["scam_detected"],
        "totalMessages": session["total_messages"],
        "extractedIntelligence": {
            k: list(v) for k, v in session["extracted_intelligence"].items()
        },
        "agentNotes": session["agent_notes"],
    }

    collection.insert_one(document)
