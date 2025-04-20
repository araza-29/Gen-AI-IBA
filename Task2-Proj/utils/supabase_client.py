import os
from dotenv import load_dotenv
import boto3
from botocore.client import Config

load_dotenv()

SUPABASE_S3_ENDPOINT = "https://ewqqiiowvwdzsnemaixq.supabase.co/storage/v1/s3"
SUPABASE_S3_KEY = "ab8146af40caef88af637df9810676b2"
SUPABASE_S3_SECRET = "7aff88abcd497e03c7d8c8eda97cd11e1ce0888e116f1867fa465cddb2323deb"
SUPABASE_BUCKET = "receipts"

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
        ExpiresIn=3600*24  
    )
    return url