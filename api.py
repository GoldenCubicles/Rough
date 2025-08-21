from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import time
import logging
import os
import openai
from languages import get_language_code, get_language_name, get_supported_languages

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI Configuration
# TODO: Replace with your actual OpenAI API key
OPENAI_API_KEY = "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"  # Replace this with your real API key

if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-your-actual-api-key-here":
    logger.error("⚠️  Please replace the hardcoded API key with your actual OpenAI API key!")
    logger.error("   Edit OpensourceAPI.py and replace 'sk-your-actual-api-key-here' with your real key")
    raise Exception("OpenAI API key not configured - please edit the file and add your real API key")

# Configure OpenAI client
try:
    # For OpenAI v1.0.0+, we don't need to set the global API key
    # It will be passed when creating the client
    logger.info("OpenAI client will be configured per request")
except Exception as e:
    logger.error(f"Failed to configure OpenAI client: {str(e)}")

app = FastAPI(
    title="OpenAI-Powered Multi-Language Translator API",
    description="High-accuracy translation API using OpenAI's advanced language models",
    version="3.0.0"
)

# OpenAI Translation Configuration
OPENAI_CONFIG = {
    "model": "gpt-3.5-turbo",  # Can be changed to gpt-4 for better quality
    "max_tokens": 4000,
    "temperature": 0.3,  # Lower temperature for more consistent translations
    "enabled": True
}

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
    model_used: str = None
    tokens_used: int = None

class BatchTranslationResponse(BaseModel):
    translations: List[TranslationResponse]
    success: bool
    message: str = None

def get_language_mapping():
    """Get language mapping for OpenAI translation."""
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
        "Persian": "Persian",
        "Turkish": "Turkish",
        "Polish": "Polish",
        "Dutch": "Dutch",
        "Swedish": "Swedish",
        "Danish": "Danish",
        "Norwegian": "Norwegian",
        "Finnish": "Finnish",
        "Greek": "Greek",
        "Hebrew": "Hebrew",
        "Vietnamese": "Vietnamese",
        "Thai": "Thai",
        "Indonesian": "Indonesian",
        "Malay": "Malay",
        "Filipino": "Filipino",
        "Swahili": "Swahili",
        "Zulu": "Zulu",
        "Afrikaans": "Afrikaans",
        "Irish": "Irish",
        "Welsh": "Welsh",
        "Scottish Gaelic": "Scottish Gaelic",
        "Catalan": "Catalan",
        "Basque": "Basque",
        "Galician": "Galician",
        "Romanian": "Romanian",
        "Bulgarian": "Bulgarian",
        "Croatian": "Croatian",
        "Serbian": "Serbian",
        "Slovenian": "Slovenian",
        "Slovak": "Slovak",
        "Czech": "Czech",
        "Hungarian": "Hungarian",
        "Estonian": "Estonian",
        "Latvian": "Latvian",
        "Lithuanian": "Lithuanian",
        "Ukrainian": "Ukrainian",
        "Belarusian": "Belarusian",
        "Macedonian": "Macedonian",
        "Albanian": "Albanian",
        "Bosnian": "Bosnian",
        "Montenegrin": "Montenegrin"
    }

def translate_with_openai(text: str, source_lang: str, target_lang: str) -> tuple[str, str, int]:
    """Translate using OpenAI's advanced language models."""
    if not OPENAI_API_KEY:
        raise Exception("OpenAI API key not configured")
    
    try:
        # Handle auto-detection
        if source_lang.lower() == "auto":
            prompt = f"""Translate the following text to {target_lang}. 
            Maintain the original meaning, tone, and style. 
            Only return the translated text, nothing else.
            
            Text to translate: {text}"""
        else:
            prompt = f"""Translate the following text from {source_lang} to {target_lang}. 
            Maintain the original meaning, tone, and style. 
            Only return the translated text, nothing else.
            
            Text to translate: {text}"""
        
        logger.info(f"Translating with OpenAI: {source_lang} -> {target_lang}")
        
        # Use the new OpenAI API format
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_CONFIG["model"],
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate accurately and naturally."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=OPENAI_CONFIG["max_tokens"],
            temperature=OPENAI_CONFIG["temperature"]
        )
        
        translated_text = response.choices[0].message.content.strip()
        tokens_used = response.usage.total_tokens
        
        logger.info(f"OpenAI translation successful. Tokens used: {tokens_used}")
        return translated_text, OPENAI_CONFIG["model"], tokens_used
        
    except Exception as e:
        logger.error(f"OpenAI translation error: {str(e)}")
        raise Exception(f"OpenAI translation failed: {str(e)}")

