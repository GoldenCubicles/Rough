import streamlit as st
import requests
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🌍 Gemini Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        text-align: center;
    }
    .stButton > button {
        width: 100%;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
GEMINI_API_BASE_URL = "http://127.0.0.1:8002"  # Default Gemini API URL

# Initialize session state
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
if 'api_status' not in st.session_state:
    st.session_state.api_status = "unknown"

def check_api_health():
    """Check if the Gemini API is running."""
    try:
        response = requests.get(f"{GEMINI_API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.session_state.api_status = "healthy"
            return True
        else:
            st.session_state.api_status = "error"
            return False
    except requests.exceptions.RequestException:
        st.session_state.api_status = "offline"
        return False

def get_rate_limit_status():
    """Get current rate limit status from Gemini API."""
    try:
        response = requests.get(f"{GEMINI_API_BASE_URL}/rate-limit-status", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def get_supported_languages():
    """Get supported languages from Gemini API."""
    try:
        response = requests.get(f"{GEMINI_API_BASE_URL}/languages", timeout=5)
        if response.status_code == 200:
            return response.json()["languages"]
        else:
            return []
    except requests.exceptions.RequestException:
        return []

def translate_text(text, source_lang, target_lang):
    """Translate text using Gemini API."""
    try:
        payload = {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
        response = requests.post(
            f"{GEMINI_API_BASE_URL}/translate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json()
            raise Exception(error_data.get("detail", "Translation failed"))
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except Exception as e:
        raise Exception(str(e))

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Gemini Translator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by Google Gemini AI - High-quality translations with rate limiting</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API URL configuration
        api_url = st.text_input(
            "Gemini API URL",
            value=GEMINI_API_BASE_URL,
            help="URL of your Gemini API server"
        )
        
        if api_url != GEMINI_API_BASE_URL:
            GEMINI_API_BASE_URL = api_url
        
        # API Status
        st.subheader("🔍 API Status")
        if st.button("Check API Health", key="health_check"):
            check_api_health()
        
        if st.session_state.api_status == "healthy":
            st.success("✅ API is running")
        elif st.session_state.api_status == "error":
            st.error("❌ API error")
        elif st.session_state.api_status == "offline":
            st.error("🔌 API is offline")
        else:
            st.info("ℹ️ Check API status")
        
        # Rate Limit Status
        st.subheader("📊 Rate Limits")
        if st.button("Check Rate Limits", key="rate_check"):
            rate_status = get_rate_limit_status()
            if rate_status:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("This Minute", f"{rate_status['requests_this_minute']}/{rate_status['max_requests_per_minute']}")
                with col2:
                    st.metric("Today", f"{rate_status['requests_today']}/{rate_status['max_requests_per_day']}")
                
                if rate_status['can_make_request']:
                    st.success("✅ Can make requests")
                else:
                    wait_time = rate_status['wait_time_seconds']
                    st.warning(f"⏳ Wait {wait_time}s")
            else:
                st.error("❌ Could not fetch rate limit status")
        
        # Free Tier Info
        st.subheader("💰 Free Tier Info")
        st.info("""
        **Gemini 1.0 Pro Free Tier:**
        - 10 requests per minute
        - 1,000 requests per day
        - Rate limiting enabled
        """)
        
        # Clear History
        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state.translation_history = []
            st.success("History cleared!")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input")
        
        # Language selection
        languages = get_supported_languages()
        if not languages:
            languages = ["Auto", "English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Chinese", "Japanese", "Korean", "Arabic", "Hindi"]
        
        source_lang = st.selectbox("From Language", languages, index=0)
        target_lang = st.selectbox("To Language", languages[1:], index=0)  # Exclude "Auto" from target
        
        # Text input
        input_text = st.text_area(
            "Text to Translate",
            height=200,
            placeholder="Enter text to translate...",
            help="Enter the text you want to translate"
        )
        
        # Translation controls
        col1_1, col1_2, col1_3 = st.columns(3)
        
        with col1_1:
            if st.button("🚀 Translate", type="primary", key="translate_btn"):
                if input_text.strip():
                    with st.spinner("Translating with Gemini..."):
                        try:
                            result = translate_text(input_text, source_lang, target_lang)
                            
                            if result.get("success"):
                                # Add to history
                                translation_entry = {
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "source_lang": source_lang,
                                    "target_lang": target_lang,
                                    "input_text": input_text[:100] + "..." if len(input_text) > 100 else input_text,
                                    "translated_text": result["translated_text"][:100] + "..." if len(result["translated_text"]) > 100 else result["translated_text"],
                                    "model_used": result.get("model_used", "Unknown"),
                                    "tokens_used": result.get("tokens_used", "Unknown")
                                }
                                st.session_state.translation_history.insert(0, translation_entry)
                                
                                # Store full result for display
                                st.session_state.last_translation = result
                                st.success("✅ Translation completed!")
                            else:
                                st.error(f"❌ Translation failed: {result.get('message', 'Unknown error')}")
                                
                        except Exception as e:
                            st.error(f"❌ Translation failed: {str(e)}")
                else:
                    st.warning("⚠️ Please enter text to translate")
        
        with col1_2:
            if st.button("🔄 Swap Languages", key="swap_btn"):
                if source_lang != "Auto":
                    st.session_state.swap_languages = True
        
        with col1_3:
            if st.button("🗑️ Clear", key="clear_btn"):
                st.session_state.last_translation = None
                st.experimental_rerun()
        
        # Handle language swap
        if st.session_state.get("swap_languages", False):
            if source_lang != "Auto":
                temp = source_lang
                source_lang = target_lang
                target_lang = temp
                st.session_state.swap_languages = False
                st.experimental_rerun()
    
    with col2:
        st.subheader("🎯 Output")
        
        if hasattr(st.session_state, 'last_translation') and st.session_state.last_translation:
            result = st.session_state.last_translation
            
            # Display translated text
            st.text_area(
                "Translated Text",
                value=result["translated_text"],
                height=200,
                disabled=True
            )
            
            # Translation details
            st.subheader("📊 Translation Details")
            
            col2_1, col2_2, col2_3 = st.columns(3)
            
            with col2_1:
                st.metric("Source Language", source_lang)
            
            with col2_2:
                st.metric("Target Language", target_lang)
            
            with col2_3:
                if result.get("detected_language"):
                    st.metric("Detected Language", result["detected_language"])
                else:
                    st.metric("Model Used", result.get("model_used", "Unknown"))
            
            # Additional info
            if result.get("tokens_used"):
                st.info(f"💡 Tokens used: {result['tokens_used']}")
            
            # Copy button
            if st.button("📋 Copy Translation", key="copy_btn"):
                st.write("Translation copied to clipboard!")
                st.balloons()
        else:
            st.info("💡 Enter text and click Translate to get started!")
    
    # Translation History
    if st.session_state.translation_history:
        st.subheader("📚 Translation History")
        
        for i, entry in enumerate(st.session_state.translation_history[:10]):  # Show last 10
            with st.expander(f"{entry['timestamp']} - {entry['source_lang']} → {entry['target_lang']}"):
                col_h1, col_h2 = st.columns(2)
                
                with col_h1:
                    st.write("**Input:**")
                    st.write(entry['input_text'])
                
                with col_h2:
                    st.write("**Output:**")
                    st.write(entry['translated_text'])
                
                st.caption(f"Model: {entry['model_used']} | Tokens: {entry['tokens_used']}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">🌍 Gemini Translator v1.0 | Powered by Google Gemini AI | Built with ❤️</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

