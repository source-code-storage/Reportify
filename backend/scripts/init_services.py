"""
Initialize external services (S3 bucket, Qdrant collection, etc.)
"""

import boto3
from botocore.exceptions import ClientError
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.core.config import settings


def init_s3_bucket():
    """Create S3 bucket if it doesn't exist."""
    print("Initializing S3 bucket...")

    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
    )

    try:
        s3_client.head_bucket(Bucket=settings.S3_BUCKET_NAME)
        print(f"✓ Bucket '{settings.S3_BUCKET_NAME}' already exists")
    except ClientError:
        try:
            s3_client.create_bucket(Bucket=settings.S3_BUCKET_NAME)
            print(f"✓ Created bucket '{settings.S3_BUCKET_NAME}'")
        except Exception as e:
            print(f"✗ Failed to create bucket: {e}")
            raise


def init_qdrant_collection():
    """Create Qdrant collection if it doesn't exist."""
    print("Initializing Qdrant collection...")

    client = QdrantClient(url=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

    collection_name = "note_embeddings"

    try:
        collections = client.get_collections().collections
        if any(col.name == collection_name for col in collections):
            print(f"✓ Collection '{collection_name}' already exists")
        else:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            print(f"✓ Created collection '{collection_name}'")
    except Exception as e:
        print(f"✗ Failed to initialize Qdrant collection: {e}")
        raise


def main():
    """Initialize all services."""
    print("=" * 50)
    print("Initializing Report Writing Assistant Services")
    print("=" * 50)

    try:
        init_s3_bucket()
        init_qdrant_collection()
        print("\n✓ All services initialized successfully!")
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
