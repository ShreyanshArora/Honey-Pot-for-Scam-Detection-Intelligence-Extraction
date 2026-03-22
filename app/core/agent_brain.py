from groq import Groq
import os
import random
import time

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ============================
# PERSONA PROMPT
# ============================
PERSONA_PROMPT = """
You are a normal Indian mobile user who is not very tech-savvy.

Behave like a real person chatting over SMS or WhatsApp.

Rules:
- Never reveal you suspect a scam
- Act confused, scared, greedy, or obedient
- Ask questions so the scammer reveals details (UPI, links, numbers)
- Keep responses short (1–2 sentences)
"""

# ============================
# STRATEGY HINTS
# ============================
STRATEGY_HINTS = {
    "scared": "You are scared your bank account will be blocked. Ask what to do.",
    "greedy": "You are excited about the reward. Ask how to claim it.",
    "obedient": "You trust them. Ask for steps.",
    "link_issue": "Say the link is not opening.",
    "otp_problem": "Say OTP not received.",
    "confused_delay": "Act confused and ask them to explain slowly.",
    "neutral_confused": "Say you don’t understand and ask basic questions."
}

# ============================
# FALLBACK RESPONSES (HUMAN-LIKE)
# ============================
FALLBACK_RESPONSES = {
    "scared": [
        "Mera account sach mein block ho jayega kya?",
        "Aisa kyun ho raha hai, please batao.",
    ],
    "greedy": [
        "Reward kaise milega? Kya process hai?",
        "Iske liye mujhe kya karna hoga?",
    ],
    "obedient": [
        "Theek hai, next step kya hai?",
        "Aap guide kar do, main follow karunga.",
    ],
    "link_issue": [
        "Link open nahi ho raha, koi aur way hai?",
        "Website load nahi ho rahi.",
    ],
    "otp_problem": [
        "OTP abhi tak nahi aaya.",
        "OTP dobara bhej sakte ho?",
    ],
    "confused_delay": [
        "Samajh nahi aa raha, thoda simple bolo.",
        "Slowly explain kar sakte ho?",
    ],
    "neutral_confused": [
        "Yeh kaise hota hai?",
        "Iska matlab kya hai?",
    ],
}

# ============================
# FALLBACK GENERATOR
# ============================
def fallback_reply(strategy: str) -> str:
    responses = FALLBACK_RESPONSES.get(
        strategy,
        ["Mujhe samajh nahi aa raha, thoda explain karo."]
    )
    return random.choice(responses)

# ============================
# MAIN GENERATE FUNCTION
# ============================
def generate_reply(strategy: str, conversation_history: list) -> str:
    """
    Generate reply using Groq.
    If Groq fails (429 / timeout), fallback safely.
    """

    strategy_hint = STRATEGY_HINTS.get(strategy, "")

    messages = [
        {
            "role": "system",
            "content": PERSONA_PROMPT + "\n" + strategy_hint
        }
    ]

    # Include last few turns only (token control)
    for msg in conversation_history[-4:]:
        role = "assistant" if msg["sender"] == "user" else "user"
        messages.append({
            "role": role,
            "content": msg["text"]
        })

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=60,
            timeout=8,  # HARD STOP (important)
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # ✅ SAFETY NET: never fail API call
        print(f"[Groq Fallback Triggered] {str(e)}")
        return fallback_reply(strategy)
