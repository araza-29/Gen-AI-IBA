import sys
import re
from utils.supabase_client import list_files_from_bucket, get_public_url
from vision.analyze_receipt import analyze_receipt
from utils.db_client import update_refund

def process_natural_language(prompt: str):
    file_match = re.search(r"refund_req(\d+).png.*?till (\d+)", prompt)
    if not file_match:
        print("❌ Couldn't find valid range in prompt.")
        return
    
    start_index = int(file_match.group(1))
    end_index = int(file_match.group(2))

    filenames = [f"refund_req{i}.png" for i in range(start_index, end_index + 1)]

    print(f"📥 Expected files: {filenames}")

    all_files = list_files_from_bucket()

    matching_files = [f for f in all_files if f in filenames]

    if not matching_files:
        print("⚠️ No matching files found in bucket.")
        return

    for filename in matching_files:
        print(f"\n🖼️ Processing: {filename}")
        image_url = get_public_url(filename)
        amount = analyze_receipt(image_url)

        if amount is not None:
            print(f"✅ Extracted Amount: {amount}")
            update_refund(filename, image_url, amount)
        else:
            print("⚠️ No amount found, skipping update.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please pass a natural language prompt as an argument.")
        sys.exit(1)

    prompt_input = sys.argv[1]
    print(f"🤖 User: \n\"{prompt_input}\"\n")
    print("Thinking...\n")
    print("Assistant: \n")
    process_natural_language(prompt_input)
