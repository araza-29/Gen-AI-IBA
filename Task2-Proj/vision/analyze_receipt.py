# import base64
# import requests

# GEMINI_API_KEY = "AIzaSyDwdA9LqXeCMjwGlUlWjgLyfQo6FBXDM1s"
# GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=" + GEMINI_API_KEY

# def extract_amount_from_image(image_path: str) -> float:
#     with open(image_path, "rb") as image_file:
#         image_data = base64.b64encode(image_file.read()).decode("utf-8")

#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {"text": "What is the total amount paid on this receipt? Just return the number."},
#                     {"inline_data": {
#                         "mime_type": "image/png",
#                         "data": image_data
#                     }}
#                 ]
#             }
#         ]
#     }

#     response = requests.post(GEMINI_URL, json=payload)
#     result = response.json()
#     try:
#         text = result['candidates'][0]['content']['parts'][0]['text']
#         return float(text.replace("$", "").strip())
#     except Exception as e:
#         print("Error:", e)
#         print("Full response:", result)
#         return 0.0


# import google.generativeai as genai
# import google.generativeai as genai
# import base64
# import requests
# GEMINI_API_KEY = "AIzaSyDwdA9LqXeCMjwGlUlWjgLyfQo6FBXDM1s"
# GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=" + GEMINI_API_KEY

# def analyze_receipt(image_url):
#      # Assuming the payload needs a 'parts' key and 'inline_data' or 'text'
#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {"text": "What is the total amount on this receipt? Just return the amount."},
#                     {"inline_data": {
#                         "mime_type": "image/png",
#                         "data": image_url
#                     }}
#                 ]
#             }
#         ]
#     }

#     # Send the payload to the Gemini Vision API
#     try:
#         response = requests.post(
#             GEMINI_URL,
#             json=payload  # Sending payload as JSON
#         )
#         if response.status_code == 200:
#             print(f"Image successfully processed: {image_url}")
#         else:
#             print(f"Error processing {image_url}: {response.text}")
#     except Exception as e:
#         print(f"An error occurred: {e}")



# import google.generativeai as genai
# import base64
# import requests

# # Your Gemini API key and URL
# GEMINI_API_KEY = "AIzaSyDwdA9LqXeCMjwGlUlWjgLyfQo6FBXDM1s"
# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

# def analyze_receipt(image_url):
#     # Step 1: Fetch the image from URL
#     try:
#         img_response = requests.get(image_url)
#         img_response.raise_for_status()
#         image_bytes = img_response.content
#     except Exception as e:
#         print(f"Error fetching image: {e}")
#         return None

#     # Step 2: Encode image to base64
#     image_base64 = base64.b64encode(image_bytes).decode("utf-8")

#     # Step 3: Prepare the Gemini payload
#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {"text": "What is the total amount on this receipt? Just return the amount."},
#                     {"inline_data": {
#                         "mime_type": "image/png",  # you can also detect mime-type if needed
#                         "data": image_base64
#                     }}
#                 ]
#             }
#         ]
#     }

#     # Step 4: Send the request to Gemini
#     try:
#         response = requests.post(GEMINI_URL, json=payload)
#         if response.status_code == 200:
#             result = response.json()
#             # Extract response text
#             reply = result['candidates'][0]['content']['parts'][0]['text']
#             return reply.strip()
#         else:
#             print(f"Error: {response.status_code} - {response.text}")
#             return None
#     except Exception as e:
#         print(f"An error occurred during Gemini API call: {e}")
#         return None




# import google.generativeai as genai
# import base64
# import requests
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# # Your Gemini API key and URL
# GEMINI_API_KEY = "AIzaSyDwdA9LqXeCMjwGlUlWjgLyfQo6FBXDM1s"
# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

# @retry(
#     stop=stop_after_attempt(3),
#     wait=wait_exponential(multiplier=1, min=2, max=10),
#     retry=retry_if_exception_type(requests.exceptions.RequestException)
# )
# def fetch_image(image_url):
#     response = requests.get(image_url)
#     response.raise_for_status()
#     return response.content

# @retry(
#     stop=stop_after_attempt(3),
#     wait=wait_exponential(multiplier=1, min=2, max=10),
#     retry=retry_if_exception_type(requests.exceptions.RequestException)
# )
# def send_to_gemini(payload):
#     response = requests.post(GEMINI_URL, json=payload)
#     response.raise_for_status()
#     return response.json()

# def analyze_receipt(image_url):
#     # Step 1: Fetch image bytes with retry
#     try:
#         image_bytes = fetch_image(image_url)
#     except Exception as e:
#         print(f"Error fetching image: {e}")
#         return None

