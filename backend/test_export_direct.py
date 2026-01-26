"""Test export functionality directly"""

import sys

sys.path.insert(0, ".")

from app.services.export_service import export_service

# Test data
sections = [
    {"title": "Introduction", "content": "This is the introduction section."},
    {"title": "Background", "content": "This is the background section."},
    {"title": "Methodology", "content": "This is the methodology section."},
]

print("Testing PDF export...")
try:
    pdf_bytes = export_service.export_to_pdf(
        report_title="Test Report",
        sections=sections,
        author="Test User",
        metadata={"description": "Test description"},
    )
    print(f"✓ PDF generated successfully! Size: {len(pdf_bytes)} bytes")

    # Save to file
    with open("test_export.pdf", "wb") as f:
        f.write(pdf_bytes)
    print("✓ PDF saved to test_export.pdf")

except Exception as e:
    print(f"✗ PDF export failed: {e}")
    import traceback

    traceback.print_exc()

print("\nTesting DOCX export...")
try:
    docx_bytes = export_service.export_to_docx(
        report_title="Test Report",
        sections=sections,
        author="Test User",
        metadata={"description": "Test description"},
    )
    print(f"✓ DOCX generated successfully! Size: {len(docx_bytes)} bytes")

    # Save to file
    with open("test_export.docx", "wb") as f:
        f.write(docx_bytes)
    print("✓ DOCX saved to test_export.docx")

except Exception as e:
    print(f"✗ DOCX export failed: {e}")
    import traceback

    traceback.print_exc()
