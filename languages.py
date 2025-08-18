# Language mapping for the translator application
# Maps human-readable language names to ISO language codes

LANGUAGES = {
    "Auto": "auto",
    "English": "en",
    "Spanish": "es", 
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese (Simplified)": "zh",
    "Chinese (Traditional)": "zh-TW",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Hindi": "hi",
    "Bengali": "bn",
    "Urdu": "ur",
    "Persian": "fa",
    "Turkish": "tr",
    "Polish": "pl",
    "Dutch": "nl",
    "Swedish": "sv",
    "Danish": "da",
    "Norwegian": "no",
    "Finnish": "fi",
    "Greek": "el",
    "Hebrew": "he"
}

# Reverse mapping for display purposes
LANGUAGE_CODES_TO_NAMES = {v: k for k, v in LANGUAGES.items()}

def get_language_code(language_name):
    """Get language code from language name."""
    return LANGUAGES.get(language_name, "en")

def get_language_name(language_code):
    """Get language name from language code."""
    return LANGUAGE_CODES_TO_NAMES.get(language_code, "English")

def get_supported_languages():
    """Get list of supported language names."""
    return list(LANGUAGES.keys()) 