#     # Step 2: Encode image to base64
#     image_base64 = base64.b64encode(image_bytes).decode("utf-8")

#     # Step 3: Prepare payload
#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {"text": "What is the total amount on this receipt? Just return the amount."},
#                     {
#                         "inline_data": {
#                             "mime_type": "image/png",
#                             "data": image_base64
#                         }
#                     }
#                 ]
#             }
#         ]
#     }

#     # Step 4: Send request to Gemini with retry
#     try:
#         response = requests.post(GEMINI_URL, json=payload)
#         if response.status_code == 200:
#             result = response.json()
#             # Extract response text
#             reply = result['candidates'][0]['content']['parts'][0]['text']
#             return reply.strip()
#         else:
#             print(f"Error: {response.status_code} - {response.text}")
#             return None
#     except Exception as e:
#         print(f"An error occurred during Gemini API call: {e}")
#         return None


# import google.generativeai as genai
# import base64
# import requests
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
# import re

# def clean_amount(amount_str):
#     try:
#         # Try direct conversion first
#         return float(amount_str)
#     except ValueError:
#         # Remove common symbols like $ and any text inside parentheses
#         cleaned = re.sub(r'[^0-9.]', '', amount_str.split('(')[0])
#         try:
#             return float(cleaned)
#         except ValueError:
#             return None

# # Your Gemini API key and URL
# GEMINI_API_KEY = "AIzaSyCxrDjE6ODeQP100zQrFBmbPGEHOTTxwBc"
# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

# @retry(
#     stop=stop_after_attempt(3),
#     wait=wait_exponential(multiplier=1, min=2, max=10),
#     retry=retry_if_exception_type(requests.exceptions.RequestException)
# )
# def fetch_image(image_url):
#     response = requests.get(image_url)
#     response.raise_for_status()
#     return response.content

# @retry(
#     stop=stop_after_attempt(3),
#     wait=wait_exponential(multiplier=1, min=2, max=10),
#     retry=retry_if_exception_type(requests.exceptions.RequestException)
# )
# def send_to_gemini(payload):
#     response = requests.post(GEMINI_URL, json=payload)
#     response.raise_for_status()
#     return response.json()

# def analyze_receipt(image_url):
#     # Step 1: Fetch image bytes with retry
#     try:
#         image_bytes = fetch_image(image_url)
#     except Exception as e:
#         print(f"Error fetching image: {e}")
#         return None

#     # Step 2: Encode image to base64
#     image_base64 = base64.b64encode(image_bytes).decode("utf-8")

#     # Step 3: Prepare payload
#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {"text": "What is the total amount on this receipt? Just return the amount."},
#                     {
#                         "inline_data": {
#                             "mime_type": "image/png",
#                             "data": image_base64
#                         }
#                     }
#                 ]
#             }
#         ]
#     }

#     # Step 4: Send request to Gemini with retry
#     try:
#         result = send_to_gemini(payload)
#         reply = result['candidates'][0]['content']['parts'][0]['text']

#         # Step 5: Process and clean the reply (e.g., converting the amount to float)
#         cleaned_reply = reply.strip()

#         # Try to convert the reply to a float if it's a number
#         try:
#             amount = float(cleaned_reply)  # Convert the amount to float
#             return amount
#         except ValueError:
#             print("Could not convert the amount to a float. Returning the raw string.")
#             return cleaned_reply  # Return the raw string if not convertible

#     except Exception as e:
#         print(f"An error occurred during Gemini API call: {e}")
#         return None


import base64
import requests
import re
import imghdr
import os
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Securely load Gemini API Key
GEMINI_API_KEY = "AIzaSyCxrDjE6ODeQP100zQrFBmbPGEHOTTxwBc"
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

        # Safely access nested response
        reply = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

        # Try cleaning & converting the result to a float
        amount = clean_amount(reply)
        if amount is not None:
            return amount
        else:
            print(f"⚠️ Could not convert extracted text to float. Raw reply: {reply}")
            return reply

    except Exception as e:
        print(f"❌ Error during Gemini API call: {e}")
        return None




# Example use:
# url = "https://ewqqiiowvwdzsnemaixq.supabase.co/storage/v1/s3/receipts/refund_req1.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ab8146af40caef88af637df9810676b2%2F20250420%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250420T022225Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a47f4f0f16f4d59ef98e8619a94d6064f583ac317208d4f12b80f1c72504125a"  # Any public receipt image
# result = analyze_receipt(url)
# print("Total Amount Extracted:", result)
