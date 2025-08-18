#!/usr/bin/env python3
"""
Test script to verify the translator application setup.
Run this before running the main app to check for any issues.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import gradio as gr
        print("✅ Gradio imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Gradio: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        from languages import LANGUAGES, get_supported_languages
        print("✅ Local languages module imported successfully")
        print(f"   Found {len(get_supported_languages())} supported languages")
    except ImportError as e:
        print(f"❌ Failed to import local languages module: {e}")
        return False
    
    return True

def test_environment():
    """Test environment setup."""
    print("\n🔍 Testing environment...")
    
    # Test .env file loading
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env file loading works")
    except Exception as e:
        print(f"⚠️  .env file loading issue: {e}")
    
    print("✅ No API key required - using free LibreTranslate API!")
    
    return True

def test_languages():
    """Test language functionality."""
    print("\n🔍 Testing language functionality...")
    
    try:
        from languages import get_language_code, get_language_name, get_supported_languages
        
        # Test language code retrieval
        test_lang = get_language_code("English")
        if test_lang == "en":
            print("✅ Language code retrieval works")
        else:
            print(f"❌ Language code retrieval failed: expected 'en', got '{test_lang}'")
            return False
        
        # Test language name retrieval
        test_name = get_language_name("es")
        if test_name == "Spanish":
            print("✅ Language name retrieval works")
        else:
            print(f"❌ Language name retrieval failed: expected 'Spanish', got '{test_name}'")
            return False
        
        # Test supported languages
        supported = get_supported_languages()
        if len(supported) >= 25:  # Should have 25+ languages
            print(f"✅ Found {len(supported)} supported languages")
        else:
            print(f"⚠️  Expected 25+ languages, found {len(supported)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Language functionality test failed: {e}")
        return False

def test_local_translation():
    """Test local translation functionality."""
    print("\n🔍 Testing local translation...")
    
    try:
        from deep_translator import GoogleTranslator
        
        # Test basic translation
        translator = GoogleTranslator(source='en', target='es')
        result = translator.translate("Hello")
        
        if result:
            print("✅ Local translation working successfully")
            print(f"   Example: 'Hello' -> '{result}' (English to Spanish)")
            return True
        else:
            print("❌ Translation returned empty result")
            return False
            
    except ImportError:
        print("❌ deep-translator library not found. Please install: pip install deep-translator")
        return False
    except Exception as e:
        print(f"❌ Local translation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Translator Application Setup Test (Free Version)")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    if not test_imports():
        all_passed = False
    
    if not test_environment():
        all_passed = False
    
    if not test_languages():
        all_passed = False
    
    if not test_local_translation():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Activate your virtual environment: 2ndTrans")
        print("2. Run: python app.py")
        print("3. Open http://localhost:7860 in your browser")
        print("\n✨ No API key required - completely free!")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Check your Python version (3.7+ required)")
        print("3. Verify all files are in the correct location")
        print("4. Check your internet connection for API access")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 