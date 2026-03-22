from datetime import datetime

from app.core.memory_store import (
    get_session,
    append_message,
    add_intelligence,
    add_agent_note,
)
from app.core.scam_detector import detect_scam
from app.core.intelligence_extractor import extract_intelligence
from app.core.strategy_engine import decide_strategy
from app.core.agent_brain import generate_reply
from app.services.guvi_callback import send_final_result
from app.config import settings


def process_message(request_data: dict) -> dict:
    session_id = request_data["sessionId"]
    incoming_msg = request_data["message"]

    # ------------------ Normalize timestamp ------------------
    ts = incoming_msg.get("timestamp")
    if isinstance(ts, int):  # epoch milliseconds (GUVI)
        incoming_msg["timestamp"] = datetime.utcfromtimestamp(ts / 1000).isoformat()
    elif ts is None:
        incoming_msg["timestamp"] = datetime.utcnow().isoformat()

    # ------------------ Load / Create Session ------------------
    session = get_session(session_id)

    # Save incoming scammer message
    append_message(session_id, incoming_msg)

    # ------------------ Scam Detection ------------------
    if not session["scam_detected"]:
        is_scam = detect_scam(incoming_msg["text"])
        if is_scam:
            session["scam_detected"] = True
            add_agent_note(session_id, "Scam intent detected")

    # ------------------ Agent Engagement ------------------
    agent_reply = "Okay, can you explain more?"

    if session["scam_detected"]:
        # ---- Extract intelligence ----
        intel = extract_intelligence(incoming_msg["text"])
        for key, values in intel.items():
            if values:
                add_intelligence(session_id, key, values)

        # ---- Decide engagement strategy ----
        strategy = decide_strategy(
            session["messages"],
            session["extracted_intelligence"]
        )

        # ---- Generate human-like reply ----
        agent_reply = generate_reply(strategy, session["messages"])

        # Save agent reply as user message
        append_message(
            session_id,
            {
                "sender": "user",
                "text": agent_reply,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

        add_agent_note(session_id, f"Strategy used: {strategy}")

    # ------------------ GUVI Callback Logic ------------------
    intel_store = session["extracted_intelligence"]
    total_msgs = session["total_messages"]
    total_intel_items = sum(len(v) for v in intel_store.values())

    if (
        session["scam_detected"]
        and not session["callback_sent"]
        and total_msgs >= settings.MAX_MESSAGES_BEFORE_CALLBACK
        and total_intel_items >= settings.MIN_INTEL_ITEMS_FOR_CALLBACK
    ):
        payload = {
            "sessionId": session_id,
            "scamDetected": True,
            "totalMessagesExchanged": total_msgs,
            "extractedIntelligence": {
                k: list(v) for k, v in intel_store.items()
            },
            "agentNotes": " | ".join(session["agent_notes"]),
        }

        success = send_final_result(payload)
        if success:
            session["callback_sent"] = True
            add_agent_note(session_id, "GUVI callback sent successfully")

    # ------------------ FINAL API RESPONSE ------------------
    # IMPORTANT: evaluator expects only status + reply
    return {
        "status": "success",
        "reply": agent_reply
    }
