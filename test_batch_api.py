#!/usr/bin/env python3
"""
Test script for the new batch translation API endpoint.
This script tests both single and batch translation to verify the rate limiting works.
"""

import requests
import time
import json

# API configuration
API_BASE_URL = "https://rough-1-8qyx.onrender.com"
# API_BASE_URL = "http://127.0.0.1:8000"  # Uncomment for local testing

def test_single_translation():
    """Test single translation endpoint."""
    print("🧪 Testing Single Translation...")
    
    payload = {
        "text": "Hello, how are you today?",
        "source_lang": "Auto",
        "target_lang": "Spanish"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/translate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"✅ Single translation successful: {result['translated_text']}")
                return True
            else:
                print(f"❌ Single translation failed: {result.get('message')}")
                return False
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return False

def test_batch_translation():
    """Test batch translation endpoint."""
    print("\n🧪 Testing Batch Translation...")
    
    texts = [
        "Hello world",
        "How are you?",
        "Good morning",
        "Thank you very much",
        "Have a nice day"
    ]
    
    payload = {
        "texts": texts,
        "source_lang": "Auto",
        "target_lang": "French"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/translate_batch",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                translations = result.get("translations", [])
                successful = [t for t in translations if t.get("success")]
                print(f"✅ Batch translation successful: {len(successful)}/{len(translations)} texts translated")
                
                for i, translation in enumerate(translations):
                    if translation.get("success"):
                        print(f"  Text {i+1}: {translation['translated_text']}")
                    else:
                        print(f"  Text {i+1}: Failed - {translation.get('message')}")
                
                return True
            else:
                print(f"❌ Batch translation failed: {result.get('message')}")
                return False
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return False

def test_rate_limiting():
    """Test rate limiting by making multiple rapid requests."""
    print("\n🧪 Testing Rate Limiting...")
    
    payload = {
        "text": "Test message",
        "source_lang": "Auto",
        "target_lang": "German"
    }
    
    print("Making 5 rapid requests to test rate limiting...")
    
    for i in range(5):
        try:
            start_time = time.time()
            response = requests.post(
                f"{API_BASE_URL}/translate",
                json=payload,
                timeout=30
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"  Request {i+1}: ✅ Success in {end_time - start_time:.2f}s")
                else:
                    print(f"  Request {i+1}: ❌ Failed - {result.get('message')}")
            else:
                print(f"  Request {i+1}: ❌ API error {response.status_code}")
                
        except Exception as e:
            print(f"  Request {i+1}: ❌ Failed - {str(e)}")
        
        # Small delay between requests
        time.sleep(0.1)

def test_api_health():
    """Test API health endpoint."""
    print("🧪 Testing API Health...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ API is healthy")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting API Tests...")
    print(f"🌐 Testing API at: {API_BASE_URL}")
    print("=" * 50)
    
    # Test API health first
    if not test_api_health():
        print("\n❌ API is not accessible. Please check if it's running.")
        return
    
    # Run tests
    test_single_translation()
    test_batch_translation()
    test_rate_limiting()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\n💡 Tips:")
    print("  - If you see rate limit errors, wait a moment and try again")
    print("  - Use batch translation for multiple texts to avoid rate limits")
    print("  - The API automatically retries with exponential backoff")

if __name__ == "__main__":
    main()
