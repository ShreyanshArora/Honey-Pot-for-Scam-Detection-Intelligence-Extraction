from typing import Dict, Any
from datetime import datetime

# ============================================================
# In-memory session store (ideal for hackathon & demo)
# ============================================================

SESSION_STORE: Dict[str, Dict[str, Any]] = {}


def get_session(session_id: str) -> Dict[str, Any]:
    """
    Fetch an existing session or create a new one.
    Each session is fully isolated.
    """
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = {
            "start_time": datetime.utcnow(),

            # Conversation history
            "messages": [],

            # Scam detection state
            "scam_detected": False,

            # Extracted intelligence (stored as sets to avoid duplicates)
            "extracted_intelligence": {
                "bankAccounts": set(),
                "upiIds": set(),
                "emailAddresses": set(),
                "phishingLinks": set(),
                "phoneNumbers": set(),
                "suspiciousKeywords": set(),
            },

            # Internal agent reasoning / strategy notes
            "agent_notes": [],

            # Metrics
            "total_messages": 0,

            # Callback control
            "callback_sent": False,
        }

    return SESSION_STORE[session_id]


def update_session(session_id: str, data: Dict[str, Any]) -> None:
    """
    Update arbitrary fields in a session.
    """
    if session_id in SESSION_STORE:
        SESSION_STORE[session_id].update(data)


def append_message(session_id: str, message: Dict[str, Any]) -> None:
    """
    Append a message to the conversation history.
    """
    SESSION_STORE[session_id]["messages"].append(message)
    SESSION_STORE[session_id]["total_messages"] += 1


def add_intelligence(session_id: str, intel_type: str, values) -> None:
    """
    Add extracted intelligence safely (no duplicates).
    """
    if (
        session_id in SESSION_STORE
        and intel_type in SESSION_STORE[session_id]["extracted_intelligence"]
    ):
        SESSION_STORE[session_id]["extracted_intelligence"][intel_type].update(values)


def add_agent_note(session_id: str, note: str) -> None:
    """
    Add internal agent reasoning note.
    """
    SESSION_STORE[session_id]["agent_notes"].append(note)


# ============================================================
# Engagement Metrics (NEW – REQUIRED FOR SCORING)
# ============================================================

def get_engagement_duration_seconds(session_id: str) -> int:
    """
    Returns total engagement duration in seconds.
    Used for evaluator scoring.
    """
    if session_id not in SESSION_STORE:
        return 0

    start_time = SESSION_STORE[session_id].get("start_time")
    if not start_time:
        return 0

    return int((datetime.utcnow() - start_time).total_seconds())


# ============================================================
# Session lifecycle control
# ============================================================

def delete_session(session_id: str) -> None:
    """
    Completely remove a session from memory.
    Triggered when user clicks 'End Chat'.
    """
    if session_id in SESSION_STORE:
        del SESSION_STORE[session_id]
