from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from languages import get_language_code, get_supported_languages
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

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Multi-Language Translator API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "translator-api"}

@app.get("/languages")
async def get_languages():
    """Get all supported languages."""
    try:
        languages = get_supported_languages()
        return {
            "languages": languages,
            "count": len(languages)
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    """Translate text between languages."""
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Handle auto-detection
        if request.source_lang == "Auto":
            target_code = get_language_code(request.target_lang)
            translator = GoogleTranslator(source='auto', target=target_code)
            result = translator.translate(request.text)
            
            return {
                "translated_text": result,
                "source_lang": "Auto",
                "target_lang": request.target_lang,
                "success": True
            }
        else:
            source_code = get_language_code(request.source_lang)
            target_code = get_language_code(request.target_lang)
            
            if target_code == "auto":
                raise HTTPException(status_code=400, detail="Cannot translate to 'Auto' language")
            
            translator = GoogleTranslator(source=source_code, target=target_code)
            result = translator.translate(request.text)
            
            return {
                "translated_text": result,
                "source_lang": request.source_lang,
                "target_lang": request.target_lang,
                "success": True
            }
            
    except Exception as e:
        return {
            "translated_text": "",
            "source_lang": request.source_lang,
            "target_lang": request.target_lang,
            "success": False,
            "message": f"Translation error: {str(e)}"
        }

if __name__ == "__main__":
    print("🚀 Starting Simple Multi-Language Translator API")
    print("✅ Using local translation - No API key required!")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    ) 