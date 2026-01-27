import requests
import sys

BASE_URL = "http://127.0.0.1:8000/auth"

def test_registration():
    print("Testing Registration...")
    payload = {
        "username": "testuser_loser",
        "email": "test@example.com",
        "password": "StrongPassword123!",
        "role": "LOSER"
    }
    try:
        response = requests.post(f"{BASE_URL}/register/", json=payload)
        if response.status_code == 201:
            print("✅ Registration Successful")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
             print("⚠️  User already exists (Expected if re-running)")
             return True
        else:
            print(f"❌ Registration Failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the server running?")
        return False

def test_login():
    print("\nTesting Login...")
    payload = {
        "username": "testuser_loser",
        "password": "StrongPassword123!"
    }
    response = requests.post(f"{BASE_URL}/login/", json=payload)
    if response.status_code == 200:
        print("✅ Login Successful")
        return response.json()
    else:
        print(f"❌ Login Failed: {response.text}")
        return None

def test_me(access_token):
    print("\nTesting /me Endpoint...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/me/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ /me Verified. User: {data['username']}, Role: {data['role']}")
        if data['role'] == 'LOSER':
             print("✅ Role Verification Passed")
        else:
             print(f"❌ Role Missmatch: Expected LOSER, got {data['role']}")
    else:
        print(f"❌ /me Failed: {response.text}")

def main():
    if test_registration():
        tokens = test_login()
        if tokens:
            test_me(tokens['access'])
        else:
            sys.exit(1)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
