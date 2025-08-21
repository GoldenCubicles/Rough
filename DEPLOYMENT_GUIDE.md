# 🚀 Deployment Guide for Multi-Language Translator API

This guide explains how to deploy the updated translator API with rate limiting, retry logic, and batch translation capabilities.

## 🎯 What's New in v2.0

- **Rate Limiting**: Automatically stays under Google's 5 req/sec limit
- **Retry Logic**: Exponential backoff for failed requests
- **Batch Translation**: Efficient processing of multiple texts
- **Better Error Handling**: Helpful error messages and suggestions
- **Production Ready**: Optimized for hosted environments

## 🌐 Deployment Options

### 1. Render.com (Recommended for Free Tier)

#### Setup Steps:
1. **Fork/Clone** this repository to your GitHub account
2. **Connect** your GitHub repo to Render
3. **Create New Web Service**
4. **Configure** the service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api.py`
   - **Environment Variables**:
     - `PORT`: `8000`
     - `HOST`: `0.0.0.0`

#### Render Configuration:
```yaml
# render.yaml (optional)
services:
  - type: web
    name: translator-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python api.py
    envVars:
      - key: PORT
        value: 8000
      - key: HOST
        value: 0.0.0.0
```

### 2. Railway.app

#### Setup Steps:
1. **Connect** your GitHub repository
2. **Deploy** automatically
3. **Environment Variables**:
   - `PORT`: Railway sets this automatically
   - `HOST`: `0.0.0.0`

### 3. Heroku

#### Setup Steps:
1. **Install Heroku CLI**
2. **Create app**: `heroku create your-app-name`
3. **Deploy**: `git push heroku main`
4. **Environment Variables**:
   ```bash
   heroku config:set HOST=0.0.0.0
   ```

### 4. Docker Deployment

#### Build and Run:
```bash
# Build image
docker build -t translator-api .

# Run container
docker run -d -p 8000:8000 --name translator-api translator-api

# Or with Docker Compose
docker-compose up -d
```

#### Docker Compose Example:
```yaml
# docker-compose.yml
version: '3.8'
services:
  translator-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
      - PORT=8000
    restart: unless-stopped
```

## ⚙️ Environment Configuration

### Required Environment Variables:
```bash
# Server Configuration
HOST=0.0.0.0          # Accept connections from anywhere
PORT=8000              # Server port (platforms may override)

# Optional Debug Settings
LOG_LEVEL=INFO         # DEBUG, INFO, WARNING, ERROR
```

### Platform-Specific Notes:
- **Render**: Automatically sets `PORT`
- **Railway**: Automatically sets `PORT`
- **Heroku**: Automatically sets `PORT`
- **Docker**: Use `0.0.0.0` for external access

## 🔧 Production Optimizations

### 1. Rate Limiting Tuning
```python
# In api.py - adjust these values based on your needs
RATE_LIMIT_REQUESTS = 4  # Stay under Google's 5 req/sec limit
RATE_LIMIT_WINDOW = 1.0  # 1 second window
```

### 2. Retry Logic Configuration
```python
# In api.py - adjust retry attempts
def translate_with_retry(text: str, source_code: str, target_code: str, max_retries: int = 3):
    # Increase max_retries for more resilient operation
```

### 3. Batch Size Limits
```python
# In api.py - adjust maximum batch size
if len(request.texts) > 10:  # Increase for higher throughput
    raise HTTPException(status_code=400, detail="Maximum 10 texts allowed per batch")
```

## 📊 Monitoring and Health Checks

### Health Endpoint:
```http
GET /health
Response: {"status": "healthy", "service": "translator-api"}
```

### Built-in Logging:
```python
# Logs are automatically generated for:
# - Translation requests
# - Rate limit hits
# - Retry attempts
# - Errors and failures
```

### External Monitoring:
- **Uptime Robot**: Monitor `/health` endpoint
- **StatusCake**: Track response times
- **Custom Scripts**: Use the test script for monitoring

## 🚨 Rate Limiting Strategy

### How It Works:
1. **Request Arrives**: API receives translation request
2. **Rate Check**: Verifies if we're under the 4 req/sec limit
3. **Delay if Needed**: Automatically delays requests to stay under limit
4. **Translation**: Processes the translation
5. **Retry Logic**: If rate limited, retries with exponential backoff

### Benefits:
- **Never Exceeds Limits**: Stays under Google's 5 req/sec limit
- **Automatic Recovery**: Self-healing from rate limit errors
- **User Friendly**: Transparent to end users
- **Efficient**: Optimizes request timing

## 🔍 Troubleshooting Deployment

### Common Issues:

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Environment Variables Not Set**
   ```bash
   # Check current environment
   env | grep PORT
   env | grep HOST
   ```

3. **Dependencies Missing**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt --force-reinstall
   ```

4. **Rate Limiting Too Aggressive**
   ```python
   # Adjust in api.py
   RATE_LIMIT_REQUESTS = 3  # More conservative
   ```

### Debug Mode:
```python
# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Metrics

### Expected Performance:
- **Response Time**: 1-3 seconds (including rate limiting)
- **Throughput**: 4 requests/second (rate limited)
- **Uptime**: 99.9%+ (with proper hosting)
- **Batch Efficiency**: 10 texts per request

### Monitoring Commands:
```bash
# Test API health
curl https://your-api-url/health

# Test single translation
curl -X POST https://your-api-url/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello","source_lang":"Auto","target_lang":"Spanish"}'

# Test batch translation
curl -X POST https://your-api-url/translate_batch \
  -H "Content-Type: application/json" \
  -d '{"texts":["Hello","World"],"source_lang":"Auto","target_lang":"French"}'
```

## 🔐 Security Considerations

### Current Security:
- **No API Keys**: Uses Google Translate directly
- **Rate Limiting**: Prevents abuse
- **Input Validation**: Sanitizes all inputs
- **Error Handling**: No sensitive information leaked

### Additional Security (Optional):
```python
# Add authentication if needed
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/translate")
async def translate_text(
    request: TranslationRequest,
    token: str = Depends(security)
):
    # Verify token here
    pass
```

## 🎉 Success Checklist

After deployment, verify:
- [ ] API responds to `/health` endpoint
- [ ] Single translation works (`/translate`)
- [ ] Batch translation works (`/translate_batch`)
- [ ] Rate limiting is working (4 req/sec max)
- [ ] Error handling provides helpful messages
- [ ] Logs are being generated
- [ ] Frontend can connect to API

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs for error details
3. Test with the provided test script
4. Open an issue in the repository

---

**Happy Deploying! 🚀✨**
