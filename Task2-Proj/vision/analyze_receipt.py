import base64
import requests
import re
import imghdr
import os
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

GEMINI_API_KEY = "AIzaSyDwdA9LqXeCMjwGlUlWjgLyfQo6FBXDM1s"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

def clean_amount(amount_str: str):
    """Cleans and converts a string amount like '$12.50' or '12.50 USD' into float."""
    try:
        return float(amount_str)
    except ValueError:
        cleaned = re.sub(r"[^\d.]", "", amount_str.split('(')[0])
        try:
            return float(cleaned)
        except ValueError:
            return None

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.exceptions.RequestException)
)
def fetch_image(image_url: str) -> bytes:
    response = requests.get(image_url)
    response.raise_for_status()
    return response.content

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.exceptions.RequestException)
)
def send_to_gemini(payload: dict) -> dict:
    response = requests.post(GEMINI_URL, json=payload)
    response.raise_for_status()
    return response.json()

def analyze_receipt(image_url: str):
    try:
        image_bytes = fetch_image(image_url)
    except Exception as e:
        print(f"❌ Error fetching image: {e}")
        return None

    mime_type = f"image/{imghdr.what(None, h=image_bytes) or 'png'}"
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "What is the total amount on this receipt? Just return the amount."},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    }

    try:
        result = send_to_gemini(payload)

        reply = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

        amount = clean_amount(reply)
        if amount is not None:
            return amount
        else:
            print(f"⚠️ Could not convert extracted text to float. Raw reply: {reply}")
            return reply

    except Exception as e:
        print(f"❌ Error during Gemini API call: {e}")
        return None

