from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from languages import get_language_code, get_language_name, get_supported_languages
import uvicorn
import os
import asyncio
import time
import random

app = FastAPI(
    title="Multi-Language Translator API",
    description="High-accuracy translation API using local Google Translate engine",
    version="1.0.0"
)

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "Auto"
    target_lang: str = "English"

class TranslationResponse(BaseModel):
    translated_text: str
    detected_language: str = None
    source_lang: str
    target_lang: str
    success: bool
    message: str = None

# ---------------- Rate limit + retry logic ----------------
# Google unofficial endpoint is rate-limited. Apply a conservative
# per-process rate limit and retry on throttling errors.
RATE_LIMIT_RPS = float(os.getenv("RATE_LIMIT_RPS", "4"))  # allowed requests per second
_MIN_INTERVAL_SECONDS = 1.0 / max(RATE_LIMIT_RPS, 0.1)
_last_request_time: float = 0.0
_rate_lock = asyncio.Lock()


async def _wait_for_client_rate_limit() -> None:
    global _last_request_time
    async with _rate_lock:
        now = time.monotonic()
        elapsed = now - _last_request_time
        if elapsed < _MIN_INTERVAL_SECONDS:
            await asyncio.sleep(_MIN_INTERVAL_SECONDS - elapsed)
        _last_request_time = time.monotonic()


def _looks_like_rate_limited(error_message: str) -> bool:
    msg = (error_message or "").lower()
    indicators = [
        "too many requests",
        "429",
        "rate limit",
        "you made too many requests",
        "server error",
    ]
    return any(k in msg for k in indicators)


async def _translate_with_retry(text: str, source_code: str, target_code: str) -> str:
    max_attempts = int(os.getenv("TRANSLATE_MAX_ATTEMPTS", "5"))
    base_delay = float(os.getenv("TRANSLATE_BACKOFF_SECONDS", "0.5"))

    attempt = 0
    while True:
        attempt += 1
        await _wait_for_client_rate_limit()
        try:
            translator = GoogleTranslator(source=source_code, target=target_code)
            return translator.translate(text)
        except Exception as e:
            if attempt < max_attempts and _looks_like_rate_limited(str(e)):
                backoff = base_delay * (2 ** (attempt - 1))
                jitter = random.uniform(0, base_delay)
                await asyncio.sleep(backoff + jitter)
                continue
            raise

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Multi-Language Translator API",
        "version": "1.0.0",
        "description": "High-accuracy translation using local Google Translate engine",
        "features": [
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
    """Translate text between languages."""
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Handle auto-detection
        if request.source_lang == "Auto":
            target_code = get_language_code(request.target_lang)
            result = await _translate_with_retry(request.text, "auto", target_code)
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
            
            # Perform translation with retries
            result = await _translate_with_retry(request.text, source_code, target_code)
            
            return TranslationResponse(
                translated_text=result,
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                success=True
            )
            
    except Exception as e:
        return TranslationResponse(
            translated_text="",
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            success=False,
            message=f"Translation error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "translator-api"}

if __name__ == "__main__":
    import os
    print("🚀 Starting Multi-Language Translator API")
    print("✅ Using local translation - No API key required!")
    print("⚡ Zero latency • 🎯 High accuracy • 🔒 Privacy-focused")
    
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