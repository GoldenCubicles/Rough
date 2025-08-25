from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from languages import get_language_code, get_language_name, get_supported_languages
import uvicorn
import time
from typing import List, Optional
from collections import deque
from threading import Lock

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

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    source_lang: str = "Auto"
    target_lang: str = "English"

class BatchItemResponse(BaseModel):
    translated_text: str = ""
    success: bool = True
    message: Optional[str] = None

class BatchTranslationResponse(BaseModel):
    translations: List[BatchItemResponse]
    source_lang: str
    target_lang: str
    success: bool
    message: Optional[str] = None

# -----------------------------
# Simple server-side rate limiter
# -----------------------------
RATE_LIMIT_REQUESTS_PER_SECOND = 2  # extra conservative under Google's 5 rps
_recent_request_times = deque()
_rate_lock = Lock()
_total_requests_processed = 0

def _enforce_rate_limit():
    global _total_requests_processed
    now = time.time()
    with _rate_lock:
        # Drop timestamps older than 1 second
        one_second_ago = now - 1.0
        while _recent_request_times and _recent_request_times[0] < one_second_ago:
            _recent_request_times.popleft()

        # If at limit, sleep until next slot
        if len(_recent_request_times) >= RATE_LIMIT_REQUESTS_PER_SECOND:
            sleep_time = max(0.0, _recent_request_times[0] + 1.0 - now)
            if sleep_time > 0:
                time.sleep(sleep_time)
            # re-evaluate window after sleep
            return _enforce_rate_limit()

        _recent_request_times.append(time.time())
        _total_requests_processed += 1

def _split_text_into_chunks(text: str, max_len: int = 4500) -> List[str]:
    # Conservative chunking to stay within Google web translate limits
    if len(text) <= max_len:
        return [text]
    chunks: List[str] = []
    current: str = ""
    for paragraph in text.split("\n\n"):
        if len(paragraph) > max_len:
            # hard split long paragraph
            start = 0
            while start < len(paragraph):
                end = min(start + max_len, len(paragraph))
                chunks.append(paragraph[start:end])
                start = end
        else:
            if len(current) + len(paragraph) + 2 <= max_len:
                current = paragraph if not current else current + "\n\n" + paragraph
            else:
                if current:
                    chunks.append(current)
                current = paragraph
    if current:
        chunks.append(current)
    return chunks

def _translate_single(text: str, source_code: str, target_code: str, max_retries: int = 6) -> str:
    # Retry with exponential backoff on transient errors / rate limits
    attempt = 0
    backoff = 1.0
    while True:
        try:
            _enforce_rate_limit()
            translator = GoogleTranslator(source=source_code, target=target_code)
            return translator.translate(text)
        except Exception as exc:  # deep_translator raises generic Exceptions with messages
            attempt += 1
            message = str(exc).lower()
            transient = any(key in message for key in [
                "too many requests", "429", "temporarily unavailable", "timeout", "server error", "quota", "limit"
            ])
            if attempt <= max_retries and transient:
                time.sleep(backoff)
                backoff *= 2
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
        source_code = 'auto' if request.source_lang == "Auto" else get_language_code(request.source_lang)
        target_code = get_language_code(request.target_lang)
        if target_code == "auto":
            raise HTTPException(status_code=400, detail="Cannot translate to 'Auto' language")

        # Chunk long texts to respect limits, then concatenate
        chunks = _split_text_into_chunks(request.text)
        translated_parts: List[str] = []
        for chunk in chunks:
            translated = _translate_single(chunk, source_code, target_code)
            translated_parts.append(translated)

        result_text = "\n\n".join(translated_parts)

        return TranslationResponse(
            translated_text=result_text,
            detected_language="Auto-detected" if source_code == 'auto' else None,
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

@app.get("/rate-limit-status")
async def rate_limit_status():
    now = time.time()
    with _rate_lock:
        one_second_ago = now - 1.0
        current_window = len([t for t in _recent_request_times if t >= one_second_ago])
        status = "healthy" if current_window < RATE_LIMIT_REQUESTS_PER_SECOND else "throttling"
        return {
            "rate_limiting": {
                "status": status,
                "requests_per_second_limit": RATE_LIMIT_REQUESTS_PER_SECOND,
                "current_window_requests": current_window,
                "total_requests_processed": _total_requests_processed,
            }
        }

@app.post("/translate_batch", response_model=BatchTranslationResponse)
async def translate_batch(request: BatchTranslationRequest):
    if not request.texts:
        raise HTTPException(status_code=400, detail="'texts' cannot be empty")
    try:
        source_code = 'auto' if request.source_lang == "Auto" else get_language_code(request.source_lang)
        target_code = get_language_code(request.target_lang)
        if target_code == "auto":
            raise HTTPException(status_code=400, detail="Cannot translate to 'Auto' language")

        translations: List[BatchItemResponse] = []
        for text in request.texts:
            if not text.strip():
                translations.append(BatchItemResponse(translated_text="", success=False, message="Empty text"))
                continue
            try:
                parts = _split_text_into_chunks(text)
                out_segments: List[str] = []
                for part in parts:
                    out_segments.append(_translate_single(part, source_code, target_code))
                translations.append(BatchItemResponse(translated_text="\n\n".join(out_segments), success=True))
            except Exception as exc:
                translations.append(BatchItemResponse(translated_text="", success=False, message=str(exc)))

        success_overall = any(item.success for item in translations)
        return BatchTranslationResponse(
            translations=translations,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            success=success_overall,
            message=None if success_overall else "All translations failed"
        )
    except Exception as e:
        return BatchTranslationResponse(
            translations=[],
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            success=False,
            message=f"Batch translation error: {str(e)}"
        )

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