from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
def update_refund(image_filename, image_url, amount):
    from postgrest.base_request_builder import APIResponse

    try:
        refund_id = int(''.join(filter(str.isdigit, image_filename)))
    except ValueError:
        print(f"❌ Could not extract ID from {image_filename}")
        return

    print(f"\n🔄 Updating row ID: {refund_id}")
    print(f"   Image URL: {image_url}")
    print(f"   Amount: {amount}")

    update_data = {
        "image_url": image_url,
        "amount": amount
    }

    try:
        response = supabase.table("refund_requests").update(update_data).eq("id", refund_id).execute()

        if isinstance(response, APIResponse):
            if response.data:
                print(f"✅ Successfully updated row {refund_id}")
                print(f"   ↪ Updated data: {response.data[0]}")
            else:
                print(f"❌ Update failed for row {refund_id}. No data returned.")
        elif isinstance(response, dict):
            if response.get("status") == 200 or response.get("data"):
                print(f"✅ Successfully updated row {refund_id}")
            else:
                print(f"❌ Update failed for row {refund_id}. Response: {response}")
        else:
            print(f"❌ Unexpected response type {type(response)}:\n{response}")

    except Exception as e:
        print(f"❌ Error processing {image_filename}: {e}")

    # Extract ID from filename like refund_req3.png -> 3
    try:
        refund_id = int(''.join(filter(str.isdigit, image_filename)))
    except ValueError:
        print(f"❌ Could not extract ID from {image_filename}")
        return

    print(f"🔄 Updating row ID: {refund_id}\nWith URL: {image_url}\n with amount: {amount}")
    update_data = {
        "image_url": image_url,
        "amount": amount
    }

    try:
        response = supabase.table("refund_requests").update(update_data).eq("id", refund_id).execute()

        # Safely access response fields
        if isinstance(response, dict):
            if response.get("status") == 200 or response.get("data"):
                print(f"✅ Successfully updated row {refund_id}")
            else:
                print(f"❌ Update failed for row {refund_id}. Response: {response}")
        else:
            # fallback if it's not a dict
            print(f"✅ Fallback success check: Response type {type(response)}\n{response}")

    except Exception as e:
        print(f"❌ Error processing {image_filename}: {e}")