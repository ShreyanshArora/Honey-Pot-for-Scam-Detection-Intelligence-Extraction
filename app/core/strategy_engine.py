from typing import List, Dict


def decide_strategy(history: List[Dict], extracted_info: Dict) -> str:
    """
    Decide how the agent should behave in this turn.
    Returns a strategy label used by agent_brain.
    """

    # If already got key intel, slow down and act confused
    if extracted_info["upiIds"] or extracted_info["bankAccounts"]:
        return "confused_delay"

    last_messages = " ".join([msg["text"].lower() for msg in history[-3:]])

    if "urgent" in last_messages or "immediately" in last_messages:
        return "scared"

    if "prize" in last_messages or "reward" in last_messages or "lottery" in last_messages:
        return "greedy"

    if "verify" in last_messages or "kyc" in last_messages or "account" in last_messages:
        return "obedient"

    if "link" in last_messages or "click" in last_messages:
        return "link_issue"

    if "otp" in last_messages:
        return "otp_problem"

    return "neutral_confused"
