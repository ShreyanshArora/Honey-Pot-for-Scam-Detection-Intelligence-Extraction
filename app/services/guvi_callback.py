import requests
from app.config import settings


def send_final_result(payload: dict) -> bool:
    """
    Sends the final extracted intelligence to GUVI evaluation endpoint.
    Returns True if successful.
    """
    try:
        print("\n========== GUVI CALLBACK TRIGGERED ==========")
        print("Payload being sent to GUVI:")
        print(payload)

        response = requests.post(
            settings.GUVI_CALLBACK_URL,
            json=payload,
            timeout=settings.CALLBACK_TIMEOUT_SECONDS,
        )

        print("GUVI Response Status:", response.status_code)
        print("GUVI Response Text:", response.text)
        print("=============================================\n")

        return response.status_code == 200

    except Exception as e:
        print(f"[GUVI CALLBACK ERROR] {e}")
        return False
