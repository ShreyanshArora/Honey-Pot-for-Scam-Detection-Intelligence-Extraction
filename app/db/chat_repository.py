import sqlite3
import json
from datetime import datetime

DB_PATH = "chats.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            session_id TEXT PRIMARY KEY,
            ended_at TEXT,
            scam_detected INTEGER,
            total_messages INTEGER,
            bank_accounts TEXT,
            upi_ids TEXT,
            phone_numbers TEXT,
            phishing_links TEXT,
            suspicious_keywords TEXT,
            agent_notes TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_conversation(session_id: str, session: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    intel = session["extracted_intelligence"]

    cur.execute("""
        INSERT OR REPLACE INTO conversations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        datetime.utcnow().isoformat(),
        int(session["scam_detected"]),
        session["total_messages"],
        json.dumps(list(intel.get("bankAccounts", []))),
        json.dumps(list(intel.get("upiIds", []))),
        json.dumps(list(intel.get("phoneNumbers", []))),
        json.dumps(list(intel.get("phishingLinks", []))),
        json.dumps(list(intel.get("suspiciousKeywords", []))),
        " | ".join(session["agent_notes"])
    ))

    conn.commit()
    conn.close()
