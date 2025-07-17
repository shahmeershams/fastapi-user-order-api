#!/usr/bin/env python3

import requests
import json
import sys
import time
from subprocess import Popen, PIPE

def test_api():
    base_url = "http://localhost:8000"
    
    # Test ping first
    print("Testing ping endpoint...")
    try:
        response = requests.get(f"{base_url}/ping")
        print(f"Ping response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Ping failed: {e}")
        return False
    
    # Test creating a user
    print("\nTesting user creation...")
    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "mypassword123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/users",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"User creation response: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 201:
            print("✅ User created successfully!")
            user_id = response.json().get("user_id")
            print(f"User ID: {user_id}")
        else:
            print(f"❌ User creation failed")
            return False
            
    except Exception as e:
        print(f"User creation request failed: {e}")
        return False
    
    # Test listing users
    print("\nTesting user listing...")
    try:
        response = requests.get(f"{base_url}/users")
        print(f"User list response: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            users_data = response.json()
            print(f"✅ Found {users_data.get('total', 0)} users")
        else:
            print(f"❌ User listing failed")
            
    except Exception as e:
        print(f"User listing request failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Starting API tests...")
    test_api()
