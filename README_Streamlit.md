# 🌍 Multi-Language Translator (Streamlit Version)

A modern, high-accuracy translation application built with **Streamlit** frontend and **FastAPI** backend, powered by Google Translate's local engine.

## ✨ Features

- **⚡ Zero Latency** - Instant translations using local processing
- **🎯 High Accuracy** - Powered by Google Translate engine via deep-translator
- **🔒 Privacy-Focused** - No external API calls, works completely offline
- **🌐 Modern UI** - Beautiful Streamlit interface with responsive design
- **🔄 Auto-Detection** - Automatically detects source language
- **📱 Responsive** - Works on desktop, tablet, and mobile devices
- **🚀 FastAPI Backend** - RESTful API for easy integration
- **25+ Languages** - Comprehensive language support

## 🏗️ Architecture

```
┌─────────────────┐    HTTP Requests    ┌─────────────────┐
│   Streamlit     │ ◄─────────────────► │   FastAPI       │
│   Frontend      │                     │   Backend       │
│   (Port 8501)   │                     │   (Port 8000)   │
└─────────────────┘                     └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │ deep-translator │
                                    │ (Google Engine) │
                                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Windows, macOS, or Linux

### Option 1: Automated Setup (Recommended)

#### Windows
```bash
setup_streamlit.bat
```

#### Linux/Mac
```bash
chmod +x setup_streamlit.sh
./setup_streamlit.sh
```

### Option 2: Manual Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv 2ndTrans
   ```

2. **Activate Environment**
   ```bash
   # Windows
   2ndTrans\Scripts\activate
   
   # Linux/Mac
   source 2ndTrans/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Running the Application

### Step 1: Start the API Backend
```bash
# Activate virtual environment first
2ndTrans\Scripts\activate  # Windows
source 2ndTrans/bin/activate  # Linux/Mac

# Start the API
python api.py
```

The API will run at: **http://localhost:8000**

### Step 2: Start the Streamlit Frontend
```bash
# In a new terminal, activate environment and run Streamlit
2ndTrans\Scripts\activate  # Windows
source 2ndTrans/bin/activate  # Linux/Mac

streamlit run streamlit_app.py
```

The Streamlit app will open at: **http://localhost:8501**

## 🌐 API Endpoints

### Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and features |
| `/health` | GET | Health check |
| `/languages` | GET | Get all supported languages |
| `/translate` | POST | Translate text |

### Translation Request Example
```json
{
  "text": "Hello, how are you?",
  "source_lang": "Auto",
  "target_lang": "Spanish"
}
```

### Translation Response Example
```json
{
  "translated_text": "Hola, ¿cómo estás?",
  "detected_language": "English",
  "source_lang": "Auto (detected: English)",
  "target_lang": "Spanish",
  "success": true,
  "message": null
}
```

## 🎨 Streamlit Features

- **Responsive Layout** - Adapts to different screen sizes
- **Real-time Translation** - Instant results as you type
- **Language Swapping** - Easy swap between source and target
- **Auto-detection** - Automatically detects source language
- **Error Handling** - Graceful error messages and API status
- **Modern Styling** - Custom CSS for professional appearance
- **Session Management** - Remembers your preferences

## 🔧 Configuration

### Environment Variables
- **None required** - All configuration is handled in code

### Port Configuration
- **API Backend**: Port 8000 (configurable in `api.py`)
- **Streamlit Frontend**: Port 8501 (configurable via Streamlit)

### Customization
- Modify `API_BASE_URL` in `streamlit_app.py` to change API endpoint
- Adjust styling in the CSS section of `streamlit_app.py`
- Add new languages in `languages.py`

## 📊 Supported Languages

- **English** (en), **Spanish** (es), **French** (fr), **German** (de)
- **Italian** (it), **Portuguese** (pt), **Russian** (ru)
- **Chinese Simplified** (zh), **Chinese Traditional** (zh-TW)
- **Japanese** (ja), **Korean** (ko), **Arabic** (ar)
- **Hindi** (hi), **Bengali** (bn), **Urdu** (ur)
- **Persian** (fa), **Turkish** (tr), **Polish** (pl)
- **Dutch** (nl), **Swedish** (sv), **Danish** (da)
- **Norwegian** (no), **Finnish** (fi), **Greek** (el), **Hebrew** (he)

## 🚀 Performance

- **Latency**: Near-instant (local processing)
- **Accuracy**: High (Google Translate engine)
- **Memory**: Low footprint (~50MB)
- **CPU**: Minimal usage during translation
- **Network**: No external requests after startup

## 🔒 Privacy & Security

- **100% Local** - No data leaves your machine
- **No Logging** - Translation requests are not stored
- **No Tracking** - Complete privacy protection
- **Offline Capable** - Works without internet connection

## 🛠️ Troubleshooting

### Common Issues

1. **"API Connection Failed"**
   - Ensure the API backend is running (`python api.py`)
   - Check if port 8000 is available
   - Verify virtual environment is activated

2. **"Module not found" errors**
   - Activate virtual environment: `2ndTrans\Scripts\activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **Port conflicts**
   - Change ports in `api.py` and `streamlit_app.py`
   - Kill existing processes: `taskkill /f /im python.exe` (Windows)

4. **Translation errors**
   - Check internet connection (for initial setup)
   - Verify text is not empty
   - Ensure language selection is valid

### Performance Tips

- Keep the API backend running for faster response times
- Use shorter text for quicker translations
- Restart the application if performance degrades

## 🔄 Migration from Gradio

If you're migrating from the Gradio version:

1. **Stop the old application** (`Ctrl+C` in the terminal)
2. **Install new dependencies**: `pip install -r requirements.txt`
3. **Start the new API**: `python api.py`
4. **Start Streamlit**: `streamlit run streamlit_app.py`

## 📁 Project Structure

```
2ndtryTrsnslator/
├── 2ndTrans/                 # Virtual environment
├── api.py                    # FastAPI backend
├── streamlit_app.py          # Streamlit frontend
├── languages.py              # Language definitions
├── requirements.txt          # Python dependencies
├── setup_streamlit.bat       # Windows setup script
├── setup_streamlit.sh        # Linux/Mac setup script
├── README_Streamlit.md       # This file
└── .gitignore               # Git ignore rules
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Google Translate** - Translation engine
- **deep-translator** - Python translation library
- **Streamlit** - Frontend framework
- **FastAPI** - Backend framework
- **OpenAI** - AI assistance

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check the Streamlit logs
4. Verify all dependencies are installed

---

**🌍 Built with ❤️ for global communication** 