# import psycopg2

# DB_CONFIG = {
#     'dbname': 'your_db',
#     'user': 'your_user',
#     'password': 'your_password',
#     'host': 'localhost',
#     'port': '5432'
# }

# def insert_refund_request(image_url: str, amount: float):
#     conn = psycopg2.connect(**DB_CONFIG)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO refund_requests (image_url, amount) VALUES (%s, %s)", (image_url, amount))
#     conn.commit()
#     cursor.close()
#     conn.close()


# from supabase import create_client
# import os
# from dotenv import load_dotenv

# load_dotenv()

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# def insert_refund(image_url, amount):
#     print(f"📝 Inserting into DB: {image_url} with amount: {amount}")
#     data = {"image_url": image_url, "amount": amount}
#     supabase.table("refund_requests").insert(data).execute()




# from supabase import create_client
# import os
# from dotenv import load_dotenv

# load_dotenv()

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# def update_refund(image_filename, image_url, amount):
#     # Extract ID from filename like refund_req3.png -> 3
#     try:
#         refund_id = int(''.join(filter(str.isdigit, image_filename)))
#     except ValueError:
#         print(f"❌ Could not extract ID from {image_filename}")
#         return

#     print(f"🔄 Updating row ID {refund_id}: {image_url} with amount: {amount}")
#     update_data = {
#         "image_url": image_url,
#         "amount": amount
#     }

#     response = supabase.table("refund_requests").update(update_data).eq("id", refund_id).execute()

#     # if response.get("status_code") == 200:
#     if response.status_code == 200:
#         print(f"✅ Successfully updated row {refund_id}")
#     else:
#         print(f"❌ Failed to update row {refund_id}: {response}")



from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def update_refund(image_filename, image_url, amount):
    # Extract ID from filename like refund_req3.png -> 3
    try:
        refund_id = int(''.join(filter(str.isdigit, image_filename)))
    except ValueError:
        print(f"❌ Could not extract ID from {image_filename}")
        return

    print(f"🔄 Updating row ID {refund_id}: {image_url} with amount: {amount}")
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