def split_text_for_translation(text: str, max_chunk_size: int = 800) -> List[str]:
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

def translate_long_text(text: str, source_lang: str, target_lang: str) -> tuple[str, str, int]:
    """Translate long text by splitting into chunks and translating sequentially."""
    chunks = split_text_for_translation(text)
    
    if len(chunks) == 1:
        # Single chunk, translate directly
        return translate_with_openai(text, source_lang, target_lang)
    
    # Multiple chunks, translate sequentially
    translated_chunks = []
    model_used = None
    total_tokens = 0
    
    for i, chunk in enumerate(chunks):
        try:
            logger.info(f"Translating chunk {i+1}/{len(chunks)} (length: {len(chunk)})")
            translated_chunk, chunk_model, tokens_used = translate_with_openai(chunk, source_lang, target_lang)
            translated_chunks.append(translated_chunk)
            
            # Track which model was used and total tokens
            if model_used is None:
                model_used = chunk_model
            total_tokens += tokens_used
            
            # Small delay between chunks to be respectful to OpenAI API
            if i < len(chunks) - 1:
                time.sleep(0.2)
                
        except Exception as e:
            logger.error(f"Failed to translate chunk {i+1}: {str(e)}")
            # If a chunk fails, raise the exception
            raise Exception(f"Translation failed for chunk {i+1}: {str(e)}")
    
    # Join the translated chunks
    return ' '.join(translated_chunks), model_used, total_tokens

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "OpenAI-Powered Multi-Language Translator API",
        "version": "3.0.0",
        "description": "High-accuracy translation using OpenAI's advanced language models",
        "features": [
            "OpenAI GPT-3.5-turbo powered translation",
            "No rate limiting issues",
            "Superior translation quality",
            "Long text support with intelligent chunking",
            "Batch translation support",
            "High accuracy and context understanding",
            "Privacy-focused",
            "50+ languages supported",
            "Professional-grade translations"
        ],
        "openai_config": {
            "model": OPENAI_CONFIG["model"],
            "max_tokens": OPENAI_CONFIG["max_tokens"],
            "temperature": OPENAI_CONFIG["temperature"]
        },
        "note": "Requires OPENAI_API_KEY environment variable"
    }

@app.get("/languages")
async def get_languages():
    """Get all supported languages."""
    return {
        "languages": get_supported_languages(),
        "count": len(get_supported_languages())
    }

