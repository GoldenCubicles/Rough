from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deep_translator import LibreTranslator
from languages import get_language_code, get_supported_languages
import uvicorn
import os

app = FastAPI(
    title="Multi-Language Translator API",
    description="Free translation API using LibreTranslate (no rate limits like Google)",
    version="2.0.0"
)

# ---------------- Request / Response Models ----------------
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


# ---------------- Helper Function ----------------
def translate_text_libre(text: str, source: str, target: str):
    """
    Translate text using LibreTranslate public API.
    """
    try:
        translator = LibreTranslator(
            source=source,
            target=target,
            base_url="https://libretranslate.de"  # public free instance
        )
        return translator.translate(text)
    except Exception as e:
        raise RuntimeError(f"LibreTranslate error: {str(e)}")


# ---------------- Routes ----------------
@app.get("/")
async def root():
    return {
        "message": "Multi-Language Translator API",
        "version": "2.0.0",
        "description": "Free translation using LibreTranslate backend (no API key required!)",
        "features": [
            "Free & open-source",
            "No Google rate limits",
            "Privacy-focused",
            "Works with 20+ languages",
        ]
    }

@app.get("/languages")
async def get_languages():
    return {
        "languages": get_supported_languages(),
        "count": len(get_supported_languages())
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Map language names to codes
        if request.source_lang == "Auto":
            source_code = "auto"
        else:
            source_code = get_language_code(request.source_lang)

        target_code = get_language_code(request.target_lang)

        if target_code == "auto":
            raise HTTPException(status_code=400, detail="Cannot translate to 'Auto' language")

        # Perform translation
        result = translate_text_libre(request.text, source_code, target_code)

        return TranslationResponse(
            translated_text=result,
            detected_language="Auto-detected" if request.source_lang == "Auto" else request.source_lang,
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
            message=str(e)
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "translator-api"}


# ---------------- Entrypoint ----------------
if __name__ == "__main__":
    print("🚀 Starting Multi-Language Translator API (LibreTranslate backend)")
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
