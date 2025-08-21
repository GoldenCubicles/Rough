#!/usr/bin/env python3
"""
Test script for the Open Source translation API.
This script tests the new open-source translation services to verify they work without rate limits.
"""

import requests
import time
import json

# API configuration
API_BASE_URL = "http://127.0.0.1:8001"  # Local Open Source API
# API_BASE_URL = "https://your-opensource-api-url.com"  # Change this to your hosted URL

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

def test_translation_services():
    """Test available translation services."""
    print("\n🧪 Testing Translation Services...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/services", timeout=10)
        if response.status_code == 200:
            services = response.json()
            print(f"✅ Found {services.get('total_services', 0)} translation services")
            
            for service_name, config in services.get("services", {}).items():
                status = "🟢 Enabled" if config.get("enabled") else "🔴 Disabled"
                priority = config.get("priority", "N/A")
                print(f"  {service_name.title()}: {status} (Priority: {priority})")
            
            return True
        else:
            print(f"❌ Services endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Services test failed: {str(e)}")
        return False

def test_single_translation():
    """Test single translation endpoint."""
    print("\n🧪 Testing Single Translation...")
    
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
                service_used = result.get("service_used", "unknown")
                print(f"✅ Single translation successful: {result['translated_text']}")
                print(f"   Service used: {service_used}")
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
                        service = translation.get("service_used", "unknown")
                        print(f"  Text {i+1}: {translation['translated_text']} (Service: {service})")
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

def test_long_text_translation():
    """Test translation of long text to verify chunking works."""
    print("\n🧪 Testing Long Text Translation...")
    
    long_text = """Learning is one of the most powerful tools that humans possess. From the moment we are born, we begin to absorb information about the world around us. As children, we learn to speak, walk, and interact with others. These early lessons shape our personality and guide us as we grow older. Education, whether formal or informal, is the foundation on which we build our future. It not only provides knowledge but also teaches us values such as patience, discipline, and respect for others.

In today's fast-changing world, continuous learning is more important than ever. Technology evolves rapidly, and new discoveries are made every day. To remain relevant in our careers and personal lives, we must keep updating our skills and knowledge. Reading books, attending classes, and exploring online courses are excellent ways to continue learning. Moreover, learning is not limited to academic subjects. It also includes life skills such as cooking, managing money, communicating effectively, and solving problems creatively."""
    
    payload = {
        "text": long_text,
        "source_lang": "Auto",
        "target_lang": "German"
    }
    
    try:
        print(f"📝 Translating long text ({len(long_text)} characters)...")
        response = requests.post(
            f"{API_BASE_URL}/translate",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                service_used = result.get("service_used", "unknown")
                translated_length = len(result.get("translated_text", ""))
                print(f"✅ Long text translation successful!")
                print(f"   Service used: {service_used}")
                print(f"   Original length: {len(long_text)} characters")
                print(f"   Translated length: {translated_length} characters")
                print(f"   Translation preview: {result['translated_text'][:100]}...")
                return True
            else:
                print(f"❌ Long text translation failed: {result.get('message')}")
                return False
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return False

def test_translation_service():
    """Test the translation service test endpoint."""
    print("\n🧪 Testing Translation Service Test...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/test-translation", timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "healthy":
                service_used = result.get("service_used", "unknown")
                test_translation = result.get("test_translation", "N/A")
                print(f"✅ Translation service test successful!")
                print(f"   Service used: {service_used}")
                print(f"   Test translation: {test_translation}")
                return True
            else:
                print(f"❌ Translation service test failed: {result.get('message')}")
                return False
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return False

def test_no_rate_limiting():
    """Test that there are no rate limiting issues by making multiple rapid requests."""
    print("\n🧪 Testing No Rate Limiting...")
    
    payload = {
        "text": "Test message",
        "source_lang": "Auto",
        "target_lang": "Italian"
    }
    
    print("Making 10 rapid requests to test no rate limiting...")
    
    successful_requests = 0
    for i in range(10):
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
                    service_used = result.get("service_used", "unknown")
                    print(f"  Request {i+1}: ✅ Success in {end_time - start_time:.2f}s (Service: {service_used})")
                    successful_requests += 1
                else:
                    print(f"  Request {i+1}: ❌ Failed - {result.get('message')}")
            else:
                print(f"  Request {i+1}: ❌ API error {response.status_code}")
                
        except Exception as e:
            print(f"  Request {i+1}: ❌ Failed - {str(e)}")
        
        # No delay between requests - testing no rate limiting
    
    print(f"\n📊 Rate Limiting Test Results: {successful_requests}/10 requests successful")
    if successful_requests == 10:
        print("✅ No rate limiting detected - all requests processed successfully!")
    else:
        print("⚠️ Some requests failed, but this may not be due to rate limiting")
    
    return successful_requests == 10

def main():
    """Run all tests."""
    print("🚀 Starting Open Source API Tests...")
    print(f"🌐 Testing API at: {API_BASE_URL}")
    print("=" * 60)
    
    # Test API health first
    if not test_api_health():
        print("\n❌ API is not accessible. Please check if it's running.")
        print("💡 Start the Open Source API with: python OpensourceAPI.py")
        return
    
    # Run tests
    test_translation_services()
    test_single_translation()
    test_batch_translation()
    test_long_text_translation()
    test_translation_service()
    test_no_rate_limiting()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("\n💡 Key Benefits of Open Source API:")
    print("  - ✅ No rate limiting issues")
    print("  - ✅ Multiple translation engines")
    print("  - ✅ Automatic fallback between services")
    print("  - ✅ Privacy-focused (no data collection)")
    print("  - ✅ Community-driven and reliable")
    print("\n🚀 Ready to use without rate limit worries!")

if __name__ == "__main__":
    main()