@app.get("/services")
async def get_services():
    """Get OpenAI translation service status and configuration."""
    return {
        "service": "OpenAI Translation",
        "status": "enabled" if OPENAI_CONFIG["enabled"] and OPENAI_API_KEY else "disabled",
        "model": OPENAI_CONFIG["model"],
        "configuration": {
            "max_tokens": OPENAI_CONFIG["max_tokens"],
            "temperature": OPENAI_CONFIG["temperature"],
            "api_key_configured": bool(OPENAI_API_KEY)
        },
        "capabilities": [
            "High-quality translation",
            "Context-aware translations",
            "Multiple language support",
            "Long text handling",
            "Professional-grade accuracy"
        ]
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """Translate text between languages using OpenAI."""
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        # Handle auto-detection
        if request.source_lang == "Auto":
            # Use the long text handler
            result, model_used, tokens_used = translate_long_text(request.text, 'auto', request.target_lang)
            
            return TranslationResponse(
                translated_text=result,
                detected_language="Auto-detected",
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                success=True,
                model_used=model_used,
                tokens_used=tokens_used
            )
        else:
            # Validate languages
            if request.target_lang == "Auto":
                raise HTTPException(status_code=400, detail="Cannot translate to 'Auto' language")
            
            # Use the long text handler
            result, model_used, tokens_used = translate_long_text(request.text, request.source_lang, request.target_lang)
            
            return TranslationResponse(
                translated_text=result,
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                success=True,
                model_used=model_used,
                tokens_used=tokens_used
            )
            
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return TranslationResponse(
            translated_text="",
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            success=False,
            message=f"Translation error: {str(e)}",
            model_used="none",
            tokens_used=0
        )

@app.post("/translate_batch", response_model=BatchTranslationResponse)
async def translate_batch(request: BatchTranslationRequest):
    """Translate multiple texts in batch using OpenAI."""
    
    if not request.texts:
        raise HTTPException(status_code=400, detail="Texts list cannot be empty")
    
    if len(request.texts) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 texts allowed per batch")
    
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        translations = []
        
        for i, text in enumerate(request.texts):
            if not text.strip():
                translations.append(TranslationResponse(
                    translated_text="",
                    source_lang=request.source_lang,
                    target_lang=request.target_lang,
                    success=False,
                    message="Empty text",
                    model_used="none",
                    tokens_used=0
                ))
                continue
            
            try:
                logger.info(f"Processing batch text {i+1}/{len(request.texts)} (length: {len(text)})")
                
                if request.source_lang == "Auto":
                    result, model_used, tokens_used = translate_long_text(text, 'auto', request.target_lang)
                    
                    translations.append(TranslationResponse(
                        translated_text=result,
                        detected_language="Auto-detected",
                        source_lang=request.source_lang,
                        target_lang=request.target_lang,
                        success=True,
                        model_used=model_used,
                        tokens_used=tokens_used
                    ))
                else:
                    if request.target_lang == "Auto":
                        translations.append(TranslationResponse(
                            translated_text="",
                            source_lang=request.source_lang,
                            target_lang=request.target_lang,
                            success=False,
                            message="Cannot translate to 'Auto' language",
                            model_used="none",
                            tokens_used=0
                        ))
                        continue
                    
                    result, model_used, tokens_used = translate_long_text(text, request.source_lang, request.target_lang)
                    
                    translations.append(TranslationResponse(
                        translated_text=result,
                        source_lang=request.source_lang,
                        target_lang=request.target_lang,
                        success=True,
                        model_used=model_used,
                        tokens_used=tokens_used
                    ))
                
                # Small delay between batch items to be respectful to OpenAI API
                if i < len(request.texts) - 1:
                    time.sleep(0.3)
                    
            except Exception as e:
                logger.error(f"Failed to translate batch text {i+1}: {str(e)}")
                translations.append(TranslationResponse(
                    translated_text="",
                    source_lang=request.source_lang,
                    target_lang=request.target_lang,
                    success=False,
                    message=f"Translation error: {str(e)}",
                    model_used="none",
                    tokens_used=0
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
    return {"status": "healthy", "service": "opensource-translator-api"}

@app.get("/test-translation")
async def test_translation():
    """Test endpoint to verify OpenAI translation is working."""
    try:
        if not OPENAI_API_KEY:
            return {
                "status": "unhealthy",
                "error": "OpenAI API key not configured",
                "message": "Please set OPENAI_API_KEY environment variable"
            }
        
        # Test with a simple translation
        result, model_used, tokens_used = translate_with_openai("Hello world", "English", "Spanish")
        
        if result:
            return {
                "status": "healthy",
                "test_translation": result,
                "model_used": model_used,
                "tokens_used": tokens_used,
                "message": "OpenAI translation is working correctly"
            }
        else:
            return {
                "status": "unhealthy",
                "message": "OpenAI translation returned no result"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "OpenAI translation is not working"
        }

if __name__ == "__main__":
    import os
    print("🚀 Starting OpenAI-Powered Multi-Language Translator API")
    print("✅ Using OpenAI GPT-3.5-turbo - Superior translation quality!")
    print("🧠 AI-powered • 🌍 50+ languages • 📦 Batch support")
    print("🎯 Professional accuracy • 🔒 Privacy-focused • ⚡ No rate limits")
    
    if OPENAI_API_KEY == "sk-your-actual-api-key-here":
        print("⚠️  WARNING: Please replace the hardcoded API key!")
        print("   Edit OpensourceAPI.py and replace 'sk-your-actual-api-key-here' with your real key")
        print("   Your API key should look like: sk-1234567890abcdef...")
    
    # Get port from environment (cloud platforms set this)
    port = int(os.getenv("PORT", 8001))  # Use different port to avoid conflicts
    # Use 0.0.0.0 to accept connections from anywhere
    host = os.getenv("HOST", "127.0.0.1")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
