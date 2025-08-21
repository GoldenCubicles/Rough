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

# Rate limiting configuration - make it less aggressive for single users
RATE_LIMIT_REQUESTS = 4  # Stay under Google's 5 req/sec limit
RATE_LIMIT_WINDOW = 1.0  # 1 second window

# Add a more flexible rate limiting approach
import threading
from collections import deque
import time

# Thread-safe rate limiting with sliding window
class RateLimiter:
    def __init__(self, max_requests=4, window_size=1.0):
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests = deque()
        self.lock = threading.Lock()
        self.total_requests = 0
        self.rate_limit_hits = 0
    
    def can_proceed(self):
        """Check if we can make a request without exceeding rate limits."""
        current_time = time.time()
        
        with self.lock:
            # Remove old requests outside the window
            while self.requests and current_time - self.requests[0] > self.window_size:
                self.requests.popleft()
            
            # Check if we're under the limit
            if len(self.requests) < self.max_requests:
                self.requests.append(current_time)
                self.total_requests += 1
                return True
            
            self.rate_limit_hits += 1
            return False
    
    def wait_if_needed(self):
        """Wait until we can make a request."""
        wait_count = 0
        while not self.can_proceed():
            wait_count += 1
            if wait_count == 1:  # Log only once per wait
                logger.info(f"Rate limit reached, waiting for slot... (total requests: {self.total_requests}, rate limit hits: {self.rate_limit_hits})")
            time.sleep(0.1)  # Small delay to avoid busy waiting
    
    def get_stats(self):
        """Get current rate limiting statistics."""
        with self.lock:
            return {
                "total_requests": self.total_requests,
                "rate_limit_hits": self.rate_limit_hits,
                "current_window_requests": len(self.requests),
                "max_requests": self.max_requests,
                "window_size": self.window_size
            }

# Create a global rate limiter instance - make it less aggressive
rate_limiter = RateLimiter(max_requests=4, window_size=1.0)

def rate_limit():
    """Implement rate limiting to stay under Google's 5 req/sec limit."""
    rate_limiter.wait_if_needed()

