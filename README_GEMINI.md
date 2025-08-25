# 🌍 Gemini-Powered Multi-Language Translator API

A high-quality translation API powered by Google's Gemini AI model, offering professional-grade translations with a generous free tier.

## ✨ Features

- **🤖 AI-Powered Translation**: Uses Google's Gemini Pro model for superior translation quality
- **🌍 50+ Languages**: Support for major world languages and dialects
- **📦 Batch Translation**: Translate multiple texts efficiently
- **🔍 Auto Language Detection**: Automatically detect source language
- **📏 Long Text Support**: Handles long texts by splitting into chunks
- **⚡ No Rate Limits**: Only limited by Gemini's free tier quotas
- **🔒 Privacy-Focused**: Direct integration with Google's secure API

## 💰 Pricing & Free Tier

**Gemini Free Tier:**
- **15 requests per minute**
- **1,500 requests per day**
- **No credit card required**
- **Perfect for personal projects and testing**

**Paid Tier (if needed):**
- Input: $0.0025 per 1K characters
- Output: $0.0005 per 1K characters

## 🚀 Quick Start

### 1. Get Your API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key

### 2. Setup Environment
```bash
# Windows
setup_gemini.bat

# Linux/Mac
python -m venv 2ndTrans
source 2ndTrans/bin/activate
pip install -r requirements_gemini.txt
```

### 3. Configure API Key
Edit `GeminiAPI.py` and replace:
```python
GEMINI_API_KEY = "your-gemini-api-key-here"
```
with your actual API key.

### 4. Start the API
```bash
python GeminiAPI.py
```

The API will run on `http://127.0.0.1:8002`

### 5. Test the API
```bash
python test_gemini_api.py
```

## 📚 API Endpoints

### Health Check
```http
GET /health
```
Returns API status and free tier information.

### Get Languages
```http
GET /languages
```
Returns list of supported languages.

### Translate Text
```http
POST /translate
Content-Type: application/json

{
  "text": "Hello, how are you?",
  "source_lang": "English",
  "target_lang": "Spanish"
}
```

### Batch Translation
```http
POST /translate_batch
Content-Type: application/json

{
  "texts": ["Hello", "Good morning", "How are you?"],
  "source_lang": "English",
  "target_lang": "French"
}
```

### Test Translation
```http
GET /test-translation
```
Tests the translation functionality with a sample text.

## 🔧 Configuration

### Environment Variables
Create a `.env` file:
```env
GEMINI_API_KEY=your-actual-api-key-here
```

### Model Settings
Adjust in `GeminiAPI.py`:
```python
GEMINI_CONFIG = {
    "temperature": 0.3,        # Lower = more consistent
    "top_p": 0.8,             # Nucleus sampling
    "top_k": 40,              # Top-k sampling
    "max_output_tokens": 2048, # Maximum output length
}
```

## 🌐 Supported Languages

The API supports 50+ languages including:
- **European**: English, Spanish, French, German, Italian, Portuguese, Russian, Dutch, Polish, Swedish, Norwegian, Danish, Finnish, Greek, etc.
- **Asian**: Chinese, Japanese, Korean, Thai, Vietnamese, Indonesian, Malay, Filipino, Hindi, Bengali, Urdu, Persian, etc.
- **Middle Eastern**: Arabic, Hebrew, Turkish, etc.
- **African**: Swahili, Afrikaans, etc.
- **Indigenous**: Welsh, Irish, Scottish Gaelic, Breton, Cornish, Manx, etc.

## 📊 Performance & Features

### Text Processing
- **Short Text**: Direct translation
- **Long Text**: Automatic chunking and sequential translation
- **Batch Processing**: Up to 10 texts per batch request

### Quality Features
- **Context Preservation**: Maintains meaning and tone
- **Style Consistency**: Preserves writing style
- **Cultural Sensitivity**: Context-aware translations

### Error Handling
- **Graceful Degradation**: Continues processing on partial failures
- **Detailed Logging**: Comprehensive error tracking
- **Retry Logic**: Built-in retry mechanisms

## 🔍 Comparison with Other APIs

| Feature | Gemini API | OpenAI API | Google Translate |
|---------|------------|------------|------------------|
| **Free Tier** | 15 req/min, 1,500/day | Limited | 5 req/sec, 200k/day |
| **Quality** | High (AI-powered) | Very High | Good |
| **Rate Limits** | None (only quotas) | None (only quotas) | Strict limits |
| **Setup** | Simple | Simple | Complex |
| **Cost** | Free tier generous | Expensive | Free tier limited |

## 🚀 Deployment

### Local Development
```bash
python GeminiAPI.py
```

### Production Deployment
1. Set environment variables
2. Use production WSGI server (Gunicorn, uvicorn)
3. Configure reverse proxy (Nginx)
4. Set up monitoring and logging

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements_gemini.txt .
RUN pip install -r requirements_gemini.txt
COPY . .
EXPOSE 8002
CMD ["python", "GeminiAPI.py"]
```

## 🧪 Testing

### Run Test Suite
```bash
python test_gemini_api.py
```

### Manual Testing
```bash
# Health check
curl http://127.0.0.1:8002/health

# Test translation
curl -X POST http://127.0.0.1:8002/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","source_lang":"English","target_lang":"Spanish"}'
```

## 🔧 Troubleshooting

### Common Issues

**1. API Key Error**
```
❌ Gemini API key not configured
```
**Solution**: Set your API key in `GeminiAPI.py`

**2. Model Initialization Error**
```
❌ Failed to configure Gemini API
```
**Solution**: Check API key validity and internet connection

**3. Rate Limit Error**
```
❌ Quota exceeded
```
**Solution**: Wait for quota reset or upgrade to paid tier

**4. Long Text Timeout**
```
❌ Request timeout
```
**Solution**: Text is automatically chunked, but very long texts may take time

### Performance Tips

1. **Batch Requests**: Use batch translation for multiple texts
2. **Text Length**: Keep individual texts under 1000 characters for best performance
3. **Language Pairs**: Some language pairs may be faster than others
4. **Caching**: Implement client-side caching for repeated translations

## 📈 Monitoring & Analytics

### Built-in Metrics
- Request count and success rate
- Token usage tracking
- Response time monitoring
- Error rate tracking

### External Monitoring
- Health check endpoints
- Structured logging
- Performance metrics
- Error tracking

## 🔒 Security & Privacy

- **No Data Storage**: Translations are not stored
- **Secure API**: Uses Google's secure infrastructure
- **CORS Support**: Configurable cross-origin requests
- **Input Validation**: Comprehensive input sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

- **Documentation**: Check this README and API docs at `/docs`
- **Issues**: Report bugs and feature requests
- **Community**: Join discussions and share solutions

## 🎯 Roadmap

- [ ] Multi-modal translation (text + images)
- [ ] Translation memory and consistency
- [ ] Advanced language detection
- [ ] Custom translation models
- [ ] WebSocket support for real-time translation
- [ ] Mobile app integration

---

**🌍 Built with ❤️ using Google Gemini AI | FastAPI | Python**

*Get your free API key at [Google AI Studio](https://makersuite.google.com/app/apikey)*

