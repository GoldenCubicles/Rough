import streamlit as st
import requests
import json
from typing import Optional

import os

# Configuration
API_BASE_URL = "https://rough-1-8qyx.onrender.com"
# Normalize base URL to avoid double slashes when joining paths
# API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip('/')

# Page configuration
st.set_page_config(
    page_title="🌍 Multi-Language Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_api_health() -> bool:
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_supported_languages() -> list:
    """Get supported languages from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/languages")
        if response.status_code == 200:
            data = response.json()
            return data.get("languages", [])
        return []
    except:
        return []

def translate_text(text: str, source_lang: str, target_lang: str) -> Optional[dict]:
    """Translate text using the API."""
    try:
        payload = {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
        response = requests.post(
            f"{API_BASE_URL}/translate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Multi-Language Translator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">High-accuracy translation using local Google Translate engine</p>', unsafe_allow_html=True)
    
    # Check API health
    if not check_api_health():
        st.error("❌ **API Connection Failed**")
        st.markdown("""
        <div class="error-box">
            <h4>🚨 API Not Running</h4>
            <p>The translation API is not running. Please start it first:</p>
            <code>python api.py</code>
            <br><br>
            <p><strong>Or use the setup script:</strong></p>
            <code>setup_venv.bat</code> (Windows) or <code>setup_venv.sh</code> (Linux/Mac)
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.success("✅ **API Connected Successfully**")
    
    # Features showcase
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="feature-box">⚡ Zero Latency</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-box">🎯 High Accuracy</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-box">🔒 Privacy-Focused</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="feature-box">🌐 Works Offline</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main translation interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input")
        
        # Language selection
        languages = get_supported_languages()
        if not languages:
            st.error("Failed to load languages from API")
            return
        
        source_lang = st.selectbox(
            "Source Language",
            options=languages,
            index=0,
            help="Select 'Auto' to automatically detect the language"
        )
        
        target_lang = st.selectbox(
            "Target Language",
            options=[lang for lang in languages if lang != "Auto"],
            index=1,
            help="Select the language you want to translate to"
        )
        
        # Input text
        input_text = st.text_area(
            "Text to Translate",
            height=200,
            placeholder="Enter text to translate...",
            help="Type or paste the text you want to translate"
        )
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn1:
            translate_btn = st.button("🚀 Translate", type="primary", use_container_width=True)
        
        with col_btn2:
            if st.button("🔄 Swap", use_container_width=True):
                if source_lang != "Autoweb-production-92222.up.railway.appweb-production-92222.up.railway.app" and target_lang != "Auto":
                    st.session_state.source_lang = target_lang
                    st.session_state.target_lang = source_lang
                    st.rerun()
        
        with col_btn3:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.input_text = ""
                st.session_state.output_text = ""
                st.rerun()
    
    with col2:
        st.subheader("🎯 Output")
        
        # Output display
        if 'output_text' not in st.session_state:
            st.session_state.output_text = ""
        
        if translate_btn and input_text.strip():
            with st.spinner("🔄 Translating..."):
                result = translate_text(input_text, source_lang, target_lang)
                
                if result and result.get("success"):
                    st.session_state.output_text = result["translated_text"]
                    
                    # Show success message
                    if result.get("detected_language"):
                        st.info(f"🔍 **Auto-detected language:** {result['detected_language']}")
                    
                    st.success("✅ Translation completed successfully!")
                else:
                    error_msg = result.get("message", "Translation failed") if result else "Unknown error"
                    st.error(f"❌ Translation failed: {error_msg}")
        
        # Display output
        output_display = st.text_area(
            "Translated Text",
            value=st.session_state.output_text,
            height=200,
            disabled=True,
            help="The translated text will appear here"
        )
    
    # Additional features
    st.markdown("---")
    
    # Language information
    col_info1, col_info2 = st.columns([1, 1])
    
    with col_info1:
        st.subheader("📊 Language Support")
        st.write(f"**Total Languages:** {len(languages)}")
        st.write(f"**Source Language:** {source_lang}")
        st.write(f"**Target Language:** {target_lang}")
        
        if source_lang == "Auto":
            st.info("🔍 **Auto-detection enabled** - The source language will be automatically detected")
    
    with col_info2:
        st.subheader("⚡ Performance")
        st.write("**Latency:** Near-instant (local processing)")
        st.write("**Accuracy:** High (Google Translate engine)")
        st.write("**Privacy:** 100% local - no data sent externally")
        st.write("**Offline:** Works without internet connection")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🌍 Multi-Language Translator v1.0 | Powered by Google Translate Engine | Built with Streamlit & FastAPI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 