"""
Test script for report management endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def test_report_management():
    """Test complete report management flow"""

    print("=" * 60)
    print("Testing Report Management Endpoints")
    print("=" * 60)

    # First, login to get access token
    print("\n0. Logging in to get access token...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )

    if login_response.status_code != 200:
        print("   ✗ Login failed. Please ensure user exists.")
        return

    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    print("   ✓ Login successful")

    # 1. Create a report
    print("\n1. Testing POST /reports (Create Report)")
    try:
        response = requests.post(
            f"{BASE_URL}/reports",
            json={
                "title": "My Final Year Report",
                "description": "Report for my internship at Tech Company",
            },
            headers=headers,
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            report_data = response.json()
            report_id = report_data["id"]
            print(f"   ✓ Report created successfully")
            print(f"   Report ID: {report_id}")
            print(f"   Title: {report_data['title']}")
            print(f"   Status: {report_data['status']}")
            print(f"   Progress: {report_data['progress_percentage']}%")
        else:
            print(f"   ✗ Error: {response.json()}")
            return
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return

    # 2. List all reports
    print("\n2. Testing GET /reports (List Reports)")
    try:
        response = requests.get(f"{BASE_URL}/reports", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            reports = response.json()
            print(f"   ✓ Retrieved {len(reports)} report(s)")
            for report in reports:
                print(
                    f"   - {report['title']} (ID: {report['id']}, Progress: {report['progress_percentage']}%)"
                )
        else:
            print(f"   ✗ Error: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 3. Get specific report
    print(f"\n3. Testing GET /reports/{report_id} (Get Report)")
    try:
        response = requests.get(f"{BASE_URL}/reports/{report_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            report_data = response.json()
            print(f"   ✓ Report retrieved successfully")
            print(f"   Title: {report_data['title']}")
            print(f"   Description: {report_data['description']}")
            print(f"   Sections: {len(report_data['sections'])}")
        else:
            print(f"   ✗ Error: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 4. Create sections
    print(f"\n4. Testing POST /reports/{report_id}/sections (Create Sections)")
    section_ids = []
    sections_to_create = [
        {"title": "Introduction", "order": 1},
        {"title": "Methodology", "order": 2},
        {"title": "Results", "order": 3},
        {"title": "Conclusion", "order": 4},
    ]

    for section_data in sections_to_create:
        try:
            response = requests.post(
                f"{BASE_URL}/reports/{report_id}/sections",
                params=section_data,
                headers=headers,
            )
            if response.status_code == 201:
                section = response.json()
                section_ids.append(section["id"])
                print(f"   ✓ Created section: {section['title']} (ID: {section['id']})")
            else:
                print(f"   ✗ Error creating {section_data['title']}: {response.json()}")
        except Exception as e:
            print(f"   ✗ Error: {e}")

    # 5. Get sections
    print(f"\n5. Testing GET /reports/{report_id}/sections (Get Sections)")
    try:
        response = requests.get(
            f"{BASE_URL}/reports/{report_id}/sections", headers=headers
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            sections = response.json()
            print(f"   ✓ Retrieved {len(sections)} section(s)")
            for section in sections:
                print(
                    f"   - {section['title']} (Order: {section['order']}, Words: {section['word_count']})"
                )
        else:
            print(f"   ✗ Error: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 6. Update a section with content
    if section_ids:
        section_id = section_ids[0]
        print(
            f"\n6. Testing PUT /reports/{report_id}/sections/{section_id} (Update Section)"
        )
        try:
            content = "This is the introduction section. It provides an overview of the project and its objectives. The main goal was to develop a comprehensive solution."
            response = requests.put(
                f"{BASE_URL}/reports/{report_id}/sections/{section_id}",
                json={"content": content, "is_completed": True},
                headers=headers,
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                section = response.json()
                print(f"   ✓ Section updated successfully")
                print(f"   Word count: {section['word_count']}")
                print(f"   Completed: {section['is_completed']}")
            else:
                print(f"   ✗ Error: {response.json()}")
        except Exception as e:
            print(f"   ✗ Error: {e}")

    # 7. Check updated progress
    print(f"\n7. Testing Progress Calculation (Get Report Again)")
    try:
        response = requests.get(f"{BASE_URL}/reports/{report_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            report_data = response.json()
            print(f"   ✓ Progress updated automatically")
            print(f"   Progress: {report_data['progress_percentage']}%")
            print(f"   Total words: {report_data['total_word_count']}")
            print(f"   Expected: 25% (1 of 4 sections completed)")
        else:
            print(f"   ✗ Error: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 8. Update report
    print(f"\n8. Testing PUT /reports/{report_id} (Update Report)")
    try:
        response = requests.put(
            f"{BASE_URL}/reports/{report_id}",
            json={"title": "My Final Year Report - Updated", "status": "in_progress"},
            headers=headers,
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            report_data = response.json()
            print(f"   ✓ Report updated successfully")
            print(f"   New title: {report_data['title']}")
            print(f"   New status: {report_data['status']}")
        else:
            print(f"   ✗ Error: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 9. Test authorization (try to access non-existent report)
    print(f"\n9. Testing Authorization (Access Non-existent Report)")
    try:
        response = requests.get(f"{BASE_URL}/reports/99999", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✓ Authorization working - 404 for non-existent report")
        else:
            print(f"   ℹ Status: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 10. Delete report
    print(f"\n10. Testing DELETE /reports/{report_id} (Delete Report)")
    try:
        response = requests.delete(f"{BASE_URL}/reports/{report_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 204:
            print(f"   ✓ Report deleted successfully")
        else:
            print(f"   ✗ Error: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 11. Verify deletion
    print(f"\n11. Verifying Deletion (Try to Get Deleted Report)")
    try:
        response = requests.get(f"{BASE_URL}/reports/{report_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✓ Report successfully deleted (404 Not Found)")
        else:
            print(f"   ✗ Report still exists!")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    print("\n" + "=" * 60)
    print("Report Management Endpoint Tests Complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_report_management()
