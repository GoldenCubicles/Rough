import streamlit as st
import requests
import json
from typing import Optional, List

import os

# Configuration for Open Source API
API_BASE_URL = "http://127.0.0.1:8001"  # Local Open Source API
# API_BASE_URL = "https://your-opensource-api-url.com"  # Change this to your hosted URL

# Page configuration
st.set_page_config(
    page_title="🌍 Open Source Multi-Language Translator",
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
        color: #28a745;
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
    .opensource-box {
        background-color: #d1f2eb;
        border: 1px solid #a8e6cf;
        color: #0e6655;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .service-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.375rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-left: 0.5rem;
    }
    .service-libretranslate {
        background-color: #e3f2fd;
        color: #1565c0;
    }
    .service-argos {
        background-color: #f3e5f5;
        color: #7b1fa2;
    }
    .service-marian {
        background-color: #e8f5e8;
        color: #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

def check_api_health() -> bool:
    """Check if the Open Source API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_supported_languages() -> list:
    """Get supported languages from Open Source API."""
    try:
        response = requests.get(f"{API_BASE_URL}/languages")
        if response.status_code == 200:
            data = response.json()
            return data.get("languages", [])
        return []
    except:
        return []

def get_translation_services() -> Optional[dict]:
    """Get available translation services from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/services", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def translate_text(text: str, source_lang: str, target_lang: str) -> Optional[dict]:
    """Translate text using the Open Source API."""
    try:
        payload = {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
        response = requests.post(
            f"{API_BASE_URL}/translate",
            json=payload,
            timeout=60
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

def translate_batch(texts: List[str], source_lang: str, target_lang: str) -> Optional[dict]:
    """Translate multiple texts using the batch API endpoint."""
    try:
        payload = {
            "texts": texts,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
        response = requests.post(
            f"{API_BASE_URL}/translate_batch",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Batch API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
        return None

def test_translation() -> Optional[dict]:
    """Test the translation services."""
    try:
        response = requests.get(f"{API_BASE_URL}/test-translation", timeout=30)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_service_badge_html(service_name: str) -> str:
    """Get HTML for service badge."""
    if not service_name or service_name == "none":
        return ""
    
    service_class = f"service-{service_name.lower()}"
    return f'<span class="service-badge {service_class}">{service_name}</span>'

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Open Source Multi-Language Translator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">High-accuracy translation using multiple open-source translation engines</p>', unsafe_allow_html=True)
    
    # Check API health
    if not check_api_health():
        st.error("❌ **Open Source API Connection Failed**")
        st.markdown("""
        <div class="error-box">
            <h4>🚨 Open Source API Not Running</h4>
            <p>The open-source translation API is not running. Please start it first:</p>
            <code>python OpensourceAPI.py</code>
            <br><br>
            <p><strong>Or use the setup script:</strong></p>
            <code>setup_venv.bat</code> (Windows) or <code>setup_venv.sh</code> (Linux/Mac)
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.success("✅ **Open Source API Connected Successfully**")
    
    # Get translation services info
    services_info = get_translation_services()
    if services_info:
        st.markdown("""
        <div class="opensource-box">
            <h4>🔧 Available Translation Services</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display services status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Services", services_info.get("total_services", 0))
        with col2:
            st.metric("Enabled Services", services_info.get("enabled_services", 0))
        with col3:
            st.metric("API Status", "🟢 Healthy")
    
    # Open source benefits
    st.markdown("""
    <div class="opensource-box">
        <h4>💚 Why Open Source Translation?</h4>
        <p><strong>✅ No Rate Limits:</strong> Unlike Google Translate, open-source services have no strict rate limits</p>
        <p><strong>🔒 Privacy-Focused:</strong> Your text stays private and isn't stored by big tech companies</p>
        <p><strong>🌐 Community-Driven:</strong> Supported by the open-source community worldwide</p>
        <p><strong>⚡ Reliable:</strong> Multiple fallback services ensure high availability</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features showcase
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="feature-box">🌐 Multiple Engines</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-box">🔄 Auto-Fallback</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-box">📦 Batch Support</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="feature-box">🎯 High Accuracy</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tab selection
    tab1, tab2, tab3 = st.tabs(["🚀 Single Translation", "📦 Batch Translation", "🧪 Service Test"])
    
    with tab1:
        # Single translation interface
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
                    if source_lang != "Auto" and target_lang != "Auto":
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
            if 'service_used' not in st.session_state:
                st.session_state.service_used = ""
            
            if translate_btn and input_text.strip():
                with st.spinner("🔄 Translating with open-source services..."):
                    result = translate_text(input_text, source_lang, target_lang)
                    
                    if result and result.get("success"):
                        st.session_state.output_text = result["translated_text"]
                        st.session_state.service_used = result.get("service_used", "unknown")
                        
                        # Show success message with service info
                        if result.get("detected_language"):
                            st.info(f"🔍 **Auto-detected language:** {result['detected_language']}")
                        
                        service_badge = get_service_badge_html(result.get("service_used"))
                        st.markdown(f'<div class="success-box">✅ Translation completed successfully! {service_badge}</div>', unsafe_allow_html=True)
                        
                        # Show which service was used
                        st.info(f"🔧 **Translation Service:** {result.get('service_used', 'Unknown').title()}")
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
    
    with tab2:
        # Batch translation interface
        st.subheader("📦 Batch Translation")
        st.info("💡 **Batch translation is more efficient and helps process multiple texts quickly.**")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Language selection for batch
            batch_source_lang = st.selectbox(
                "Source Language (Batch)",
                options=languages,
                index=0,
                help="Select 'Auto' to automatically detect the language"
            )
            
            batch_target_lang = st.selectbox(
                "Target Language (Batch)",
                options=[lang for lang in languages if lang != "Auto"],
                index=1,
                help="Select the language you want to translate to"
            )
            
            # Batch input
            batch_input = st.text_area(
                "Texts to Translate (One per line)",
                height=200,
                placeholder="Enter multiple texts, one per line...\n\nExample:\nHello world\nHow are you?\nGood morning",
                help="Enter multiple texts, one per line. Maximum 10 texts allowed."
            )
            
            # Parse texts
            texts = [text.strip() for text in batch_input.split('\n') if text.strip()]
            text_count = len(texts)
            
            if text_count > 10:
                st.error(f"❌ Too many texts! Maximum 10 allowed, you have {text_count}")
                texts = texts[:10]
                text_count = 10
            
            if text_count > 0:
                st.success(f"📊 **{text_count} texts ready for translation**")
            
            # Batch translate button
            batch_translate_btn = st.button("📦 Translate Batch", type="primary", use_container_width=True)
        
        with col2:
            st.subheader("🎯 Batch Output")
            
            if batch_translate_btn and texts:
                with st.spinner(f"🔄 Translating {text_count} texts with open-source services..."):
                    result = translate_batch(texts, batch_source_lang, batch_target_lang)
                    
                    if result and result.get("success"):
                        translations = result.get("translations", [])
                        
                        # Display results
                        for i, translation in enumerate(translations):
                            if translation.get("success"):
                                service_badge = get_service_badge_html(translation.get("service_used"))
                                st.markdown(f'<div class="success-box">✅ <strong>Text {i+1}:</strong> {translation["translated_text"]} {service_badge}</div>', unsafe_allow_html=True)
                            else:
                                st.error(f"❌ **Text {i+1}:** {translation.get('message', 'Translation failed')}")
                        
                        st.success(f"🎉 Batch translation completed! {len([t for t in translations if t.get('success')])}/{len(translations)} successful")
                    else:
                        error_msg = result.get("message", "Batch translation failed") if result else "Unknown error"
                        st.error(f"❌ Batch translation failed: {error_msg}")
            
            # Show batch info
            st.info("""
            **Batch Translation Benefits:**
            - More efficient than individual requests
            - Better service utilization
            - Faster processing for multiple texts
            - Automatic service fallback
            """)
    
    with tab3:
        # Service testing interface
        st.subheader("🧪 Test Translation Services")
        st.info("💡 **Test the available translation services to ensure they're working correctly.**")
        
        if st.button("🧪 Test All Services", type="primary", use_container_width=True):
            with st.spinner("Testing translation services..."):
                test_result = test_translation()
                
                if test_result and test_result.get("status") == "healthy":
                    st.success("✅ **All Services Working!**")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Test Status", "🟢 Healthy")
                        st.metric("Service Used", test_result.get("service_used", "Unknown").title())
                    
                    with col2:
                        st.metric("Test Translation", test_result.get("test_translation", "N/A"))
                        st.metric("Message", "Services OK")
                    
                    st.info(f"**Test Message:** {test_result.get('message', '')}")
                else:
                    st.error("❌ **Services Test Failed**")
                    if test_result:
                        st.error(f"Error: {test_result.get('error', 'Unknown error')}")
                        st.error(f"Message: {test_result.get('message', 'No message')}")
                    else:
                        st.error("Could not connect to test endpoint")
        
        # Service information
        if services_info:
            st.subheader("📊 Service Information")
            
            for service_name, config in services_info.get("services", {}).items():
                status_icon = "🟢" if config.get("enabled") else "🔴"
                priority = config.get("priority", "N/A")
                fallback = "✅" if config.get("fallback") else "❌"
                url = config.get("url", "Local installation required")
                
                st.write(f"{status_icon} **{service_name.title()}**")
                st.write(f"   Priority: {priority} | Fallback: {fallback} | URL: {url}")
                st.write("---")
    
    # Additional features
    st.markdown("---")
    
    # Language information
    col_info1, col_info2 = st.columns([1, 1])
    
    with col_info1:
        st.subheader("📊 Language Support")
        st.write(f"**Total Languages:** {len(languages)}")
        st.write(f"**Source Language:** {source_lang if 'source_lang' in locals() else 'Not selected'}")
        st.write(f"**Target Language:** {target_lang if 'target_lang' in locals() else 'Not selected'}")
        
        if 'source_lang' in locals() and source_lang == "Auto":
            st.info("🔍 **Auto-detection enabled** - The source language will be automatically detected")
    
    with col_info2:
        st.subheader("⚡ Open Source Benefits")
        st.write("**Rate Limits:** None - unlimited requests")
        st.write("**Privacy:** 100% private - no data collection")
        st.write("**Services:** Multiple fallback engines")
        st.write("**Community:** Open-source and community-driven")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🌍 Open Source Multi-Language Translator v2.0 | Multiple Engines & No Rate Limits | Built with Streamlit & FastAPI</p>
        <p>💚 Powered by the open-source community | 🔒 Privacy-focused | 🌐 Community-driven</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
