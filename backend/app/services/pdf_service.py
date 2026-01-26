"""
PDF processing service for extracting text and structure from PDF files
"""

import fitz  # PyMuPDF
from typing import List, Dict, Tuple, Optional
import re
from dataclasses import dataclass


@dataclass
class PDFTextBlock:
    """Represents a text block extracted from PDF"""

    text: str
    page_number: int
    position_top: float
    font_size: float
    font_name: str
    is_bold: bool
    bbox: Tuple[float, float, float, float]  # (x0, y0, x1, y1)


@dataclass
class PDFSection:
    """Represents a section identified in PDF"""

    title: str
    level: int
    content: str
    page_number: int
    position_top: float
    font_size: float
    font_name: str
    is_bold: bool
    word_count: int
    children: List["PDFSection"]


class PDFService:
    """Service for processing PDF files"""

    # Common heading patterns
    HEADING_PATTERNS = [
        r"^\d+\.\s+",  # 1. Introduction
        r"^\d+\.\d+\s+",  # 1.1 Background
        r"^\d+\.\d+\.\d+\s+",  # 1.1.1 Details
        r"^[A-Z][A-Z\s]+$",  # ALL CAPS HEADINGS
        r"^Chapter\s+\d+",  # Chapter 1
        r"^Section\s+\d+",  # Section 1
        r"^Part\s+[IVX]+",  # Part I, Part II
        r"^[IVX]+\.\s+",  # I. Introduction, II. Background
        r"^[A-Z]\.\s+",  # A. First Section
    ]

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Tuple[str, List[PDFTextBlock], Dict]:
        """
        Extract text and structure from PDF file.

        Args:
            file_path: Path to PDF file

        Returns:
            Tuple of (full_text, text_blocks, metadata)
        """
        try:
            doc = fitz.open(file_path)
            full_text = ""
            text_blocks = []

            # Extract metadata
            metadata = {
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", ""),
                "producer": doc.metadata.get("producer", ""),
                "creation_date": doc.metadata.get("creationDate", ""),
                "modification_date": doc.metadata.get("modDate", ""),
                "total_pages": len(doc),
            }

            # Extract text blocks from each page
            for page_num, page in enumerate(doc, start=1):
                # Get text with formatting information
                blocks = page.get_text("dict")["blocks"]

                for block in blocks:
                    if block.get("type") == 0:  # Text block
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                text = span.get("text", "").strip()
                                if text:
                                    # Extract formatting information
                                    font_size = span.get("size", 12.0)
                                    font_name = span.get("font", "")
                                    is_bold = "bold" in font_name.lower()
                                    bbox = span.get("bbox", (0, 0, 0, 0))

                                    text_block = PDFTextBlock(
                                        text=text,
                                        page_number=page_num,
                                        position_top=bbox[1],
                                        font_size=font_size,
                                        font_name=font_name,
                                        is_bold=is_bold,
                                        bbox=bbox,
                                    )
                                    text_blocks.append(text_block)
                                    full_text += text + " "

                # Add page break
                full_text += "\n\n"

            doc.close()
            return full_text.strip(), text_blocks, metadata

        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    @staticmethod
    def identify_sections(text_blocks: List[PDFTextBlock]) -> List[PDFSection]:
        """
        Identify sections in PDF based on text formatting and patterns.

        Args:
            text_blocks: List of text blocks extracted from PDF

        Returns:
            List of identified sections with hierarchy
        """
        if not text_blocks:
            return []

        # Calculate average font size for comparison
        avg_font_size = sum(block.font_size for block in text_blocks) / len(text_blocks)

        sections = []
        current_section = None
        current_content = []

        for i, block in enumerate(text_blocks):
            is_heading = PDFService._is_heading(block, avg_font_size)

            if is_heading:
                # Save previous section if exists
                if current_section:
                    current_section.content = " ".join(current_content).strip()
                    current_section.word_count = len(current_section.content.split())
                    sections.append(current_section)

                # Start new section
                level = PDFService._determine_heading_level(block, avg_font_size)
                current_section = PDFSection(
                    title=block.text,
                    level=level,
                    content="",
                    page_number=block.page_number,
                    position_top=block.position_top,
                    font_size=block.font_size,
                    font_name=block.font_name,
                    is_bold=block.is_bold,
                    word_count=0,
                    children=[],
                )
                current_content = []
            else:
                # Add to current section content
                if current_section:
                    current_content.append(block.text)

        # Save last section
        if current_section:
            current_section.content = " ".join(current_content).strip()
            current_section.word_count = len(current_section.content.split())
            sections.append(current_section)

        # Build hierarchy
        hierarchical_sections = PDFService._build_hierarchy(sections)

        return hierarchical_sections

    @staticmethod
    def _is_heading(block: PDFTextBlock, avg_font_size: float) -> bool:
        """
        Determine if a text block is a heading.

        Args:
            block: Text block to check
            avg_font_size: Average font size in document

        Returns:
            True if block is likely a heading
        """
        # Check font size (headings are usually larger)
        if block.font_size > avg_font_size * 1.2:
            return True

        # Check if bold
        if block.is_bold and block.font_size >= avg_font_size:
            return True

        # Check heading patterns
        for pattern in PDFService.HEADING_PATTERNS:
            if re.match(pattern, block.text):
                return True

        # Check if all caps and short (likely a heading)
        if block.text.isupper() and len(block.text.split()) <= 10:
            return True

        return False

    @staticmethod
    def _determine_heading_level(block: PDFTextBlock, avg_font_size: float) -> int:
        """
        Determine the heading level (1-6) based on formatting.

        Args:
            block: Text block
            avg_font_size: Average font size in document

        Returns:
            Heading level (1-6)
        """
        # Check for numbered sections
        if re.match(r"^\d+\.\d+\.\d+\s+", block.text):
            return 3
        elif re.match(r"^\d+\.\d+\s+", block.text):
            return 2
        elif re.match(r"^\d+\.\s+", block.text):
            return 1

        # Check font size relative to average
        size_ratio = block.font_size / avg_font_size
        if size_ratio >= 1.8:
            return 1
        elif size_ratio >= 1.5:
            return 2
        elif size_ratio >= 1.3:
            return 3
        elif size_ratio >= 1.1:
            return 4
        else:
            return 5

    @staticmethod
    def _build_hierarchy(sections: List[PDFSection]) -> List[PDFSection]:
        """
        Build hierarchical structure from flat list of sections.

        Args:
            sections: Flat list of sections

        Returns:
            Hierarchical list of sections
        """
        if not sections:
            return []

        root_sections = []
        stack = []  # Stack to track parent sections

        for section in sections:
            # Pop sections from stack that are not parents of current section
            while stack and stack[-1].level >= section.level:
                stack.pop()

            if stack:
                # Add as child of last section in stack
                stack[-1].children.append(section)
            else:
                # Add as root section
                root_sections.append(section)

            # Add current section to stack
            stack.append(section)

        return root_sections

    @staticmethod
    def extract_simple_text(file_path: str) -> str:
        """
        Simple text extraction without formatting (fallback method).

        Args:
            file_path: Path to PDF file

        Returns:
            Extracted text
        """
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")


# Singleton instance
pdf_service = PDFService()
