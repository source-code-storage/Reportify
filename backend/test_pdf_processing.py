"""
Test script for PDF processing functionality
Tests Task 7 - PDF Processing Worker
"""

import requests
import json
import io
import time
from pathlib import Path

# Base URL
BASE_URL = "http://localhost:8000/api/v1"

# Test credentials
TEST_USER = {
    "email": f"pdf_test_{hash('test')}@example.com",
    "password": "TestPassword123!",
    "full_name": "PDF Test User",
}

# Global variables
access_token = None
report_id = None


def print_section(title):
    """Print a section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def register_and_login():
    """Register and login user"""
    print_section("1. AUTHENTICATION")

    # Register
    response = requests.post(f"{BASE_URL}/auth/register", json=TEST_USER)
    if response.status_code == 201:
        print("✅ User registered")
    elif "already registered" in response.text.lower():
        print("ℹ️  User already exists")

    # Login
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": TEST_USER["email"], "password": TEST_USER["password"]},
    )

    if response.status_code == 200:
        global access_token
        access_token = response.json()["access_token"]
        print("✅ Login successful")
        return True
    else:
        print(f"❌ Login failed: {response.status_code}")
        return False


def create_test_report():
    """Create a test report"""
    print_section("2. CREATING TEST REPORT")

    headers = {"Authorization": f"Bearer {access_token}"}
    report_data = {
        "title": "PDF Processing Test Report",
        "description": "Testing PDF template processing",
    }

    response = requests.post(f"{BASE_URL}/reports", json=report_data, headers=headers)

    if response.status_code == 201:
        global report_id
        report_id = response.json()["id"]
        print(f"✅ Report created (ID: {report_id})")
        return True
    else:
        print(f"❌ Report creation failed: {response.status_code}")
        return False


def create_sample_pdf():
    """Create a sample PDF with sections"""
    print_section("3. CREATING SAMPLE PDF")

    try:
        import fitz  # PyMuPDF

        # Create a new PDF
        doc = fitz.open()

        # Page 1
        page = doc.new_page()

        # Title
        page.insert_text(
            (72, 72), "Sample Report Template", fontsize=24, fontname="helv-bold"
        )

        # Section 1
        page.insert_text(
            (72, 120), "1. Introduction", fontsize=18, fontname="helv-bold"
        )
        page.insert_text(
            (72, 150),
            "This is the introduction section. It provides an overview of the report.",
            fontsize=12,
        )

        # Section 1.1
        page.insert_text((72, 200), "1.1 Background", fontsize=14, fontname="helv-bold")
        page.insert_text(
            (72, 230),
            "Background information goes here. This section provides context.",
            fontsize=12,
        )

        # Section 2
        page.insert_text((72, 300), "2. Methodology", fontsize=18, fontname="helv-bold")
        page.insert_text(
            (72, 330),
            "This section describes the methodology used in the research.",
            fontsize=12,
        )

        # Page 2
        page = doc.new_page()

        # Section 3
        page.insert_text((72, 72), "3. Results", fontsize=18, fontname="helv-bold")
        page.insert_text(
            (72, 102),
            "The results of the study are presented in this section.",
            fontsize=12,
        )

        # Section 4
        page.insert_text((72, 200), "4. Conclusion", fontsize=18, fontname="helv-bold")
        page.insert_text(
            (72, 230),
            "This section summarizes the findings and provides conclusions.",
            fontsize=12,
        )

        # Save to bytes
        pdf_bytes = doc.tobytes()
        doc.close()

        print("✅ Sample PDF created")
        print(f"   Pages: 2")
        print(f"   Sections: 6 (including subsections)")
        print(f"   Size: {len(pdf_bytes)} bytes")

        return pdf_bytes

    except ImportError:
        print("⚠️  PyMuPDF not installed, using simple PDF")
        # Fallback: create a minimal PDF
        pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 24 Tf
100 700 Td
(Sample Report) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000317 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
410
%%EOF"""
        print("✅ Simple PDF created (fallback)")
        return pdf_content


