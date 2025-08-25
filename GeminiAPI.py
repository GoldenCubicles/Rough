import os
import logging
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from collections import deque
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting for Gemini API (free tier limits)
class RateLimiter:
    def __init__(self, max_requests_per_minute=15, max_requests_per_day=1500):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_requests_per_day = max_requests_per_day
        self.requests_per_minute = deque()
        self.requests_per_day = deque()
        self.lock = threading.Lock()
    
    def can_make_request(self) -> bool:
        current_time = time.time()
        
        with self.lock:
            # Clean old requests
            while self.requests_per_minute and current_time - self.requests_per_minute[0] > 60:
                self.requests_per_minute.popleft()
            
            while self.requests_per_day and current_time - self.requests_per_day[0] > 86400:  # 24 hours
                self.requests_per_day.popleft()
            
            # Check limits
            if len(self.requests_per_minute) >= self.max_requests_per_minute:
                return False
            
            if len(self.requests_per_day) >= self.max_requests_per_day:
                return False
            
            # Add current request
            self.requests_per_minute.append(current_time)
            self.requests_per_day.append(current_time)
            return True
    
    def get_wait_time(self) -> int:
        current_time = time.time()
        
        with self.lock:
            if self.requests_per_minute:
                oldest_minute = self.requests_per_minute[0]
                wait_time = 60 - (current_time - oldest_minute)
                return max(0, int(wait_time))
            return 0

# Initialize rate limiter (conservative for free tier)
rate_limiter = RateLimiter(max_requests_per_minute=10, max_requests_per_day=1000)

