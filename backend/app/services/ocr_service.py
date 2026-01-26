"""
OCR service for extracting text from images and scanned PDFs
"""

import os
from typing import Tuple, Dict, Optional
from PIL import Image
import io


class OCRService:
    """Service for OCR text extraction"""

    # Supported image extensions
    IMAGE_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".tiff",
        ".tif",
        ".webp",
    }

    def __init__(self):
        """Initialize OCR service"""
        self._tesseract_available = None
        self._tesseract_cmd = None

    @property
    def tesseract_available(self) -> bool:
        """Check if Tesseract is available"""
        if self._tesseract_available is None:
            try:
                import pytesseract

                # Try to get tesseract version
                pytesseract.get_tesseract_version()
                self._tesseract_available = True
            except Exception:
                self._tesseract_available = False
        return self._tesseract_available

    def is_image_file(self, filename: str) -> bool:
        """
        Check if file is an image based on extension.

        Args:
            filename: Name of the file

        Returns:
            True if file is an image
        """
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.IMAGE_EXTENSIONS

    def is_scanned_pdf(self, pdf_path: str) -> bool:
        """
        Check if PDF is scanned (image-based) or text-based.

        Args:
            pdf_path: Path to PDF file

        Returns:
            True if PDF appears to be scanned
        """
        try:
            import fitz

            doc = fitz.open(pdf_path)

            # Check first few pages
            pages_to_check = min(3, len(doc))
            total_text_length = 0

            for i in range(pages_to_check):
                page = doc[i]
                text = page.get_text().strip()
                total_text_length += len(text)

            doc.close()

            # If very little text found, likely scanned
            avg_text_per_page = (
                total_text_length / pages_to_check if pages_to_check > 0 else 0
            )
            return (
                avg_text_per_page < 100
            )  # Less than 100 chars per page = likely scanned

        except Exception:
            return False

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results.

        Args:
            image: PIL Image object

        Returns:
            Preprocessed PIL Image
        """
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Convert to grayscale
        image = image.convert("L")

        # Resize if too small (OCR works better with larger images)
        min_dimension = 1000
        width, height = image.size
        if width < min_dimension or height < min_dimension:
            scale = max(min_dimension / width, min_dimension / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Increase contrast
        from PIL import ImageEnhance

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)

        return image

    def extract_text_from_image(self, image_path: str) -> Tuple[str, Dict]:
        """
        Extract text from an image file using OCR.

        Args:
            image_path: Path to image file

        Returns:
            Tuple of (extracted_text, metadata)
        """
        if not self.tesseract_available:
            return self._fallback_image_extraction(image_path)

        try:
            import pytesseract

            # Open and preprocess image
            image = Image.open(image_path)
            processed_image = self.preprocess_image(image)

            # Perform OCR with detailed output
            data = pytesseract.image_to_data(
                processed_image, output_type=pytesseract.Output.DICT
            )

            # Extract text and calculate confidence
            text_parts = []
            confidences = []

            for i, word in enumerate(data["text"]):
                if word.strip():
                    text_parts.append(word)
                    conf = data["conf"][i]
                    if conf > 0:  # -1 means no confidence available
                        confidences.append(conf)

            extracted_text = " ".join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0

            metadata = {
                "word_count": len(text_parts),
                "char_count": len(extracted_text),
                "confidence": round(avg_confidence, 2),
                "image_width": image.width,
                "image_height": image.height,
                "method": "tesseract",
            }

            return extracted_text, metadata

        except Exception as e:
            # Fallback to basic extraction
            return self._fallback_image_extraction(image_path, str(e))

    def _fallback_image_extraction(
        self, image_path: str, error: str = None
    ) -> Tuple[str, Dict]:
        """
        Fallback when Tesseract is not available.

        Args:
            image_path: Path to image file
            error: Optional error message

        Returns:
            Tuple of (placeholder_text, metadata)
        """
        try:
            image = Image.open(image_path)

            # Return placeholder with image info
            placeholder = f"[Image file: {os.path.basename(image_path)}]\n"
            placeholder += f"[Size: {image.width}x{image.height}]\n"
            placeholder += "[OCR not available - Tesseract not installed]\n"
            if error:
                placeholder += f"[Error: {error}]\n"

            metadata = {
                "word_count": 0,
                "char_count": len(placeholder),
                "confidence": 0,
                "image_width": image.width,
                "image_height": image.height,
                "method": "fallback",
                "error": error or "Tesseract not available",
            }

            return placeholder, metadata

        except Exception as e:
            return f"[Failed to process image: {str(e)}]", {
                "word_count": 0,
                "char_count": 0,
                "confidence": 0,
                "method": "error",
                "error": str(e),
            }

    def extract_text_from_pdf_images(self, pdf_path: str) -> Tuple[str, Dict]:
        """
        Extract text from a scanned PDF by converting pages to images and running OCR.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Tuple of (extracted_text, metadata)
        """
        if not self.tesseract_available:
            return self._fallback_pdf_extraction(pdf_path)

        try:
            import fitz
            import pytesseract

            doc = fitz.open(pdf_path)
            all_text = []
            all_confidences = []
            total_words = 0

            for page_num, page in enumerate(doc, start=1):
                # Convert page to image
                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2)
                )  # 2x zoom for better OCR
                img_data = pix.tobytes("png")

                # Open as PIL Image
                image = Image.open(io.BytesIO(img_data))
                processed_image = self.preprocess_image(image)

                # Perform OCR
                data = pytesseract.image_to_data(
                    processed_image, output_type=pytesseract.Output.DICT
                )

                # Extract text
                page_text_parts = []
                for i, word in enumerate(data["text"]):
                    if word.strip():
                        page_text_parts.append(word)
                        conf = data["conf"][i]
                        if conf > 0:
                            all_confidences.append(conf)

                page_text = " ".join(page_text_parts)
                total_words += len(page_text_parts)

                if page_text.strip():
                    all_text.append(f"--- Page {page_num} ---\n{page_text}")

            doc.close()

            extracted_text = "\n\n".join(all_text)
            avg_confidence = (
                sum(all_confidences) / len(all_confidences) if all_confidences else 0
            )

            metadata = {
                "word_count": total_words,
                "char_count": len(extracted_text),
                "confidence": round(avg_confidence, 2),
                "page_count": len(doc) if hasattr(doc, "__len__") else 0,
                "method": "tesseract_pdf",
            }

            return extracted_text, metadata

        except Exception as e:
            return self._fallback_pdf_extraction(pdf_path, str(e))

    def _fallback_pdf_extraction(
        self, pdf_path: str, error: str = None
    ) -> Tuple[str, Dict]:
        """
        Fallback for scanned PDF when Tesseract is not available.

        Args:
            pdf_path: Path to PDF file
            error: Optional error message

        Returns:
            Tuple of (placeholder_text, metadata)
        """
        try:
            import fitz

            doc = fitz.open(pdf_path)
            page_count = len(doc)
            doc.close()

            placeholder = f"[Scanned PDF: {os.path.basename(pdf_path)}]\n"
            placeholder += f"[Pages: {page_count}]\n"
            placeholder += "[OCR not available - Tesseract not installed]\n"
            if error:
                placeholder += f"[Error: {error}]\n"

            metadata = {
                "word_count": 0,
                "char_count": len(placeholder),
                "confidence": 0,
                "page_count": page_count,
                "method": "fallback",
                "error": error or "Tesseract not available",
            }

            return placeholder, metadata

        except Exception as e:
            return f"[Failed to process PDF: {str(e)}]", {
                "word_count": 0,
                "char_count": 0,
                "confidence": 0,
                "method": "error",
                "error": str(e),
            }

    def extract_text_from_bytes(
        self, file_bytes: bytes, filename: str
    ) -> Tuple[str, Dict]:
        """
        Extract text from file bytes.

        Args:
            file_bytes: File content as bytes
            filename: Original filename

        Returns:
            Tuple of (extracted_text, metadata)
        """
        import tempfile

        ext = os.path.splitext(filename)[1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write(file_bytes)
            tmp_file.flush()

            try:
                if ext == ".txt":
                    text = file_bytes.decode("utf-8", errors="ignore")
                    return text, {
                        "word_count": len(text.split()),
                        "char_count": len(text),
                        "confidence": 100,
                        "method": "direct",
                    }
                elif ext == ".pdf":
                    if self.is_scanned_pdf(tmp_path):
                        return self.extract_text_from_pdf_images(tmp_path)
                    else:
                        import fitz

                        doc = fitz.open(tmp_path)
                        text = ""
                        for page in doc:
                            text += page.get_text() + "\n"
                        doc.close()
                        return text, {
                            "word_count": len(text.split()),
                            "char_count": len(text),
                            "confidence": 100,
                            "method": "pymupdf",
                        }
                elif self.is_image_file(filename):
                    return self.extract_text_from_image(tmp_path)
                else:
                    return f"[Unsupported file type: {ext}]", {
                        "word_count": 0,
                        "char_count": 0,
                        "confidence": 0,
                        "method": "unsupported",
                    }
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)


# Singleton instance
ocr_service = OCRService()