def upload_pdf_template(pdf_content):
    """Upload PDF template"""
    print_section("4. UPLOADING PDF TEMPLATE")

    headers = {"Authorization": f"Bearer {access_token}"}
    files = {"file": ("test_template.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"report_id": report_id}

    response = requests.post(
        f"{BASE_URL}/uploads/template", files=files, data=data, headers=headers
    )

    if response.status_code == 201:
        data = response.json()
        print("✅ PDF uploaded successfully")
        print(f"   Upload ID: {data['id']}")
        print(f"   Filename: {data['filename']}")
        print(f"   Status: {data['status']}")
        return data["id"]
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None


def wait_for_processing(upload_id, max_wait=30):
    """Wait for PDF processing to complete"""
    print_section("5. WAITING FOR PDF PROCESSING")

    headers = {"Authorization": f"Bearer {access_token}"}

    print("⏳ Waiting for processing to complete...")
    print("   (This may take a few seconds)")

    for i in range(max_wait):
        response = requests.get(
            f"{BASE_URL}/uploads/{upload_id}/status", headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            status = data["status"]
            progress = data.get("progress", 0)

            print(f"   Status: {status} ({progress}%)", end="\r")

            if status == "completed":
                print(f"\n✅ Processing completed!")
                print(f"   Progress: {progress}%")
                print(f"   Completed at: {data.get('completed_at', 'N/A')}")
                return True
            elif status == "failed":
                print(f"\n❌ Processing failed!")
                print(f"   Error: {data.get('error_message', 'Unknown error')}")
                return False

            time.sleep(1)
        else:
            print(f"\n❌ Failed to get status: {response.status_code}")
            return False

    print(f"\n⚠️  Processing timeout after {max_wait} seconds")
    return False


def check_template_structure():
    """Check if template structure was created"""
    print_section("6. CHECKING TEMPLATE STRUCTURE")

    headers = {"Authorization": f"Bearer {access_token}"}

    # Get report details
    response = requests.get(f"{BASE_URL}/reports/{report_id}", headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("✅ Report retrieved")
        print(f"   Title: {data['title']}")
        print(f"   Sections: {len(data.get('sections', []))}")

        # Check if sections were created from template
        if data.get("sections"):
            print("\n   📄 Extracted Sections:")
            for section in data["sections"]:
                print(f"      - {section.get('title', 'Untitled')}")
            return True
        else:
            print("   ⚠️  No sections found (processing may still be in progress)")
            return False
    else:
        print(f"❌ Failed to get report: {response.status_code}")
        return False


def run_all_tests():
    """Run all PDF processing tests"""
    print("\n" + "=" * 60)
    print("  PDF PROCESSING TEST SUITE")
    print("  Testing Task 7 - PDF Processing Worker")
    print("=" * 60)

    results = {"passed": 0, "failed": 0, "total": 0}

    def record_result(success):
        results["total"] += 1
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1

    # Run tests
    record_result(register_and_login())

    if not access_token:
        print("\n❌ Cannot continue without authentication")
        return

    record_result(create_test_report())

    if not report_id:
        print("\n❌ Cannot continue without a report")
        return

    # Create and upload PDF
    pdf_content = create_sample_pdf()
    if pdf_content:
        record_result(True)

        upload_id = upload_pdf_template(pdf_content)
        if upload_id:
            record_result(True)

            # Wait for processing
            processing_success = wait_for_processing(upload_id)
            record_result(processing_success)

            if processing_success:
                # Check results
                record_result(check_template_structure())
        else:
            record_result(False)
    else:
        record_result(False)

    # Print summary
    print_section("TEST SUMMARY")
    print(f"Total tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"\nSuccess rate: {(results['passed'] / results['total'] * 100):.1f}%")

    if results["failed"] == 0:
        print("\n🎉 All tests passed! Task 7 is working correctly.")
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed.")
        print("\nNote: If processing failed, make sure:")
        print("  1. Redis is running (for Celery)")
        print("  2. Celery worker is running")
        print("  3. MinIO is accessible")
        print("\nTo start Celery worker:")
        print("  cd backend")
        print("  celery -A app.worker.celery_app worker --loglevel=info")


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
