from utils.supabase_client import list_files_from_bucket, get_public_url
from vision.analyze_receipt import analyze_receipt
from utils.db_client import update_refund

def run_pipeline():
    print(f"📂 Fetching files from Supabase...")
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
