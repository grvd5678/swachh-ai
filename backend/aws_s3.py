import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

load_dotenv()

# AWS Configurations
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")  # Default to AWS Mumbai
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "swachh-ai-knowledge-base-grvd5678")

KB_DIR = BASE_DIR / "data" / "knowledge_base"

def get_s3_client():
    import boto3
    from botocore.exceptions import NoCredentialsError

    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        return boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )
    else:
        # Fallback to default AWS CLI credentials (~/.aws/credentials)
        return boto3.client("s3", region_name=AWS_REGION)

def ensure_bucket_exists(s3_client, bucket_name: str, region: str):
    """Create S3 bucket if it does not already exist."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except Exception:
        print(f"Bucket '{bucket_name}' not found. Creating in region '{region}'...")
        try:
            if region == "us-east-1":
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": region},
                )
            print(f"Successfully created bucket: '{bucket_name}'!")
        except Exception as e:
            print(f"Error creating bucket '{bucket_name}': {e}")
            raise

def upload_knowledge_base(bucket_name: str = S3_BUCKET_NAME):
    """Upload all markdown guidelines from data/knowledge_base to Amazon S3."""
    print("=" * 65)
    print(f"Uploading Knowledge Base to Amazon S3: s3://{bucket_name}/")
    print("=" * 65)

    try:
        s3 = get_s3_client()
        ensure_bucket_exists(s3, bucket_name, AWS_REGION)

        files = list(KB_DIR.glob("*.md"))
        if not files:
            print(f"No files found in {KB_DIR}")
            return

        for file_path in files:
            s3_key = f"guidelines/{file_path.name}"
            print(f"Uploading: {file_path.name} -> s3://{bucket_name}/{s3_key}")
            
            s3.upload_file(
                Filename=str(file_path),
                Bucket=bucket_name,
                Key=s3_key,
                ExtraArgs={
                    "Metadata": {
                        "Project": "Swachh.ai",
                        "Source": "Authoritative-Regulations",
                    }
                },
            )

        print(f"\nSUCCESS: All {len(files)} regulatory files uploaded to Amazon S3!")
        print(f"Check your AWS Console under S3 -> '{bucket_name}/guidelines/'")

    except Exception as e:
        print(f"\n⚠️ AWS Error: {e}")
        print("Tip: Ensure your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are added to .env")

def list_s3_files(bucket_name: str = S3_BUCKET_NAME):
    """List documents currently stored in the S3 knowledge repository."""
    try:
        s3 = get_s3_client()
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix="guidelines/")
        print(f"\nFiles in s3://{bucket_name}/guidelines/:")
        if "Contents" in response:
            for item in response["Contents"]:
                print(f"  • {item['Key']} (Size: {item['Size']} bytes, Last Modified: {item['LastModified']})")
        else:
            print("  (Bucket is empty or prefix has no objects)")
    except Exception as e:
        print(f"AWS Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Swachh.ai S3 Knowledge Base Manager")
    parser.add_argument("--upload", action="store_true", help="Upload local knowledge base to S3")
    parser.add_argument("--list", action="store_true", help="List files in S3 knowledge base bucket")
    args = parser.parse_args()

    if args.list:
        list_s3_files()
    else:
        # Default action
        upload_knowledge_base()
