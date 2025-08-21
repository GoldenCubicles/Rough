#!/usr/bin/env python3
"""
Debug script to test translation API and identify issues.
This will help figure out why the API is returning the same text instead of translated text.
"""

import requests
import json
import time

# API configuration
API_BASE_URL = "http://127.0.0.1:8000"  # Your Google Translate API

def test_api_health():
    """Test if the API is running."""
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

def test_translation_endpoint():
    """Test the translation endpoint directly."""
    print("\n🧪 Testing Translation Endpoint...")
    
    payload = {
        "text": "Hello world",
        "source_lang": "Auto",
        "target_lang": "Spanish"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/translate",
            json=payload,
            timeout=60
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response JSON: {json.dumps(result, indent=2)}")
            
            if result.get("success"):
                original_text = payload["text"]
                translated_text = result.get("translated_text", "")
                
                print(f"\n📝 Original Text: '{original_text}'")
                print(f"🎯 Translated Text: '{translated_text}'")
                
                if translated_text == original_text:
                    print("❌ PROBLEM: Translation returned same text!")
                    return False
                else:
                    print("✅ Translation working correctly!")
                    return True
            else:
                print(f"❌ Translation failed: {result.get('message')}")
                return False
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return False

def test_simple_translation():
    """Test with a very simple translation."""
    print("\n🧪 Testing Simple Translation...")
    
    payload = {
        "text": "Hi",
        "source_lang": "English",
        "target_lang": "French"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/translate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            if result.get("success"):
                original = payload["text"]
                translated = result.get("translated_text", "")
                
                print(f"Original: '{original}'")
                print(f"Translated: '{translated}'")
                
                if translated == original:
                    print("❌ Still returning same text!")
                else:
                    print("✅ Simple translation working!")
                    
                return translated != original
            else:
                print(f"Failed: {result.get('message')}")
                return False
        else:
            print(f"Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_language_codes():
    """Test if language codes are being resolved correctly."""
    print("\n🧪 Testing Language Code Resolution...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/languages", timeout=10)
        if response.status_code == 200:
            languages = response.json()
            print(f"Available languages: {languages.get('languages', [])[:10]}...")
            
            # Test specific language codes
            test_cases = [
                ("English", "Spanish"),
                ("English", "French"),
                ("English", "German")
            ]
            
            for source, target in test_cases:
                payload = {
                    "text": "Hello",
                    "source_lang": source,
                    "target_lang": target
                }
                
                print(f"\nTesting: {source} -> {target}")
                response = requests.post(f"{API_BASE_URL}/translate", json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        original = payload["text"]
                        translated = result.get("translated_text", "")
                        print(f"  '{original}' -> '{translated}'")
                        
                        if translated == original:
                            print(f"  ❌ {source}->{target} failed - same text returned")
                        else:
                            print(f"  ✅ {source}->{target} working")
                    else:
                        print(f"  ❌ {source}->{target} failed: {result.get('message')}")
                else:
                    print(f"  ❌ {source}->{target} API error: {response.status_code}")
                    
        else:
            print(f"Failed to get languages: {response.status_code}")
            
    except Exception as e:
        print(f"Language test failed: {str(e)}")

def test_rate_limit_status():
    """Check rate limiting status."""
    print("\n🧪 Checking Rate Limit Status...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/rate-limit-status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print(f"Rate Limit Status: {json.dumps(status, indent=2)}")
        else:
            print(f"Rate limit status failed: {response.status_code}")
    except Exception as e:
        print(f"Rate limit check failed: {str(e)}")

def test_translation_test_endpoint():
    """Test the new test-translation endpoint."""
    print("\n🧪 Testing Translation Test Endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/test-translation", timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"Test Result: {json.dumps(result, indent=2)}")
            
            if result.get("status") == "healthy":
                print("✅ Translation test endpoint working!")
            else:
                print("❌ Translation test endpoint shows issues!")
                
        else:
            print(f"Test endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"Test endpoint error: {str(e)}")

def main():
    """Run all debug tests."""
    print("🔍 Translation API Debug Script")
    print(f"🌐 Testing API at: {API_BASE_URL}")
    print("=" * 60)
    
    # Test API health first
    if not test_api_health():
        print("\n❌ API is not accessible. Please check if it's running.")
        return
    
    # Run all tests
    test_translation_endpoint()
    test_simple_translation()
    test_language_codes()
    test_rate_limit_status()
    test_translation_test_endpoint()
    
    print("\n" + "=" * 60)
    print("🎯 Debug Summary:")
    print("1. Check if the API is running and accessible")
    print("2. Verify language codes are being resolved correctly")
    print("3. Check if Google Translate is working")
    print("4. Look for rate limiting issues")
    print("5. Check the logs for detailed error messages")
    
    print("\n💡 Next Steps:")
    print("- Check the API logs for detailed error messages")
    print("- Verify your internet connection (Google Translate needs it)")
    print("- Try the Open Source API if Google Translate continues to fail")
    print("- Use the test-translation endpoint to verify functionality")

if __name__ == "__main__":
    main()
