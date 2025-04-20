# import os
# from utils.supabase_client import upload_and_get_url
# from utils.supabase_client import insert_refund_request
# from vision.analyze_receipt import extract_amount_from_image

# def process_images_in_folder(folder_path: str):
#     for filename in os.listdir(folder_path):
#         if filename.endswith((".png", ".jpg", ".jpeg")):
#             full_path = os.path.join(folder_path, filename)
#             print(f"🔄 Processing {filename}...")

#             image_url = upload_and_get_url(filename, full_path)
#             print(f"✅ Uploaded and got public URL: {image_url}")

#             amount = extract_amount_from_image(full_path)
#             print(f"💰 Extracted Amount: {amount}")

#             insert_refund_request(image_url, amount)
#             print(f"📥 Inserted into refund_requests\n")


# from utils.supabase_client import list_files_from_bucket, get_public_url
# from vision.analyze_receipt import analyze_receipt
# from utils.db_client import update_refund # assumes a function to insert into refund_requests

# def run_pipeline():
#     print(f"📂 Fetching files from Supabase...")
#     files = list_files_from_bucket()
#     print(f"🗂️ Found {len(files)} files")

#     for filename in files:
#         # filename = file['name']
#         print(f"🖼️ Processing file: {filename}")
#         image_url = get_public_url(filename)
#         print(f"🔍 Analyzing {filename}...")

#         try:
#             amount = analyze_receipt(image_url)
#             print(f"✅ Extracted amount: {amount}")
#             update_refund(filename,image_url, amount)
#         except Exception as e:
#             print(f"❌ Error processing {filename}: {e}")
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
