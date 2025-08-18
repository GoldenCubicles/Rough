from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from languages import get_language_code, get_language_name, get_supported_languages
import uvicorn

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
            # For auto-detection, we'll use Google's auto-detection
            target_code = get_language_code(request.target_lang)
            
            # Use Google Translator with auto-detection
            translator = GoogleTranslator(source='auto', target=target_code)
            result = translator.translate(request.text)
            
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
            
            # Perform translation
            translator = GoogleTranslator(source=source_code, target=target_code)
            result = translator.translate(request.text)
            
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