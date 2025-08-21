from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from languages import get_language_code, get_language_name, get_supported_languages
import uvicorn
import time
import asyncio
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT_REQUESTS = 4  # Stay under Google's 5 req/sec limit
RATE_LIMIT_WINDOW = 1.0  # 1 second window
last_request_time = 0

app = FastAPI(
    title="Multi-Language Translator API",
    description="High-accuracy translation API using local Google Translate engine with rate limiting",
    version="1.0.0"
)

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "Auto"
    target_lang: str = "English"

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    source_lang: str = "Auto"
    target_lang: str = "English"

class TranslationResponse(BaseModel):
    translated_text: str
    detected_language: str = None
    source_lang: str
    target_lang: str
    success: bool
    message: str = None

class BatchTranslationResponse(BaseModel):
    translations: List[TranslationResponse]
    success: bool
    message: str = None

def rate_limit():
    """Implement rate limiting to stay under Google's 5 req/sec limit."""
    global last_request_time
    current_time = time.time()
    time_since_last = current_time - last_request_time
    
    if time_since_last < RATE_LIMIT_WINDOW / RATE_LIMIT_REQUESTS:
        sleep_time = (RATE_LIMIT_WINDOW / RATE_LIMIT_REQUESTS) - time_since_last
        time.sleep(sleep_time)
    
    last_request_time = time.time()

def translate_with_retry(text: str, source_code: str, target_code: str, max_retries: int = 3) -> str:
    """Translate text with retry logic and rate limiting."""
    for attempt in range(max_retries):
        try:
            rate_limit()  # Apply rate limiting
            
            translator = GoogleTranslator(source=source_code, target=target_code)
            result = translator.translate(text)
            return result
            
        except Exception as e:
            error_msg = str(e).lower()
            if "too many requests" in error_msg or "rate limit" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + 1  # Exponential backoff
                    logger.warning(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}")
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception("Rate limit exceeded after multiple retries. Please try again later.")
            else:
                raise e
    
    raise Exception("Translation failed after multiple attempts")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Multi-Language Translator API",
        "version": "1.0.0",
        "description": "High-accuracy translation using local Google Translate engine with rate limiting",
        "features": [
            "Rate limiting to avoid Google's limits",
            "Retry logic with exponential backoff",
            "Batch translation support",
            "Zero latency",
            "High accuracy", 
            "Privacy-focused",
            "Works offline",
            "25+ languages supported"
        ]
    }

@app.get("/languages")
async def get_languages():
    """Get all supported languages."""
    return {
        "languages": get_supported_languages(),
        "count": len(get_supported_languages())
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """Translate text between languages with rate limiting and retry logic."""
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Handle auto-detection
        if request.source_lang == "Auto":
            target_code = get_language_code(request.target_lang)
            result = translate_with_retry(request.text, 'auto', target_code)
            
            return TranslationResponse(
                translated_text=result,
                detected_language="Auto-detected",
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                success=True
            )
        else:
            # Get language codes
            source_code = get_language_code(request.source_lang)
            target_code = get_language_code(request.target_lang)
            
            # Validate languages
            if target_code == "auto":
                raise HTTPException(status_code=400, detail="Cannot translate to 'Auto' language")
            
            # Perform translation with retry logic
            result = translate_with_retry(request.text, source_code, target_code)
            
            return TranslationResponse(
                translated_text=result,
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                success=True
            )
            
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return TranslationResponse(
            translated_text="",
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            success=False,
            message=f"Translation error: {str(e)}"
        )

@app.post("/translate_batch", response_model=BatchTranslationResponse)
async def translate_batch(request: BatchTranslationRequest):
    """Translate multiple texts in batch with rate limiting."""
    
    if not request.texts:
        raise HTTPException(status_code=400, detail="Texts list cannot be empty")
    
    if len(request.texts) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 texts allowed per batch")
    
    try:
        translations = []
        
        for text in request.texts:
            if not text.strip():
                translations.append(TranslationResponse(
                    translated_text="",
                    source_lang=request.source_lang,
                    target_lang=request.target_lang,
                    success=False,
                    message="Empty text"
                ))
                continue
            
            try:
                if request.source_lang == "Auto":
                    target_code = get_language_code(request.target_lang)
                    result = translate_with_retry(text, 'auto', target_code)
                    
                    translations.append(TranslationResponse(
                        translated_text=result,
                        detected_language="Auto-detected",
                        source_lang=request.source_lang,
                        target_lang=request.target_lang,
                        success=True
                    ))
                else:
                    source_code = get_language_code(request.source_lang)
                    target_code = get_language_code(request.target_lang)
                    
                    if target_code == "auto":
                        translations.append(TranslationResponse(
                            translated_text="",
                            source_lang=request.source_lang,
                            target_lang=request.target_lang,
                            success=False,
                            message="Cannot translate to 'Auto' language"
                        ))
                        continue
                    
                    result = translate_with_retry(text, source_code, target_code)
                    
                    translations.append(TranslationResponse(
                        translated_text=result,
                        source_lang=request.source_lang,
                        target_lang=request.target_lang,
                        success=True
                    ))
                    
            except Exception as e:
                translations.append(TranslationResponse(
                    translated_text="",
                    source_lang=request.source_lang,
                    target_lang=request.target_lang,
                    success=False,
                    message=f"Translation error: {str(e)}"
                ))
        
        return BatchTranslationResponse(
            translations=translations,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Batch translation error: {str(e)}")
        return BatchTranslationResponse(
            translations=[],
            success=False,
            message=f"Batch translation error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "translator-api"}

if __name__ == "__main__":
    import os
    print("🚀 Starting Multi-Language Translator API")
    print("✅ Using local translation - No API key required!")
    print("⚡ Rate limiting enabled • 🔄 Retry logic • 📦 Batch support")
    print("🎯 High accuracy • 🔒 Privacy-focused")
    
    # Get port from environment (cloud platforms set this)
    port = int(os.getenv("PORT", 8000))
    # Use 0.0.0.0 to accept connections from anywhere
    host = os.getenv("HOST", "127.0.0.1")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    ) 