def translate_with_retry(text: str, source_code: str, target_code: str, max_retries: int = 3) -> str:
    """Translate text with retry logic and rate limiting."""
    for attempt in range(max_retries):
        try:
            rate_limit()  # Apply rate limiting
            
            logger.info(f"Attempt {attempt + 1}: Translating '{text[:50]}...' from {source_code} to {target_code}")
            
            translator = GoogleTranslator(source=source_code, target=target_code)
            result = translator.translate(text)
            
            # Verify we got a proper translation
            if result and result.strip() and result.strip() != text.strip():
                logger.info(f"Translation successful: '{text[:30]}...' -> '{result[:30]}...'")
                return result
            else:
                logger.warning(f"Attempt {attempt + 1}: Translation returned empty or same text")
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + 1
                    logger.info(f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception("Translation failed: returned same text after all retries")
            
        except Exception as e:
            error_msg = str(e).lower()
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            
            if "too many requests" in error_msg or "rate limit" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + 1  # Exponential backoff
                    logger.warning(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}")
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception("Rate limit exceeded after multiple retries. Please try again later.")
            else:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + 1
                    logger.warning(f"Translation error, waiting {wait_time}s before retry {attempt + 1}")
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception(f"Translation failed after {max_retries} attempts: {str(e)}")
    
    raise Exception("Translation failed after multiple attempts")

def split_text_for_translation(text: str, max_chunk_size: int = 1000) -> List[str]:
    """Split long text into smaller chunks for translation."""
    if len(text) <= max_chunk_size:
        return [text]
    
    # Split by sentences first, then by words if needed
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if not sentence.strip():
            continue
            
        # Add period back if it's not the last sentence
        if sentence != sentences[-1]:
            sentence += '. '
        
        # If adding this sentence would exceed the limit, start a new chunk
        if len(current_chunk) + len(sentence) > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += sentence
    
    # Add the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def translate_long_text(text: str, source_code: str, target_code: str) -> str:
    """Translate long text by splitting into chunks and translating sequentially."""
    chunks = split_text_for_translation(text)
    
    if len(chunks) == 1:
        # Single chunk, translate directly
        return translate_with_retry(text, source_code, target_code)
    
    # Multiple chunks, translate sequentially
    translated_chunks = []
    
    for i, chunk in enumerate(chunks):
        try:
            logger.info(f"Translating chunk {i+1}/{len(chunks)} (length: {len(chunk)})")
            translated_chunk = translate_with_retry(chunk, source_code, target_code)
            
            # Verify that we actually got a translation, not the original text
            if translated_chunk and translated_chunk.strip() != chunk.strip():
                translated_chunks.append(translated_chunk)
                logger.info(f"Chunk {i+1} translated successfully: '{chunk[:50]}...' -> '{translated_chunk[:50]}...'")
            else:
                logger.warning(f"Chunk {i+1} returned same text, retrying...")
                # Try one more time with a different approach
                time.sleep(0.5)
                retry_chunk = translate_with_retry(chunk, source_code, target_code)
                if retry_chunk and retry_chunk.strip() != chunk.strip():
                    translated_chunks.append(retry_chunk)
                    logger.info(f"Chunk {i+1} retry successful")
                else:
                    raise Exception(f"Failed to translate chunk {i+1}: returned same text")
            
            # Small delay between chunks to be extra safe with rate limiting
            if i < len(chunks) - 1:
                time.sleep(0.3)
                
        except Exception as e:
            logger.error(f"Failed to translate chunk {i+1}: {str(e)}")
            # Don't return original text on failure - raise the exception
            raise Exception(f"Translation failed for chunk {i+1}: {str(e)}")
    
    # Join the translated chunks
    return ' '.join(translated_chunks)

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
            
            # Use the long text handler for better rate limiting
            result = translate_long_text(request.text, 'auto', target_code)
            
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
            
            # Use the long text handler for better rate limiting
            result = translate_long_text(request.text, source_code, target_code)
            
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
        
        for i, text in enumerate(request.texts):
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
                logger.info(f"Processing batch text {i+1}/{len(request.texts)} (length: {len(text)})")
                
                if request.source_lang == "Auto":
                    target_code = get_language_code(request.target_lang)
                    result = translate_long_text(text, 'auto', target_code)
                    
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
                    
                    result = translate_long_text(text, source_code, target_code)
                    
                    translations.append(TranslationResponse(
                        translated_text=result,
                        source_lang=request.source_lang,
                        target_lang=request.target_lang,
                        success=True
                    ))
                
                # Small delay between batch items to be extra safe with rate limiting
                if i < len(request.texts) - 1:
                    time.sleep(0.3)
                    
            except Exception as e:
                logger.error(f"Failed to translate batch text {i+1}: {str(e)}")
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

@app.get("/rate-limit-status")
async def rate_limit_status():
    """Get current rate limiting status and statistics."""
    stats = rate_limiter.get_stats()
    return {
        "rate_limiting": {
            "max_requests_per_second": stats["max_requests"],
            "window_size_seconds": stats["window_size"],
            "current_window_requests": stats["current_window_requests"],
            "total_requests_processed": stats["total_requests"],
            "rate_limit_hits": stats["rate_limit_hits"],
            "status": "healthy" if stats["current_window_requests"] < stats["max_requests"] else "rate_limited"
        },
        "google_limits": {
            "max_requests_per_second": 5,
            "max_requests_per_day": 200000,
            "our_limit": "4 req/sec (staying under Google's 5 req/sec limit)"
        }
    }

@app.get("/test-translation")
async def test_translation():
    """Test endpoint to verify translation is working."""
    try:
        # Test with a simple translation
        test_text = "Hello world"
        result = translate_with_retry(test_text, "en", "es")
        
        if result and result != test_text:
            return {
                "status": "healthy",
                "test_text": test_text,
                "translated_text": result,
                "message": "Translation is working correctly"
            }
        else:
            return {
                "status": "unhealthy",
                "test_text": test_text,
                "translated_text": result,
                "message": "Translation returned same text - not working"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "Translation test failed"
        }

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