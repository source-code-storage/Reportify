"""
File validation service
"""

import os
from typing import Tuple
from fastapi import UploadFile, HTTPException, status

from app.core.config import settings


class FileValidationService:
    """Service for validating uploaded files"""

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".txt",
        ".png",
        ".jpg",
        ".jpeg",
        ".doc",
        ".docx",
    }

    # MIME types for validation
    ALLOWED_MIME_TYPES = {
        "application/pdf",
        "text/plain",
        "image/png",
        "image/jpeg",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    # Maximum file size (50MB)
    MAX_FILE_SIZE = settings.MAX_UPLOAD_SIZE

    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """
        Validate file extension.

        Args:
            filename: Name of the file

        Returns:
            True if extension is allowed

        Raises:
            HTTPException: If extension is not allowed
        """
        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension not in FileValidationService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(FileValidationService.ALLOWED_EXTENSIONS)}",
            )

        return True

    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """
        Validate file size.

        Args:
            file_size: Size of file in bytes

        Returns:
            True if size is within limit

        Raises:
            HTTPException: If file is too large
        """
        if file_size > FileValidationService.MAX_FILE_SIZE:
            max_size_mb = FileValidationService.MAX_FILE_SIZE / (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size: {max_size_mb}MB",
            )

        return True

    @staticmethod
    async def validate_file_content(file: UploadFile) -> Tuple[str, int]:
        """
        Validate file content and detect MIME type.

        Args:
            file: Uploaded file

        Returns:
            Tuple of (mime_type, file_size)

        Raises:
            HTTPException: If file content is invalid or malicious
        """
        # Read file content
        content = await file.read()
        file_size = len(content)

        # Reset file pointer
        await file.seek(0)

        # Validate file size
        FileValidationService.validate_file_size(file_size)

        # Use content type from upload or detect from extension
        mime_type = file.content_type or FileValidationService._get_mime_from_filename(
            file.filename or ""
        )

        # Validate MIME type
        if mime_type not in FileValidationService.ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Detected type: {mime_type}",
            )

        # Basic malicious content checks
        FileValidationService._check_malicious_content(content, mime_type)

        return mime_type, file_size

    @staticmethod
    def _get_mime_from_filename(filename: str) -> str:
        """
        Get MIME type from filename extension.

        Args:
            filename: Name of the file

        Returns:
            MIME type string
        """
        extension = os.path.splitext(filename)[1].lower()
        mime_map = {
            ".pdf": "application/pdf",
            ".txt": "text/plain",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        return mime_map.get(extension, "application/octet-stream")

    @staticmethod
    def _check_malicious_content(content: bytes, mime_type: str):
        """
        Basic check for malicious content.

        Args:
            content: File content
            mime_type: Detected MIME type

        Raises:
            HTTPException: If malicious content detected
        """
        # Check for executable signatures
        executable_signatures = [
            b"MZ",  # Windows executable
            b"\x7fELF",  # Linux executable
            b"#!",  # Script with shebang
        ]

        for signature in executable_signatures:
            if content.startswith(signature):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Executable files are not allowed",
                )

        # Check for suspicious patterns in text files
        if mime_type == "text/plain":
            try:
                text_content = content.decode("utf-8", errors="ignore")
                suspicious_patterns = [
                    "<script",
                    "javascript:",
                    "eval(",
                    "exec(",
                ]

                for pattern in suspicious_patterns:
                    if pattern.lower() in text_content.lower():
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File contains suspicious content",
                        )
            except Exception:
                pass  # If decoding fails, let it pass (binary content)

    @staticmethod
    async def validate_upload_file(file: UploadFile) -> Tuple[str, int]:
        """
        Complete validation of an uploaded file.

        Args:
            file: Uploaded file

        Returns:
            Tuple of (mime_type, file_size)

        Raises:
            HTTPException: If validation fails
        """
        # Validate filename
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required",
            )

        # Validate extension
        FileValidationService.validate_file_extension(file.filename)

        # Validate content and get MIME type
        mime_type, file_size = await FileValidationService.validate_file_content(file)

        return mime_type, file_size

    @staticmethod
    def get_file_type(filename: str) -> str:
        """
        Get file type from filename.

        Args:
            filename: Name of the file

        Returns:
            File type (extension without dot)
        """
        return os.path.splitext(filename)[1].lower().replace(".", "")

    @staticmethod
    def get_file_category(filename: str) -> str:
        """
        Get file category from filename.

        Args:
            filename: Name of the file

        Returns:
            File category (pdf, text, image, document)
        """
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".pdf":
            return "pdf"
        elif ext == ".txt":
            return "text"
        elif ext in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif", ".webp"}:
            return "image"
        elif ext in {".doc", ".docx"}:
            return "document"
        else:
            return "other"

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to remove potentially dangerous characters.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename
        """
        import re

        # Remove path separators and null bytes
        filename = os.path.basename(filename)
        # Remove or replace dangerous characters
        filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", filename)
        # Limit length
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[: 255 - len(ext)] + ext
        return filename


# Singleton instance
file_validation_service = FileValidationService()
