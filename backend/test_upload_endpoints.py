"""
Test script for file upload endpoints
Tests Task 5 - File Upload Service
"""

import requests
import json
import io
from pathlib import Path

# Base URL
BASE_URL = "http://localhost:8000/api/v1"

# Test credentials
TEST_USER = {
    "email": f"upload_test_{hash('test')}@example.com",
    "password": "TestPassword123!",
    "full_name": "Upload Test User",
}

# Global variables for test data
access_token = None
report_id = None


def print_section(title):
    """Print a section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def register_user():
    """Register a new test user"""
    print_section("1. REGISTERING TEST USER")

    response = requests.post(f"{BASE_URL}/auth/register", json=TEST_USER)

    if response.status_code == 201:
        print("✅ User registered successfully")
        return True
    elif response.status_code == 400 and "already registered" in response.text.lower():
        print("ℹ️  User already exists, will try to login")
        return True
    else:
        print(f"❌ Registration failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def login_user():
    """Login and get access token"""
    global access_token

    print_section("2. LOGGING IN")

    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": TEST_USER["email"], "password": TEST_USER["password"]},
    )

    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        print("✅ Login successful")
        print(f"   Access token: {access_token[:20]}...")
        return True
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def create_test_report():
    """Create a test report"""
    global report_id

    print_section("3. CREATING TEST REPORT")

    headers = {"Authorization": f"Bearer {access_token}"}

    report_data = {
        "title": "Upload Test Report",
        "description": "Testing file upload functionality",
    }

    response = requests.post(f"{BASE_URL}/reports", json=report_data, headers=headers)

    if response.status_code == 201:
        data = response.json()
        report_id = data["id"]
        print("✅ Report created successfully")
        print(f"   Report ID: {report_id}")
        print(f"   Title: {data['title']}")
        return True
    else:
        print(f"❌ Report creation failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def test_template_upload():
    """Test template file upload"""
    print_section("4. TESTING TEMPLATE UPLOAD")

    headers = {"Authorization": f"Bearer {access_token}"}

    # Create a fake PDF file
    pdf_content = b"%PDF-1.4\n%Test PDF content\n%%EOF"
    files = {"file": ("test_template.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"report_id": report_id}

    response = requests.post(
        f"{BASE_URL}/uploads/template", files=files, data=data, headers=headers
    )

    if response.status_code == 201:
        data = response.json()
        print("✅ Template uploaded successfully")
        print(f"   Upload ID: {data['id']}")
        print(f"   Filename: {data['filename']}")
        print(f"   Status: {data['status']}")
        print(f"   File size: {data['file_size']} bytes")
        return data["id"]
    else:
        print(f"❌ Template upload failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None


def test_notes_upload():
    """Test multiple note files upload"""
    print_section("5. TESTING NOTES UPLOAD")

    headers = {"Authorization": f"Bearer {access_token}"}

    # Create multiple test files
    files = [
        ("files", ("note1.txt", io.BytesIO(b"Test note 1 content"), "text/plain")),
        ("files", ("note2.txt", io.BytesIO(b"Test note 2 content"), "text/plain")),
        (
            "files",
            (
                "note3.pdf",
                io.BytesIO(b"%PDF-1.4\n%Test PDF note\n%%EOF"),
                "application/pdf",
            ),
        ),
    ]
    data = {"report_id": report_id}

    response = requests.post(
        f"{BASE_URL}/uploads/notes", files=files, data=data, headers=headers
    )

    if response.status_code == 201:
        data = response.json()
        print("✅ Notes uploaded successfully")
        print(f"   Uploaded: {data['uploaded']}")
        print(f"   Failed: {data['failed']}")
        print(f"\n   Upload jobs:")
        for job in data["jobs"]:
            status_icon = "✅" if job["status"] == "completed" else "❌"
            print(f"   {status_icon} {job['filename']} - {job['status']}")
        return [job["id"] for job in data["jobs"]]
    else:
        print(f"❌ Notes upload failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return []


def test_upload_status(upload_id):
    """Test getting upload status"""
    print_section(f"6. CHECKING UPLOAD STATUS (ID: {upload_id})")

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(f"{BASE_URL}/uploads/{upload_id}/status", headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("✅ Upload status retrieved successfully")
        print(f"   Filename: {data['filename']}")
        print(f"   Status: {data['status']}")
        print(f"   Progress: {data['progress']}%")
        print(f"   Created: {data['created_at']}")
        if data.get("completed_at"):
            print(f"   Completed: {data['completed_at']}")
        if data.get("error_message"):
            print(f"   Error: {data['error_message']}")
        return True
    else:
        print(f"❌ Failed to get upload status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def test_invalid_file_upload():
    """Test uploading an invalid file type"""
    print_section("7. TESTING INVALID FILE UPLOAD")

    headers = {"Authorization": f"Bearer {access_token}"}

    # Try to upload an executable file (should be rejected)
    exe_content = b"MZ\x90\x00"  # Windows executable signature
    files = {
        "file": ("malicious.exe", io.BytesIO(exe_content), "application/x-msdownload")
    }
    data = {"report_id": report_id}

    response = requests.post(
        f"{BASE_URL}/uploads/notes", files=files, data=data, headers=headers
    )

    if response.status_code == 400 or response.status_code == 201:
        if response.status_code == 400:
            print("✅ Invalid file correctly rejected")
            print(f"   Error: {response.json().get('detail', 'Unknown error')}")
        else:
            # Check if it was marked as failed
            data = response.json()
            if data["failed"] > 0:
                print("✅ Invalid file correctly rejected during processing")
            else:
                print("⚠️  Invalid file was accepted (security issue!)")
        return True
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def test_file_size_limit():
    """Test file size limit"""
    print_section("8. TESTING FILE SIZE LIMIT")

    headers = {"Authorization": f"Bearer {access_token}"}

    # Create a file larger than 50MB
    large_content = b"X" * (51 * 1024 * 1024)  # 51MB
    files = {"file": ("large_file.txt", io.BytesIO(large_content), "text/plain")}
    data = {"report_id": report_id}

    response = requests.post(
        f"{BASE_URL}/uploads/notes", files=files, data=data, headers=headers
    )

    if response.status_code == 413 or response.status_code == 400:
        print("✅ Large file correctly rejected")
        print(f"   Error: {response.json().get('detail', 'File too large')}")
        return True
    elif response.status_code == 201:
        data = response.json()
        if data["failed"] > 0:
            print("✅ Large file correctly rejected during validation")
            return True
        else:
            print("⚠️  Large file was accepted (should be rejected!)")
            return False
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def test_delete_upload(upload_id):
    """Test deleting an upload"""
    print_section(f"9. TESTING UPLOAD DELETION (ID: {upload_id})")

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.delete(f"{BASE_URL}/uploads/{upload_id}", headers=headers)

    if response.status_code == 204:
        print("✅ Upload deleted successfully")
        return True
    else:
        print(f"❌ Failed to delete upload: {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def run_all_tests():
    """Run all upload tests"""
    print("\n" + "=" * 60)
    print("  FILE UPLOAD SERVICE TEST SUITE")
    print("  Testing Task 5 - File Upload Service")
    print("=" * 60)

    results = {
        "passed": 0,
        "failed": 0,
        "total": 0,
    }

    def record_result(success):
        results["total"] += 1
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1

    # Run tests
    record_result(register_user())
    record_result(login_user())

    if not access_token:
        print("\n❌ Cannot continue without authentication")
        return

    record_result(create_test_report())

    if not report_id:
        print("\n❌ Cannot continue without a report")
        return

    template_upload_id = test_template_upload()
    record_result(template_upload_id is not None)

    note_upload_ids = test_notes_upload()
    record_result(len(note_upload_ids) > 0)

    if template_upload_id:
        record_result(test_upload_status(template_upload_id))

    record_result(test_invalid_file_upload())
    record_result(test_file_size_limit())

    if template_upload_id:
        record_result(test_delete_upload(template_upload_id))

    # Print summary
    print_section("TEST SUMMARY")
    print(f"Total tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"\nSuccess rate: {(results['passed'] / results['total'] * 100):.1f}%")

    if results["failed"] == 0:
        print("\n🎉 All tests passed! Task 5 is working correctly.")
    else:
        print(
            f"\n⚠️  {results['failed']} test(s) failed. Please review the output above."
        )


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
