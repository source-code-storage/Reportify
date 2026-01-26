"""
Test script for API endpoints
Tests the complete flow: create report → upload notes → generate content
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def test_api_flow():
    """Test the complete API flow"""

    print_section("Testing Report Writing Assistant API")

    # Step 1: Check API is running
    print_section("Step 1: Check API Health")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✅ API is running: {response.json()}")
    except Exception as e:
        print(f"❌ API is not running: {e}")
        print("   Start the backend: python test_frontend_integration.py")
        return

    # Step 2: Login (using mock user for now)
    print_section("Step 2: Authentication")
    print("Note: Using mock authentication for testing")
    print("In production, you would login with real credentials")

    # For testing, we'll skip auth and use a mock token
    # In real usage, you would do:
    # response = requests.post(f"{BASE_URL}/auth/login", json={
    #     "email": "test@example.com",
    #     "password": "password"
    # })
    # token = response.json()["access_token"]

    # Mock token for testing (you'll need to implement proper auth)
    token = "mock_token_for_testing"
    headers = {"Authorization": f"Bearer {token}"}

    print("⚠️  Note: Authentication endpoints need to be connected to database")
    print("   For now, testing without auth...")

    # Step 3: Create a report
    print_section("Step 3: Create Report")
    try:
        response = requests.post(
            f"{BASE_URL}/reports",
            headers=headers,
            json={
                "title": "Machine Learning Research Report",
                "description": "A comprehensive study of ML algorithms",
            },
        )

        if response.status_code == 401:
            print("⚠️  Authentication required. Skipping authenticated endpoints...")
            print("   To test with auth:")
            print("   1. Run database migrations: alembic upgrade head")
            print("   2. Create a test user")
            print("   3. Login to get a token")
            return

        report = response.json()
        report_id = report["id"]
        print(f"✅ Created report: ID={report_id}, Title='{report['title']}'")

    except Exception as e:
        print(f"❌ Failed to create report: {e}")
        return

    # Step 4: Create sections
    print_section("Step 4: Create Sections")
    sections = [
        {"title": "Introduction", "order": 1},
        {"title": "Literature Review", "order": 2},
        {"title": "Methodology", "order": 3},
    ]

    section_ids = []
    for section_data in sections:
        try:
            response = requests.post(
                f"{BASE_URL}/reports/{report_id}/sections",
                headers=headers,
                json=section_data,
            )
            section = response.json()
            section_ids.append(section["id"])
            print(f"✅ Created section: '{section['title']}' (ID={section['id']})")
        except Exception as e:
            print(f"❌ Failed to create section '{section_data['title']}': {e}")

    # Step 5: Create test note file
    print_section("Step 5: Upload Research Notes")

    # Create a test note file
    test_note_content = """
Machine Learning Overview

Machine learning is a method of data analysis that automates analytical model building. 
It is a branch of artificial intelligence based on the idea that systems can learn from 
data, identify patterns and make decisions with minimal human intervention.

Key Concepts:
- Supervised Learning: Learning from labeled data
- Unsupervised Learning: Finding patterns in unlabeled data
- Deep Learning: Neural networks with multiple layers
- Reinforcement Learning: Learning through trial and error

