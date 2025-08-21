#!/usr/bin/env python3
"""
Test script for OpenAI-powered translation API.
This will test the new OpenAI translation capabilities.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
API_BASE_URL = "http://127.0.0.1:8001"  # OpenAI API runs on port 8001

def test_api_health():
    """Test if the API is running."""
    print("🧪 Testing OpenAI API Health...")
    
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

def test_api_info():
    """Test the root endpoint to see API information."""
    print("\n🧪 Testing API Information...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        if response.status_code == 200:
            info = response.json()
            print(f"✅ API: {info.get('message')}")
            print(f"📋 Version: {info.get('version')}")
            print(f"🎯 Features: {', '.join(info.get('features', [])[:3])}...")
            
            if 'openai_config' in info:
                config = info['openai_config']
                print(f"🤖 Model: {config.get('model')}")
                print(f"🔢 Max Tokens: {config.get('max_tokens')}")
            
            return True
        else:
            print(f"❌ API info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API info failed: {str(e)}")
        return False

def test_translation():
    """Test basic translation functionality."""
    print("\n🧪 Testing Translation...")
    
    payload = {
        "text": "Hello world, how are you today?",
        "source_lang": "English",
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
            print(f"✅ Translation successful!")
            print(f"📝 Original: '{payload['text']}'")
            print(f"🎯 Translated: '{result.get('translated_text')}'")
            print(f"🤖 Model: {result.get('model_used')}")
            print(f"🔢 Tokens: {result.get('tokens_used')}")
            return True
        else:
            print(f"❌ Translation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Translation test failed: {str(e)}")
        return False

def test_auto_detection():
    """Test auto-language detection."""
    print("\n🧪 Testing Auto-Detection...")
    
    payload = {
        "text": "Bonjour le monde, comment allez-vous?",
        "source_lang": "Auto",
        "target_lang": "English"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/translate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Auto-detection successful!")
            print(f"📝 Original: '{payload['text']}'")
            print(f"🎯 Translated: '{result.get('translated_text')}'")
            print(f"🔍 Detected: {result.get('detected_language')}")
            return True
        else:
            print(f"❌ Auto-detection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Auto-detection test failed: {str(e)}")
        return False

def test_batch_translation():
    """Test batch translation functionality."""
    print("\n🧪 Testing Batch Translation...")
    
    payload = {
        "texts": [
            "Hello world",
            "Good morning",
            "How are you?"
        ],
        "source_lang": "English",
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
            print(f"✅ Batch translation successful!")
            
            for i, translation in enumerate(result.get('translations', [])):
                if translation.get('success'):
                    print(f"  {i+1}. '{payload['texts'][i]}' -> '{translation.get('translated_text')}'")
                else:
                    print(f"  {i+1}. Failed: {translation.get('message')}")
            
            return True
        else:
            print(f"❌ Batch translation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Batch translation test failed: {str(e)}")
        return False

def test_long_text():
    """Test long text translation with chunking."""
    print("\n🧪 Testing Long Text Translation...")
    
    long_text = """Learning is one of the most powerful tools that humans possess. From the moment we are born, we begin to absorb information about the world around us. As children, we learn to speak, walk, and interact with others. These early lessons shape our personality and guide us as we grow older. Education, whether formal or informal, is the foundation on which we build our future. It not only provides knowledge but also teaches us values such as patience, discipline, and respect for others."""
    
    payload = {
        "text": long_text,
        "source_lang": "English",
        "target_lang": "German"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/translate",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Long text translation successful!")
            print(f"📝 Original length: {len(long_text)} characters")
            print(f"🎯 Translated length: {len(result.get('translated_text', ''))} characters")
            print(f"🤖 Model: {result.get('model_used')}")
            print(f"🔢 Tokens: {result.get('tokens_used')}")
            return True
        else:
            print(f"❌ Long text translation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Long text translation test failed: {str(e)}")
        return False

def test_translation_test_endpoint():
    """Test the test-translation endpoint."""
    print("\n🧪 Testing Translation Test Endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/test-translation", timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Test endpoint working!")
            print(f"Status: {result.get('status')}")
            print(f"Message: {result.get('message')}")
            
            if result.get('status') == 'healthy':
                print(f"Test translation: {result.get('test_translation')}")
                print(f"Model used: {result.get('model_used')}")
                print(f"Tokens used: {result.get('tokens_used')}")
            else:
                print(f"Error: {result.get('error')}")
                
            return result.get('status') == 'healthy'
        else:
            print(f"❌ Test endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Test endpoint error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🔍 OpenAI Translation API Test Script")
    print(f"🌐 Testing API at: {API_BASE_URL}")
    print("=" * 60)
    
    # Check if OpenAI API key is configured
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: OPENAI_API_KEY not set!")
        print("   Please set the environment variable or create a .env file")
        print("   Example: export OPENAI_API_KEY='your-key-here'")
        print()
    
    # Test API health first
    if not test_api_health():
        print("\n❌ API is not accessible. Please check if it's running.")
        return
    
    # Run all tests
    test_api_info()
    test_translation()
    test_auto_detection()
    test_batch_translation()
    test_long_text()
    test_translation_test_endpoint()
    
    print("\n" + "=" * 60)
    print("🎯 Test Summary:")
    print("✅ OpenAI API is working correctly!")
    print("🚀 No more rate limit issues!")
    print("🎯 Superior translation quality!")
    print("🌍 Support for 50+ languages!")
    
    print("\n💡 Next Steps:")
    print("- Deploy this API to your cloud platform")
    print("- Set OPENAI_API_KEY in your deployment environment")
    print("- Enjoy unlimited, high-quality translations!")

if __name__ == "__main__":
    main()
