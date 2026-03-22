from fastapi import APIRouter
from pymongo import MongoClient
from collections import Counter
from app.config import settings

router = APIRouter(prefix="/admin", tags=["Admin Analytics"])

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
collection = db[settings.MONGO_COLLECTION]


@router.get("/stats")
def get_stats():
    conversations = list(collection.find())

    total = len(conversations)
    scam_count = sum(1 for c in conversations if c.get("scamDetected"))

    upi_counter = Counter()
    phone_counter = Counter()
    keyword_counter = Counter()

    for c in conversations:
        intel = c.get("extractedIntelligence", {})
        upi_counter.update(intel.get("upiIds", []))
        phone_counter.update(intel.get("phoneNumbers", []))
        keyword_counter.update(intel.get("suspiciousKeywords", []))

    return {
        "totalConversations": total,
        "scamConversations": scam_count,
        "nonScamConversations": total - scam_count,
        "topUpiIds": upi_counter.most_common(5),
        "topPhoneNumbers": phone_counter.most_common(5),
        "topKeywords": keyword_counter.most_common(5),
    }


@router.get("/recent")
def recent_conversations(limit: int = 5):
    docs = (
        collection.find({}, {"_id": 0})
        .sort("endedAt", -1)
        .limit(limit)
    )

    return list(docs)
