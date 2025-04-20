# from supabase import create_client, Client
# import os

# SUPABASE_URL = "https://ewqqiiowvwdzsnemaixq.supabase.co"
# SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3cXFpaW93dndkenNuZW1haXhxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUwNjMwNzMsImV4cCI6MjA2MDYzOTA3M30.c3GD_Zsh-RrMpnmc-rQo1t4fXEhnQotfjFQpMfhVZ90"
# BUCKET_NAME = "receipts"

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# def upload_and_get_url(filename: str, local_path: str) -> str:
#     with open(local_path, 'rb') as f:
#         supabase.storage.from_(BUCKET_NAME).upload(file=f, path=filename, file_options={"content-type": "image/png"})
#     url = supabase.storage.from_(BUCKET_NAME).get_public_url(filename)
#     return url

# def insert_refund_request(image_url: str, amount: float):
#     data = {
#         "image_url": image_url,
#         "amount": amount
#     }
#     response = supabase.table("refund_requests").insert(data).execute()
#     return responsefrom supabase import create_client


# import os
# from dotenv import load_dotenv
# from supabase import create_client, Client
# load_dotenv()

# # SUPABASE_URL = load_dotenv("SUPABASE_URL")
# # SUPABASE_KEY = load_dotenv("SUPABASE_KEY")
# # BUCKET_NAME = load_dotenv("SUPABASE_BUCKET")
# SUPABASE_URL="https://ewqqiiowvwdzsnemaixq.supabase.co"
# SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3cXFpaW93dndkenNuZW1haXhxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUwNjMwNzMsImV4cCI6MjA2MDYzOTA3M30.c3GD_Zsh-RrMpnmc-rQo1t4fXEhnQotfjFQpMfhVZ90"
# SUPABASE_BUCKET="https://ewqqiiowvwdzsnemaixq.supabase.co/storage/v1/s3"

# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# # def list_files_from_bucket():
# #     response = supabase.storage.from_(BUCKET_NAME).list(path="receipts/")
# #     print("DEBUG: Supabase file list:", response)
# #     files = [file['name'] for file in response if file['name'].endswith(('.png', '.jpg', '.jpeg'))]
# #     return ["receipts/" + f for f in files]
# def list_files_from_bucket():
#     response = supabase.storage.from_(SUPABASE_BUCKET).list()
#     print("DEBUG raw list response:", response)
#     files = [file['name'] for file in response if file['name'].endswith(('.png', '.jpg', '.jpeg'))]
#     return [f"receipts/{f}" for f in files]

# def get_public_url(filename):
#     res = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)
#     return res["publicUrl"]



import os
from dotenv import load_dotenv
import boto3
from botocore.client import Config

# Load environment variables
load_dotenv()

SUPABASE_S3_ENDPOINT = "https://ewqqiiowvwdzsnemaixq.supabase.co/storage/v1/s3"
SUPABASE_S3_KEY = "ab8146af40caef88af637df9810676b2"
SUPABASE_S3_SECRET = "7aff88abcd497e03c7d8c8eda97cd11e1ce0888e116f1867fa465cddb2323deb"
SUPABASE_BUCKET = "receipts"

# Initialize S3 client
s3 = boto3.client(
    's3',
    endpoint_url=SUPABASE_S3_ENDPOINT,
    aws_access_key_id=SUPABASE_S3_KEY,
    aws_secret_access_key=SUPABASE_S3_SECRET,
    config=Config(signature_version='s3v4')
)


def list_files_from_bucket():
    """
    List all image files from the Supabase bucket.
    """
    response = s3.list_objects_v2(Bucket=SUPABASE_BUCKET, Prefix='')

    print("📦 DEBUG raw list response:", response)

    if 'Contents' not in response:
        print("⚠️ No files found in the bucket.")
        return []

    files = [
        item["Key"]
        for item in response["Contents"]
        if item["Key"].endswith((".png", ".jpg", ".jpeg"))
    ]
    return files

def get_public_url(filename):
    """
    Generate a temporary public URL for a file in the bucket.
    """
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": SUPABASE_BUCKET, "Key": filename},
        ExpiresIn=3600*24  # 1 hour
    )
    return url