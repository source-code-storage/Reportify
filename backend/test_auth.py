"""
Quick test script for authentication endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def test_auth_flow():
    """Test the complete authentication flow"""

    print("=" * 50)
    print("Testing Authentication Flow")
    print("=" * 50)

    # Test 1: Register a new user
    print("\n1. Testing user registration...")
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("✓ User registered successfully")
            user = response.json()
            print(f"  User ID: {user['id']}")
            print(f"  Email: {user['email']}")
            print(f"  Name: {user['name']}")
        else:
            print(f"✗ Registration failed: {response.status_code}")
            print(f"  {response.json()}")
    except Exception as e:
        print(f"✗ Registration error: {e}")
        return

    # Test 2: Login with credentials
    print("\n2. Testing user login...")
    login_data = {"email": "test@example.com", "password": "testpassword123"}

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✓ Login successful")
            tokens = response.json()
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
            print(f"  Access token: {access_token[:50]}...")
            print(f"  Refresh token: {refresh_token[:50]}...")
        else:
            print(f"✗ Login failed: {response.status_code}")
            print(f"  {response.json()}")
            return
    except Exception as e:
        print(f"✗ Login error: {e}")
        return

    # Test 3: Get current user info
    print("\n3. Testing get current user...")
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            print("✓ Got current user info")
            user = response.json()
            print(f"  User ID: {user['id']}")
            print(f"  Email: {user['email']}")
            print(f"  Name: {user['name']}")
        else:
            print(f"✗ Get user failed: {response.status_code}")
            print(f"  {response.json()}")
    except Exception as e:
        print(f"✗ Get user error: {e}")

    # Test 4: Refresh token
    print("\n4. Testing token refresh...")
    refresh_data = {"refresh_token": refresh_token}

    try:
        response = requests.post(f"{BASE_URL}/auth/refresh", json=refresh_data)
        if response.status_code == 200:
            print("✓ Token refreshed successfully")
            new_tokens = response.json()
            print(f"  New access token: {new_tokens['access_token'][:50]}...")
        else:
            print(f"✗ Token refresh failed: {response.status_code}")
            print(f"  {response.json()}")
    except Exception as e:
        print(f"✗ Token refresh error: {e}")

    # Test 5: Logout
    print("\n5. Testing logout...")
    try:
        response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
        if response.status_code == 204:
            print("✓ Logout successful")
        else:
            print(f"✗ Logout failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Logout error: {e}")

    # Test 6: Try to login with wrong password
    print("\n6. Testing invalid credentials...")
    wrong_login = {"email": "test@example.com", "password": "wrongpassword"}

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=wrong_login)
        if response.status_code == 401:
            print("✓ Invalid credentials correctly rejected")
        else:
            print(f"✗ Expected 401, got: {response.status_code}")
    except Exception as e:
        print(f"✗ Invalid credentials test error: {e}")

    print("\n" + "=" * 50)
    print("Authentication tests completed!")
    print("=" * 50)


if __name__ == "__main__":
    test_auth_flow()
