import requests
import json

# Your local API URL
RAILWAY_URL = "http://127.0.0.1:8080"

def test_health():
    """Test the health endpoint."""
    try:
        response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
        print(f"✅ Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_root():
    """Test the root endpoint."""
    try:
        response = requests.get(f"{RAILWAY_URL}/", timeout=10)
        print(f"✅ Root Endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Root Endpoint Failed: {e}")
        return False

def test_languages():
    """Test the languages endpoint."""
    try:
        response = requests.get(f"{RAILWAY_URL}/languages", timeout=10)
        print(f"✅ Languages Endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Languages Endpoint Failed: {e}")
        return False

def test_translation():
    """Test the translation endpoint."""
    try:
        payload = {
            "text": "Hello world",
            "source_lang": "Auto",
            "target_lang": "Spanish"
        }
        
        response = requests.post(
            f"{RAILWAY_URL}/translate",
            json=payload,
            timeout=30
        )
        
        print(f"✅ Translation Endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Translation Endpoint Failed: {e}")
        return False

def main():
    print("🚀 Testing Railway API Endpoints")
    print("=" * 50)
    
    # Test all endpoints
    health_ok = test_health()
    print()
    
    root_ok = test_root()
    print()
    
    languages_ok = test_languages()
    print()
    
    translation_ok = test_translation()
    print()
    
    # Summary
    print("=" * 50)
    print("📊 Test Results:")
    print(f"Health: {'✅' if health_ok else '❌'}")
    print(f"Root: {'✅' if root_ok else '❌'}")
    print(f"Languages: {'✅' if languages_ok else '❌'}")
    print(f"Translation: {'✅' if translation_ok else '❌'}")
    
    if all([health_ok, root_ok, languages_ok, translation_ok]):
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main() 