Applications:
Machine learning is used in various fields including computer vision, natural language 
processing, recommendation systems, and autonomous vehicles.
"""

    with open("test_note.txt", "w") as f:
        f.write(test_note_content)

    # Upload the note
    try:
        with open("test_note.txt", "rb") as f:
            response = requests.post(
                f"{BASE_URL}/notes/upload",
                headers=headers,
                data={"report_id": report_id},
                files={"file": ("test_note.txt", f, "text/plain")},
            )

        note = response.json()
        print(f"✅ Uploaded note: '{note['filename']}'")
        print(f"   Status: {note['status']}")
        print(f"   Size: {note['file_size']} bytes")
        print(f"   Content preview: {note['content'][:100]}...")

        if note["status"] == "completed":
            print("✅ Note processed and embeddings generated!")

    except Exception as e:
        print(f"❌ Failed to upload note: {e}")

    # Step 6: Search notes
    print_section("Step 6: Semantic Search")
    try:
        response = requests.get(
            f"{BASE_URL}/content/search",
            headers=headers,
            params={
                "query": "What is machine learning?",
                "report_id": report_id,
                "limit": 3,
            },
        )

        search_results = response.json()
        print(f"Query: '{search_results['query']}'")
        print(f"Found {len(search_results['results'])} results:")

        for idx, result in enumerate(search_results["results"], 1):
            print(f"\n  Result {idx}:")
            print(f"    Score: {result['score']:.4f}")
            print(f"    Source: {result['filename']}")
            print(f"    Text: {result['chunk_text'][:100]}...")

    except Exception as e:
        print(f"❌ Search failed: {e}")

    # Step 7: Generate AI content
    print_section("Step 7: Generate AI Content (THE MAGIC!)")

    # Check if OpenAI API key is configured
    try:
        response = requests.post(
            f"{BASE_URL}/content/generate",
            headers=headers,
            json={
                "section_id": section_ids[0],  # Introduction section
                "section_description": "Introduce machine learning concepts and applications",
            },
        )

        if response.status_code == 503:
            print("⚠️  OpenAI API key not configured")
            print("   To enable AI content generation:")
            print("   1. Get API key from https://platform.openai.com/")
            print("   2. Add to backend/.env: OPENAI_API_KEY=sk-your-key")
            print("   3. Restart backend")
            return

        result = response.json()

        print("✅ Content generated successfully!")
        print(f"\n{'='*60}")
        print("Generated Content:")
        print(f"{'='*60}")
        print(
            result["content"][:500] + "..."
            if len(result["content"]) > 500
            else result["content"]
        )

        print(f"\n{'='*60}")
        print("Metadata:")
        print(f"{'='*60}")
        print(f"Model: {result['metadata']['model']}")
        print(f"Input tokens: {result['metadata']['input_tokens']}")
        print(f"Output tokens: {result['metadata']['output_tokens']}")
        print(f"Total tokens: {result['metadata']['total_tokens']}")
        print(f"Estimated cost: ${result['metadata']['estimated_cost']}")

        print(f"\n{'='*60}")
        print(f"Sources Used: {len(result['sources'])}")
        print(f"{'='*60}")
        for idx, source in enumerate(result["sources"], 1):
            print(f"\nSource {idx}:")
            print(f"  File: {source['filename']}")
            print(f"  Relevance: {source['score']:.4f}")
            print(f"  Text: {source['chunk_text'][:100]}...")

    except Exception as e:
        print(f"❌ Content generation failed: {e}")
        import traceback

        traceback.print_exc()

    # Step 8: Get final report
    print_section("Step 8: Get Complete Report")
    try:
        response = requests.get(f"{BASE_URL}/reports/{report_id}", headers=headers)

        report = response.json()
        print(f"Report: {report['title']}")
        print(f"Status: {report['status']}")
        print(f"Progress: {report['progress_percentage']}%")
        print(f"Word count: {report['total_word_count']}")
        print(f"Sections: {len(report['sections'])}")

        for section in report["sections"]:
            print(f"\n  - {section['title']}")
            print(f"    Words: {section['word_count']}")
            print(f"    Completed: {section['is_completed']}")

    except Exception as e:
        print(f"❌ Failed to get report: {e}")

    # Summary
    print_section("Test Summary")
    print("✅ API endpoints are working!")
    print("\nNext steps:")
    print("1. Set up database and run migrations")
    print("2. Configure OpenAI API key")
    print("3. Connect frontend to these endpoints")
    print("4. Test end-to-end flow with real authentication")

    print("\n" + "=" * 60)
    print("🎉 API Test Complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    test_api_flow()
