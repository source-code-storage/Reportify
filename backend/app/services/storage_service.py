"""
File storage service for S3/MinIO
"""

import os
import uuid
from typing import Optional, BinaryIO
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status

from app.core.config import settings


class StorageService:
    """Service for managing file storage in S3/MinIO"""

    def __init__(self):
        """Initialize S3/MinIO client"""
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
        )
        self.bucket_name = settings.S3_BUCKET_NAME
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure the S3 bucket exists, create if it doesn't"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                # Bucket doesn't exist, create it
                try:
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                    print(f"Created S3 bucket: {self.bucket_name}")
                except ClientError as create_error:
                    print(f"Error creating bucket: {create_error}")
            else:
                print(f"Error checking bucket: {e}")

    def upload_file(
        self,
        file_content: bytes,
        file_name: str,
        content_type: str,
        folder: str = "uploads",
    ) -> str:
        """
        Upload a file to S3/MinIO.

        Args:
            file_content: File content as bytes
            file_name: Original file name
            content_type: MIME type of the file
            folder: Folder/prefix in the bucket

        Returns:
            S3 object key (path to file in bucket)

        Raises:
            HTTPException: If upload fails
        """
        try:
            # Generate unique file name
            file_extension = os.path.splitext(file_name)[1]
            unique_name = f"{uuid.uuid4()}{file_extension}"
            object_key = f"{folder}/{unique_name}"

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_content,
                ContentType=content_type,
                Metadata={
                    "original_filename": file_name,
                    "upload_date": datetime.utcnow().isoformat(),
                },
            )

            return object_key

        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload file: {str(e)}",
            )

    def upload_file_stream(
        self,
        file_stream: BinaryIO,
        file_name: str,
        content_type: str,
        folder: str = "uploads",
    ) -> str:
        """
        Upload a file from a stream to S3/MinIO.

        Args:
            file_stream: File stream object
            file_name: Original file name
            content_type: MIME type of the file
            folder: Folder/prefix in the bucket

        Returns:
            S3 object key (path to file in bucket)

        Raises:
            HTTPException: If upload fails
        """
        try:
            # Generate unique file name
            file_extension = os.path.splitext(file_name)[1]
            unique_name = f"{uuid.uuid4()}{file_extension}"
            object_key = f"{folder}/{unique_name}"

            # Upload to S3
            self.s3_client.upload_fileobj(
                file_stream,
                self.bucket_name,
                object_key,
                ExtraArgs={
                    "ContentType": content_type,
                    "Metadata": {
                        "original_filename": file_name,
                        "upload_date": datetime.utcnow().isoformat(),
                    },
                },
            )

            return object_key

        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload file: {str(e)}",
            )

    def download_file(self, object_key: str) -> bytes:
        """
        Download a file from S3/MinIO.

        Args:
            object_key: S3 object key (path to file)

        Returns:
            File content as bytes

        Raises:
            HTTPException: If download fails or file not found
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name, Key=object_key
            )
            return response["Body"].read()

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NoSuchKey":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="File not found",
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to download file: {str(e)}",
            )

    def download_file_to_path(self, object_key: str, local_path: str) -> str:
        """
        Download a file from S3/MinIO to a local path.

        Args:
            object_key: S3 object key (path to file)
            local_path: Local file path to save to

        Returns:
            Local file path

        Raises:
            HTTPException: If download fails or file not found
        """
        try:
            self.s3_client.download_file(self.bucket_name, object_key, local_path)
            return local_path

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NoSuchKey":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="File not found",
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to download file: {str(e)}",
            )

    def delete_file(self, object_key: str) -> bool:
        """
        Delete a file from S3/MinIO.

        Args:
            object_key: S3 object key (path to file)

        Returns:
            True if deleted successfully

        Raises:
            HTTPException: If deletion fails
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
            return True

        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file: {str(e)}",
            )

    def get_file_url(self, object_key: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for temporary file access.

        Args:
            object_key: S3 object key (path to file)
            expiration: URL expiration time in seconds (default 1 hour)

        Returns:
            Presigned URL

        Raises:
            HTTPException: If URL generation fails
        """
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": object_key},
                ExpiresIn=expiration,
            )
            return url

        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate file URL: {str(e)}",
            )

    def file_exists(self, object_key: str) -> bool:
        """
        Check if a file exists in S3/MinIO.

        Args:
            object_key: S3 object key (path to file)

        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=object_key)
            return True
        except ClientError:
            return False

    def get_file_metadata(self, object_key: str) -> dict:
        """
        Get metadata for a file in S3/MinIO.

        Args:
            object_key: S3 object key (path to file)

        Returns:
            Dictionary with file metadata

        Raises:
            HTTPException: If file not found or metadata retrieval fails
        """
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name, Key=object_key
            )
            return {
                "content_type": response.get("ContentType"),
                "content_length": response.get("ContentLength"),
                "last_modified": response.get("LastModified"),
                "metadata": response.get("Metadata", {}),
            }

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="File not found",
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get file metadata: {str(e)}",
            )


# Singleton instance
storage_service = StorageService()
