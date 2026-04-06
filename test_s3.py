import os
import boto3
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_S3_REGION_NAME')
)

with open('test.txt', 'wb') as f:
    f.write(b"Hello")

try:
    with open('test.txt', 'rb') as f:
        s3_client.upload_fileobj(
            f,
            os.getenv('AWS_STORAGE_BUCKET_NAME'),
            "purchases/test/test.txt"
        )
    print("UPLOAD SUCCESSFUL")
except Exception as e:
    print("UPLOAD FAILED:", e)
