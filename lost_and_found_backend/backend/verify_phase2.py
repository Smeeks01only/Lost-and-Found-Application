import requests
import sys
import datetime

BASE_URL = "http://127.0.0.1:8000"
AUTH_URL = f"{BASE_URL}/auth"
ITEMS_URL = f"{BASE_URL}/items"

def get_token():
    # Login as test user from Phase 1
    payload = {
        "username": "testuser_loser",
        "password": "StrongPassword123!"
    }
    response = requests.post(f"{AUTH_URL}/login/", json=payload)
    if response.status_code == 200:
        return response.json()['access']
    else:
        print(f"❌ Login Failed: {response.text}")
        return None

def test_create_lost_item(token):
    print("\nTesting Create LOST Item...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "description": "Lost my black leather wallet near the library entrance.",
        "location": "Library Entrance",
        "date_lost_found": datetime.datetime.now().isoformat(),
        "contact_info": "lost@example.com"
    }
    response = requests.post(f"{ITEMS_URL}/lost/", json=payload, headers=headers)
    if response.status_code == 201:
        print("✅ Created LOST Item")
        return True
    else:
        print(f"❌ Failed to create LOST item: {response.text}")
        return False

def test_create_found_item(token):
    print("\nTesting Create FOUND Item (with Security Question)...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "description": "Found a black leather wallet.",
        "location": "Library Steps",
        "date_lost_found": datetime.datetime.now().isoformat(),
        "contact_info": "found@example.com",
        "security_question": "What created ID is inside?",
        "security_answer": "Student ID 12345" 
    }
    response = requests.post(f"{ITEMS_URL}/found/", json=payload, headers=headers)
    if response.status_code == 201:
        print("✅ Created FOUND Item")
        data = response.json()
        if 'security_answer' not in data:
             print("✅ Security Answer NOT exposed in response")
        else:
             print("❌ Security Answer EXPOSED in response!")
        return True
    else:
        print(f"❌ Failed to create FOUND item: {response.text}")
        return False

def test_list_items(token):
    print("\nTesting List Items...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # List Lost
    resp = requests.get(f"{ITEMS_URL}/lost/", headers=headers)
    if resp.status_code == 200:
        print(f"✅ Listed {len(resp.json())} LOST items")
    else:
        print(f"❌ Failed to list LOST items: {resp.text}")

    # List Found
    resp = requests.get(f"{ITEMS_URL}/found/", headers=headers)
    if resp.status_code == 200:
        print(f"✅ Listed {len(resp.json())} FOUND items")
    else:
        print(f"❌ Failed to list FOUND items: {resp.text}")

def main():
    token = get_token()
    if not token:
        # Try registering if login fails (Phase 1 might need re-run in new env?)
        # For now assume Phase 1 user exists as DB is persistent
        print("Could not login. Ensure server is running and user exists.")
        sys.exit(1)

    test_create_lost_item(token)
    test_create_found_item(token)
    test_list_items(token)

if __name__ == "__main__":
    main()
