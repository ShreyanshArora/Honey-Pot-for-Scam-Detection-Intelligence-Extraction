<div align="center">

# 🍯 Agentic Honey-Pot
### AI-Powered Scam Detection & Intelligence Extraction

[![API](https://img.shields.io/badge/Live_API-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://honey-pot-for-scam-detection.onrender.com/docs)
[![Frontend](https://img.shields.io/badge/Live_Demo-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://honey-pot-frontend.vercel.app/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

*Engage scammers. Extract intelligence. Prevent fraud.*

</div>

---

## 📖 Overview

**Agentic Honey-Pot** is an AI-powered system that fights scams by doing something traditional spam filters can't — *talking back*. Instead of simply blocking scam messages, it simulates genuine human responses to safely lure and extract high-value intelligence from scam senders: phone numbers, bank accounts, UPI IDs, phishing links, and more.

This intelligence can then be used for fraud analysis, reporting, and prevention at scale.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **AI Scam Detection** | Real-time classification of scam intent |
| 💬 **Conversational Engagement** | Multi-turn human-like responses to scammers |
| 🧠 **Session Memory** | Maintains context across a full conversation |
| 🔍 **Intelligence Extraction** | Pulls phones, accounts, UPI IDs, links & keywords |
| 📦 **Data Persistence** | Sessions saved to MongoDB for analytics |
| 📡 **External Callbacks** | Optional integration with evaluator systems (GUVI) |
| 🖥️ **Demo UI** | Live React frontend for interactive testing |

---

## 🏗️ Architecture

```
 Scammer Message
       │
       ▼
 ┌─────────────────────┐
 │   FastAPI  /honeypot │
 └──────────┬──────────┘
            │
       ┌────▼────┐
       │  Scam   │
       │Detector │
       └────┬────┘
            │
    ┌───────▼────────┐
    │ Strategy Engine │
    └───────┬─────────┘
            │
      ┌─────▼──────┐
      │ Agent Brain │
      └─────┬───────┘
            │
  ┌─────────▼──────────┐
  │ Intelligence Extract│
  └─────────┬───────────┘
            │
   ┌────────▼─────────┐
   │  MongoDB  Session │
   │      Store        │
   └────────┬──────────┘
            │
   ┌────────▼──────────┐
   │ GUVI Callback (opt)│
   │  + Demo UI         │
   └────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **API Backend** | FastAPI |
| **Language** | Python 3.13 |
| **AI / LLM** | Groq API (LLaMA-3.1-8B Instant) |
| **Database** | MongoDB |
| **Frontend** | React (Vercel hosted) |
| **Deployment** | Render + Vercel |
| **Key Deps** | requests, python-dotenv, pydantic, uvicorn, regex |

---

## 📋 API Reference

### `POST /honeypot` — Official Endpoint

> Requires API key authentication via header.

**Headers**
```
x-api-key: <YOUR_API_KEY>
Content-Type: application/json
```

**Request**
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked. Provide otp now.",
    "timestamp": 1690000000000
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

**Response**
```json
{
  "status": "success",
  "reply": "...",
  "scamDetected": true,
  "totalMessagesExchanged": 3,
  "extractedIntelligence": {
    "phoneNumbers": ["+91-9876543210"],
    "bankAccounts": ["1234567890123456"],
    "upiIds": ["scammer@fakebank"],
    "emailAddresses": ["scam@fake.com"],
    "phishingLinks": ["http://fake-site.com"],
    "suspiciousKeywords": ["urgent", "verify now"]
  },
  "agentNotes": "Scam intent detected | Strategy used: ..."
}
```

---

### `POST /demo-chat` — Demo UI Endpoint

> No API key required. Used by the React frontend.

Same request format as `/honeypot`. Response wraps data inside a `debug` object:

```json
{
  "status": "success",
  "reply": "...",
  "debug": {
    "scamDetected": true,
    "totalMessagesExchanged": 2,
    "extractedIntelligence": { "..." : "..." },
    "agentNotes": "..."
  }
}
```

---

### `POST /end-chat` — End & Persist Session

**Request**
```json
{
  "sessionId": "unique-session-id"
}
```

**Response**
```json
{
  "status": "ended",
  "sessionId": "unique-session-id",
  "message": "Conversation saved and session closed"
}
```

Calls `save_conversation()` to persist the full session to MongoDB.

---

## 🔍 Intelligence Extraction

### Extracted Fields

| Field | Pattern Matched |
|---|---|
| `phoneNumbers` | Indian formats with/without `+91` |
| `bankAccounts` | Numeric sequences of 13–18 digits |
| `upiIds` | UPI handles (`name@bank`) |
| `emailAddresses` | Standard email format |
| `phishingLinks` | URLs starting with `http`/`https` |
| `suspiciousKeywords` | Predefined scam keyword list |

### Example — Full Extraction

**Input message:**
```
URGENT: Your SBI account 1234567890123456 is suspended.
Send OTP to +91-9876543210 and confirm your UPI scammer.fraud@fakebank immediately.
Click here to update KYC: http://fake-bank-verification.com/login
```

**Extracted intelligence:**
```json
{
  "bankAccounts":        ["1234567890123456"],
  "phoneNumbers":        ["+91-9876543210"],
  "upiIds":              ["scammer.fraud@fakebank"],
  "emailAddresses":      ["fakebank@gmail.com"],
  "phishingLinks":       ["http://fake-bank-verification.com/login"],
  "suspiciousKeywords":  ["urgent", "suspended", "verify now", "immediately"]
}
```

---

## 🧠 Agent Logic

The agent doesn't just detect — it strategically engages:

```
1. detect_scam()       →  Classify scam intent from message
2. extract_intel()     →  Pull any intelligence found so far
3. decide_strategy()   →  Choose the best engagement approach
4. generate_reply()    →  Craft a convincing human-like response
5. loop               →  Continue multi-turn conversation
```

---

## 🚀 Local Setup

### 1. Clone

```bash
git clone https://github.com/yourusername/agentic-honeypot.git
cd agentic-honeypot
```

### 2. Configure Environment

Create a `.env` file in the root:

```env
API_KEY=Honeypot_Aaron_2026_neuralink
OPENAI_API_KEY=your_openai_key
MODEL_NAME=gpt-4o-mini
MONGODB_URI=mongodb+srv://...
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open API Docs

```
http://localhost:8000/docs
```

---

## 🧪 Testing Guide (Postman)

Simulate a multi-turn scam conversation step by step.

**Turn 1 — Initial Contact**
```json
{
  "sessionId": "session1",
  "message": {
    "sender": "scammer",
    "text": "Your account has been blocked",
    "timestamp": 1650000000000
  }
}
```

**Turn 2+ — Continue the thread**

Keep using the same `sessionId` and pass increasingly specific scam content to trigger full intelligence extraction.

---

## 📈 MongoDB Analytics

Every saved session includes:
- Full conversation history
- Extracted intelligence
- Agent notes & strategy used
- Engagement metrics

This unlocks analytics like:

- 📞 Top scam phone numbers
- 🌐 Frequent phishing domains
- 🔥 Keyword heatmaps
- 🕸️ Scammer network graphs

---

## ☁️ Deployment

| Environment | URL |
|---|---|
| 📘 API Docs | [honey-pot-for-scam-detection.onrender.com/docs](https://honey-pot-for-scam-detection.onrender.com/docs) |
| 🖥️ Demo Frontend | [honey-pot-frontend.vercel.app](https://honey-pot-frontend.vercel.app/) |

---

## 📦 Submission Checklist

- [x] Public API URL
- [x] Valid API Key
- [x] GitHub Repo with complete code & README
- [x] Demo UI URL

---

## 👨‍💻 Contributors

| Name | Role |
|---|---|
| **Aaron Rao** | Project Lead |
| **Aditi Karn** | Contributor |
| **Abhinand Meethele Valappil** | Contributor |
| **Shreyansh Arora** | Contributor |

*Built by the Neuralink Team*

---

## 📄 License

This project is licensed under the **MIT License** — feel free to adapt and extend.

---

<div align="center">
  <sub>Made with ❤️ to fight scams, one conversation at a time.</sub>
</div>