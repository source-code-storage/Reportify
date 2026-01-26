"""
Test script for authentication endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def test_auth_flow():
    """Test complete authentication flow"""

    print("=" * 60)
    print("Testing Authentication Endpoints")
    print("=" * 60)

    # Test data
    test_user = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
    }

    # 1. Test Registration
    print("\n1. Testing POST /auth/register")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            user_data = response.json()
            print(f"   ✓ User registered successfully")
            print(f"   User ID: {user_data['id']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Name: {user_data['name']}")
        elif response.status_code == 400:
            print(f"   ℹ User already exists (expected if running multiple times)")
        else:
            print(f"   ✗ Error: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return

    # 2. Test Login
    print("\n2. Testing POST /auth/login")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": test_user["email"], "password": test_user["password"]},
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
            print(f"   ✓ Login successful")
            print(f"   Access Token: {access_token[:50]}...")
            print(f"   Refresh Token: {refresh_token[:50]}...")
        else:
            print(f"   ✗ Error: {response.json()}")
            return
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return

    # 3. Test Get Current User
    print("\n3. Testing GET /auth/me")
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me", headers={"Authorization": f"Bearer {access_token}"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✓ User info retrieved successfully")
            print(f"   User ID: {user_data['id']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Name: {user_data['name']}")
            print(f"   Active: {user_data['is_active']}")
        else:
            print(f"   ✗ Error: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 4. Test Token Refresh
    print("\n4. Testing POST /auth/refresh")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/refresh", json={"refresh_token": refresh_token}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            new_tokens = response.json()
            new_access_token = new_tokens["access_token"]
            print(f"   ✓ Token refreshed successfully")
            print(f"   New Access Token: {new_access_token[:50]}...")
        else:
            print(f"   ✗ Error: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 5. Test Logout
    print("\n5. Testing POST /auth/logout")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 204:
            print(f"   ✓ Logout successful")
        else:
            print(f"   ✗ Error: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 6. Test Invalid Credentials
    print("\n6. Testing login with invalid credentials")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": test_user["email"], "password": "wrongpassword"},
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print(f"   ✓ Invalid credentials rejected correctly")
        else:
            print(f"   ✗ Unexpected response: {response.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # 7. Test Unauthorized Access
    print("\n7. Testing unauthorized access to /auth/me")
    try:
        response = requests.get(f"{BASE_URL}/auth/me")
        print(f"   Status: {response.status_code}")
        if response.status_code == 403:
            print(f"   ✓ Unauthorized access blocked correctly")
        else:
            print(f"   ℹ Status: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    print("\n" + "=" * 60)
    print("Authentication Endpoint Tests Complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_auth_flow()