# Gemini Configuration
GEMINI_API_KEY = "AIzaSyAjQL3OMn2QwsL-c8yNLWu-QhizPZ3dJ7Y"  # Your actual API key
GEMINI_MODEL = "gemini-1.0-pro"  # Using the more generous free tier model
GEMINI_CONFIG = {
    "temperature": 0.3,  # Lower temperature for more consistent translations
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# Initialize Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    logger.info("✅ Gemini API configured successfully")
except Exception as e:
    logger.error(f"❌ Failed to configure Gemini API: {e}")
    model = None

# FastAPI app
app = FastAPI(
    title="Gemini-Powered Multi-Language Translator API",
    description="High-quality translation using Google's Gemini AI model",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

class TranslationResponse(BaseModel):
    success: bool
    translated_text: str
    source_lang: str
    target_lang: str
    detected_language: Optional[str] = None
    model_used: str
    tokens_used: Optional[int] = None
    message: Optional[str] = None

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    source_lang: str
    target_lang: str

class BatchTranslationResponse(BaseModel):
    success: bool
    translations: List[TranslationResponse]
    total_texts: int
    successful_translations: int
    message: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    model: str
    api_provider: str
    free_tier_info: str

class LanguagesResponse(BaseModel):
    languages: List[str]
    total_count: int

# Language mapping for Gemini (using full language names)
def get_language_mapping() -> dict:
    return {
        "English": "English",
        "Spanish": "Spanish",
        "French": "French",
        "German": "German",
        "Italian": "Italian",
        "Portuguese": "Portuguese",
        "Russian": "Russian",
        "Chinese": "Chinese",
        "Japanese": "Japanese",
        "Korean": "Korean",
        "Arabic": "Arabic",
        "Hindi": "Hindi",
        "Bengali": "Bengali",
        "Urdu": "Urdu",
        "Turkish": "Turkish",
        "Dutch": "Dutch",
        "Polish": "Polish",
        "Swedish": "Swedish",
        "Norwegian": "Norwegian",
        "Danish": "Danish",
        "Finnish": "Finnish",
        "Greek": "Greek",
        "Hebrew": "Hebrew",
        "Thai": "Thai",
        "Vietnamese": "Vietnamese",
        "Indonesian": "Indonesian",
        "Malay": "Malay",
        "Filipino": "Filipino",
        "Persian": "Persian",
        "Romanian": "Romanian",
        "Czech": "Czech",
        "Slovak": "Slovak",
        "Hungarian": "Hungarian",
        "Bulgarian": "Bulgarian",
        "Croatian": "Croatian",
        "Serbian": "Serbian",
        "Slovenian": "Slovenian",
        "Estonian": "Estonian",
        "Latvian": "Latvian",
        "Lithuanian": "Lithuanian",
        "Icelandic": "Icelandic",
        "Maltese": "Maltese",
        "Luxembourgish": "Luxembourgish",
        "Catalan": "Catalan",
        "Galician": "Galician",
        "Basque": "Basque",
        "Welsh": "Welsh",
        "Irish": "Irish",
        "Scottish Gaelic": "Scottish Gaelic",
        "Breton": "Breton",
        "Cornish": "Cornish",
        "Manx": "Manx"
    }

def translate_with_gemini(text: str, source_lang: str, target_lang: str) -> tuple[str, str, Optional[int]]:
    """Translate text using Gemini AI."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your-gemini-api-key-here":
        raise Exception("Gemini API key not configured")
    
    if not model:
        raise Exception("Gemini model not initialized")
    
    # Check rate limits first
    if not rate_limiter.can_make_request():
        wait_time = rate_limiter.get_wait_time()
        raise Exception(f"Rate limit exceeded. Please wait {wait_time} seconds before trying again. Free tier limits: 10 req/min, 1000 req/day")
    
    try:
        # Construct the prompt
        if source_lang.lower() == "auto":
            prompt = f"""You are a professional translator. Translate the following text to {target_lang}. 
            Maintain the original meaning, tone, and style. Only return the translated text, nothing else.
            
            Text to translate: {text}"""
        else:
            prompt = f"""You are a professional translator. Translate the following text from {source_lang} to {target_lang}. 
            Maintain the original meaning, tone, and style. Only return the translated text, nothing else.
            
            Text to translate: {text}"""
        
        logger.info(f"Translating with Gemini: {source_lang} -> {target_lang}")
        
        # Generate response
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(**GEMINI_CONFIG)
        )
        
        translated_text = response.text.strip()
        
        # Get token usage if available
        tokens_used = None
        if hasattr(response, 'usage_metadata'):
            tokens_used = response.usage_metadata.total_token_count
        
        logger.info(f"Gemini translation successful. Tokens used: {tokens_used}")
        return translated_text, GEMINI_MODEL, tokens_used
        
    except Exception as e:
        logger.error(f"Gemini translation error: {str(e)}")
        raise Exception(f"Gemini translation failed: {str(e)}")



# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "🌍 Gemini-Powered Multi-Language Translator API",
        "version": "1.0.0",
        "model": GEMINI_MODEL,
        "provider": "Google Gemini",
        "free_tier": "10 requests/minute, 1,000 requests/day (conservative)",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    if not model:
        raise HTTPException(status_code=503, detail="Gemini model not available")
    
    return HealthResponse(
        status="healthy",
        model=GEMINI_MODEL,
        api_provider="Google Gemini",
        free_tier_info="10 req/min, 1,000 req/day (conservative)"
    )

@app.get("/languages", tags=["Languages"])
async def get_languages():
    """Get supported languages."""
    languages = list(get_language_mapping().keys())
    languages.insert(0, "Auto")  # Add Auto as first option
    
    return LanguagesResponse(
        languages=languages,
        total_count=len(languages)
    )

@app.get("/rate-limit-status", tags=["Rate Limiting"])
async def get_rate_limit_status():
    """Get current rate limit status."""
    current_time = time.time()
    
    with rate_limiter.lock:
        # Clean old requests
        while rate_limiter.requests_per_minute and current_time - rate_limiter.requests_per_minute[0] > 60:
            rate_limiter.requests_per_minute.popleft()
        
        while rate_limiter.requests_per_day and current_time - rate_limiter.requests_per_day[0] > 86400:
            rate_limiter.requests_per_day.popleft()
        
        return {
            "requests_this_minute": len(rate_limiter.requests_per_minute),
            "requests_today": len(rate_limiter.requests_per_day),
            "max_requests_per_minute": rate_limiter.max_requests_per_minute,
            "max_requests_per_day": rate_limiter.max_requests_per_day,
            "can_make_request": rate_limiter.can_make_request(),
            "wait_time_seconds": rate_limiter.get_wait_time()
        }

@app.post("/translate", tags=["Translation"])
async def translate_text(request: TranslationRequest):
    """Translate text from one language to another."""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Translate entire text as single request
        translated_text, model_used, tokens_used = translate_with_gemini(
            request.text, request.source_lang, request.target_lang
        )
        
        # Detect language if auto was used
        detected_language = None
        if request.source_lang.lower() == "auto":
            # Simple language detection using Gemini
            try:
                detect_prompt = f"Detect the language of this text and respond with only the language name: {request.text[:200]}"
                detection_response = model.generate_content(detect_prompt)
                detected_language = detection_response.text.strip()
            except:
                detected_language = "Unknown"
        
        return TranslationResponse(
            success=True,
            translated_text=translated_text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            detected_language=detected_language,
            model_used=model_used,
            tokens_used=tokens_used
        )
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return TranslationResponse(
            success=False,
            translated_text="",
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            detected_language=None,
            model_used=GEMINI_MODEL,
            tokens_used=None,
            message=f"Translation failed: {str(e)}"
        )

@app.post("/translate_batch", tags=["Batch Translation"])
async def translate_batch_texts(request: BatchTranslationRequest):
    """Translate multiple texts in batch."""
    try:
        if not request.texts:
            raise HTTPException(status_code=400, detail="Texts list cannot be empty")
        
        if len(request.texts) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 texts allowed per batch")
        
        translations = []
        successful_count = 0
        
        for i, text in enumerate(request.texts):
            try:
                # Translate entire text as single request
                translated_text, model_used, tokens_used = translate_with_gemini(
                    text, request.source_lang, request.target_lang
                )
                
                translations.append(TranslationResponse(
                    success=True,
                    translated_text=translated_text,
                    source_lang=request.source_lang,
                    target_lang=request.target_lang,
                    model_used=model_used,
                    tokens_used=tokens_used
                ))
                successful_count += 1
                
                # Small delay between requests
                if i < len(request.texts) - 1:
                    import time
                    time.sleep(0.3)
                    
            except Exception as e:
                translations.append(TranslationResponse(
                    success=False,
                    translated_text="",
                    source_lang=request.source_lang,
                    target_lang=request.target_lang,
                    detected_language=None,
                    model_used=GEMINI_MODEL,
                    tokens_used=None,
                    message=f"Translation failed: {str(e)}"
                ))
        
        return BatchTranslationResponse(
            success=successful_count > 0,
            translations=translations,
            total_texts=len(request.texts),
            successful_translations=successful_count
        )
        
    except Exception as e:
        logger.error(f"Batch translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch translation failed: {str(e)}")

@app.get("/test-translation", tags=["Testing"])
async def test_translation():
    """Test endpoint for translation functionality."""
    try:
        test_text = "Hello, how are you today?"
        translated_text, model_used, tokens_used = translate_with_gemini(
            test_text, "English", "Spanish"
        )
        
        return {
            "success": True,
            "test_text": test_text,
            "translated_text": translated_text,
            "source_lang": "English",
            "target_lang": "Spanish",
            "model_used": model_used,
            "tokens_used": tokens_used,
            "message": "Test translation successful"
        }
        
    except Exception as e:
        logger.error(f"Test translation error: {str(e)}")
        return {
            "success": False,
            "message": f"Test translation failed: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    
    # Check API key configuration
    if GEMINI_API_KEY == "your-gemini-api-key-here":
        print("⚠️  WARNING: Please set your Gemini API key in the GEMINI_API_KEY variable")
        print("   Get your free API key from: https://makersuite.google.com/app/apikey")
        print("   Free tier: 15 requests/minute, 1,500 requests/day")
    
    print("🚀 Starting Gemini-Powered Multi-Language Translator API")
    print("✅ Using Google Gemini 1.0 Pro - High-quality AI translation!")
    print("🧠 AI-powered • 🌍 50+ languages • 📦 Batch support")
    print("🎯 Professional accuracy • 🔒 Privacy-focused • ⚡ Single request processing")
    print("💰 Free tier: 10 req/min, 1,000 req/day (conservative)")
    print("🛡️ Rate limiting enabled to prevent quota issues")
    
    host = "127.0.0.1"
    port = 8002  # Different port to avoid conflicts
    
    uvicorn.run(
        "GeminiAPI:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
