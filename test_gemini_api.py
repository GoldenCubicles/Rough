#!/usr/bin/env python3
"""
Test script for Gemini-Powered Multi-Language Translator API
"""

import requests
import json
import time

# API Configuration
API_BASE_URL = "http://127.0.0.1:8002"  # Gemini API runs on port 8002

def test_api_health():
    """Test API health endpoint."""
    print("🔍 Testing API Health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"   Model: {data['model']}")
            print(f"   Provider: {data['api_provider']}")
            print(f"   Free Tier: {data['free_tier_info']}")
            return True
        else:
            print(f"❌ API Health Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health Error: {e}")
        return False

def test_api_info():
    """Test API root endpoint."""
    print("\n🔍 Testing API Info...")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Info: {data['message']}")
            print(f"   Version: {data['version']}")
            print(f"   Model: {data['model']}")
            print(f"   Provider: {data['provider']}")
            print(f"   Free Tier: {data['free_tier']}")
            return True
        else:
            print(f"❌ API Info Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Info Error: {e}")
        return False

def test_languages():
    """Test languages endpoint."""
    print("\n🔍 Testing Languages...")
    try:
        response = requests.get(f"{API_BASE_URL}/languages", timeout=10)
        if response.status_code == 200:
            data = response.json()
            languages = data['languages']
            print(f"✅ Languages: {data['total_count']} supported")
            print(f"   First 10: {languages[:10]}")
            return languages
        else:
            print(f"❌ Languages Failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Languages Error: {e}")
        return []

def test_translation():
    """Test translation endpoint."""
    print("\n🔍 Testing Translation...")
    
    test_cases = [
        {
            "text": "Hello, how are you today?",
            "source_lang": "English",
            "target_lang": "Spanish"
        },
        {
            "text": "Learning is one of the most powerful tools that humans possess.",
            "source_lang": "English", 
            "target_lang": "French"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['source_lang']} → {test_case['target_lang']}")
        try:
            response = requests.post(
                f"{API_BASE_URL}/translate",
                json=test_case,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"   ✅ Success: {data['translated_text'][:50]}...")
                    print(f"      Model: {data['model_used']}")
                    if data.get('tokens_used'):
                        print(f"      Tokens: {data['tokens_used']}")
                else:
                    print(f"   ❌ Failed: {data.get('message', 'Unknown error')}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                print(f"      Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Small delay between tests
        time.sleep(1)

def test_auto_detection():
    """Test auto language detection."""
    print("\n🔍 Testing Auto Language Detection...")
    
    test_cases = [
        {
            "text": "Bonjour, comment allez-vous?",
            "source_lang": "Auto",
            "target_lang": "English"
        },
        {
            "text": "Hola, ¿cómo estás?",
            "source_lang": "Auto",
            "target_lang": "English"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: Auto → {test_case['target_lang']}")
        try:
            response = requests.post(
                f"{API_BASE_URL}/translate",
                json=test_case,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"   ✅ Success: {data['translated_text'][:50]}...")
                    if data.get('detected_language'):
                        print(f"      Detected: {data['detected_language']}")
                    print(f"      Model: {data['model_used']}")
                else:
                    print(f"   ❌ Failed: {data.get('message', 'Unknown error')}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)

def test_batch_translation():
    """Test batch translation endpoint."""
    print("\n🔍 Testing Batch Translation...")
    
    test_texts = [
        "Hello world",
        "How are you?",
        "Good morning",
        "Have a nice day"
    ]
    
    payload = {
        "texts": test_texts,
        "source_lang": "English",
        "target_lang": "German"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/translate_batch",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Batch Success: {data['successful_translations']}/{data['total_texts']}")
                for i, translation in enumerate(data['translations']):
                    if translation['success']:
                        print(f"   {i+1}. ✅ {translation['translated_text'][:30]}...")
                    else:
                        print(f"   {i+1}. ❌ {translation.get('message', 'Failed')}")
            else:
                print(f"❌ Batch Failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Batch Error: {e}")

def test_long_text():
    """Test long text translation."""
    print("\n🔍 Testing Long Text Translation...")
    
    long_text = """
    Learning is one of the most powerful tools that humans possess. From the moment we are born, 
    we begin to absorb information about the world around us. As children, we learn to speak, 
    walk, and interact with others. These early lessons shape our personality and guide us as we grow.
    
    Education, whether formal or informal, is the foundation on which we build our future. 
    It not only provides knowledge but also teaches us values such as patience, discipline, 
    and respect for others. In today's fast-changing world, continuous learning is more important than ever.
    
    Technology evolves rapidly, and new discoveries are made every day. To remain relevant in our 
    careers and personal lives, we must keep updating our skills and knowledge. Reading books, 
    attending classes, and exploring online courses are excellent ways to continue learning.
    """
    
    payload = {
        "text": long_text.strip(),
        "source_lang": "English",
        "target_lang": "Italian"
    }
    
    try:
        print("   Translating long text (will be split into chunks)...")
        response = requests.post(
            f"{API_BASE_URL}/translate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"   ✅ Success: {data['translated_text'][:100]}...")
                print(f"      Model: {data['model_used']}")
                if data.get('tokens_used'):
                    print(f"      Total Tokens: {data['tokens_used']}")
            else:
                print(f"   ❌ Failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_translation_endpoint():
    """Test the test-translation endpoint."""
    print("\n🔍 Testing Test Translation Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/test-translation", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Test Translation: {data['translated_text']}")
                print(f"   Model: {data['model_used']}")
                if data.get('tokens_used'):
                    print(f"   Tokens: {data['tokens_used']}")
            else:
                print(f"❌ Test Failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test Error: {e}")

def main():
    """Run all tests."""
    print("🚀 Gemini API Test Suite")
    print("=" * 50)
    
    # Check if API is running
    if not test_api_health():
        print("\n❌ API is not running. Please start it first:")
        print("   python GeminiAPI.py")
        return
    
    # Run all tests
    test_api_info()
    languages = test_languages()
    
    if languages:
        test_translation()
        test_auto_detection()
        test_batch_translation()
        test_long_text()
        test_translation_endpoint()
    
    print("\n" + "=" * 50)
    print("🎉 Test suite completed!")
    print("\n💡 Tips:")
    print("   - Make sure you have set your Gemini API key in GeminiAPI.py")
    print("   - Get your free API key from: https://makersuite.google.com/app/apikey")
    print("   - Free tier: 15 requests/minute, 1,500 requests/day")

if __name__ == "__main__":
    main()

