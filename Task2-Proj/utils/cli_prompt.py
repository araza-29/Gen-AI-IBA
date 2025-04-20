import sys
import os

# Add the root project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vision.analyze_receipt import analyze_receipt  # Now this should work!


# utils/cli_prompt.py
import argparse
import requests
from vision.analyze_receipt import analyze_receipt
from utils.db_client import update_refund
from utils.supabase_client import list_files_from_bucket, get_public_url

# Securely load Gemini API Key
GEMINI_API_KEY = "AIzaSyCxrDjE6ODeQP100zQrFBmbPGEHOTTxwBc"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

def send_to_gemini(prompt: str) -> dict:
    """Send the prompt to Gemini API to process the task."""
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(GEMINI_URL, json=payload)
    response.raise_for_status()
    return response.json()

def process_prompt(prompt: str):
    """Process the natural language prompt and perform the required task."""
    print(f"🚀 Processing prompt: {prompt}")
    try:
        # Send the prompt to Gemini
        result = send_to_gemini(prompt)

        # Extract relevant instructions from Gemini response
        action_instructions = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

        print(f"Gemini response: {action_instructions}")

        # Parse the instructions and act accordingly
        if "get all the urls from the storage" in action_instructions.lower():
            print("📂 Fetching files from Supabase...")
            files = list_files_from_bucket()
            print(f"🗂️ Found {len(files)} files")

            for filename in files:
                print(f"\n🖼️ Processing file: {filename}")
                image_url = get_public_url(filename)
                print(f"🔍 Analyzing receipt from: {image_url}")

                try:
                    amount = analyze_receipt(image_url)
                    if amount is not None:
                        print(f"✅ Extracted amount: {amount}")
                        update_refund(filename, image_url, amount)
                    else:
                        print("⚠️ No amount extracted. Skipping DB update.")
                except Exception as e:
                    print(f"❌ Error processing {filename}: {e}")
        else:
            print(f"❌ Could not understand instructions properly from Gemini. Response: {action_instructions}")

    except Exception as e:
        print(f"❌ Error processing prompt: {e}")

def main():
    # Parse the command-line prompt
    parser = argparse.ArgumentParser(description="Process natural language prompts for the refund agent.")
    parser.add_argument("prompt", help="Enter a natural language prompt for the agent to process.")
    args = parser.parse_args()

    # Process the given prompt
    process_prompt(args.prompt)

if __name__ == "__main__":
    main()
