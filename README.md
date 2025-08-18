# 🌍 Multi-Language Translator (Free)

A high-accuracy Python-based translator application that supports 25+ languages using **LibreTranslate API** - completely free and open-source! Built with Gradio for a clean, modern web interface.

## ✨ Features

- **25+ Supported Languages**: Including English, Spanish, French, German, Italian, Portuguese, Russian, Chinese (Simplified & Traditional), Japanese, Korean, Arabic, Hindi, Bengali, Urdu, Persian, Turkish, Polish, Dutch, Swedish, Danish, Norwegian, Finnish, Greek, and Hebrew
- **Auto-Language Detection**: Automatically detect the source language
- **High Translation Accuracy**: Powered by LibreTranslate API
- **Completely Free**: No API keys or costs required
- **Clean Gradio Interface**: Modern, responsive web UI
- **Easy Language Swapping**: Quick swap between source and target languages
- **Real-time Translation**: Auto-translate as you type (with debouncing)
- **Error Handling**: Comprehensive error handling for API failures

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection (for API access)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd 2ndtryTrsnslator
   ```

2. **Create and activate virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv 2ndTrans
   2ndTrans\Scripts\activate
   
   # Linux/Mac
   python3 -m venv 2ndTrans
   source 2ndTrans/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test your setup**
   ```bash
   python test_setup.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to `http://localhost:7860`

## 🔑 No API Key Required!

This application uses **LibreTranslate API** which is:
- ✅ **Completely free** - no costs or limits
- ✅ **Open-source** - transparent and community-driven
- ✅ **No registration** - just start using immediately
- ✅ **High quality** - excellent translation accuracy

## 📁 Project Structure

```
2ndtryTrsnslator/
├── app.py              # Main application with Gradio UI
├── languages.py        # Language mapping and utilities
├── requirements.txt    # Python dependencies
├── test_setup.py      # Setup verification script
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🎯 Usage

1. **Select Source Language**: Choose the language of your input text, or select "Auto" for automatic detection
2. **Select Target Language**: Choose the language you want to translate to
3. **Enter Text**: Type or paste the text you want to translate
4. **Get Translation**: The translated text appears automatically, or click the "Translate" button
5. **Additional Features**:
   - Use "🔄 Swap Languages" to quickly switch source and target
   - Use "🗑️ Clear" to clear both input and output
   - Translation happens automatically as you type

## 🌐 Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| Auto | auto | English | en |
| Spanish | es | French | fr |
| German | de | Italian | it |
| Portuguese | pt | Russian | ru |
| Chinese (Simplified) | zh | Chinese (Traditional) | zh-TW |
| Japanese | ja | Korean | ko |
| Arabic | ar | Hindi | hi |
| Bengali | bn | Urdu | ur |
| Persian | fa | Turkish | tr |
| Polish | pl | Dutch | nl |
| Swedish | sv | Danish | da |
| Norwegian | no | Finnish | fi |
| Greek | el | Hebrew | he |

## ⚙️ Configuration

### Environment Variables

- **None required!** This application works out of the box

### Customization

You can modify the following in `app.py`:
- Server port (default: 7860)
- Server host (default: 0.0.0.0)
- UI theme and styling
- Translation behavior and debouncing
- LibreTranslate API endpoint (if you want to use a different instance)

## 🔧 Troubleshooting

### Common Issues

1. **Translation fails**
   - Check your internet connection
   - Verify the LibreTranslate API is accessible
   - Try refreshing the page

2. **Port already in use**
   - Change the port in `app.py` or stop the process using port 7860

3. **Virtual environment issues**
   - Make sure you've activated the `2ndTrans` environment
   - Reinstall dependencies: `pip install -r requirements.txt`

### Performance Tips

- Translation results are cached during the session
- Use "Auto" detection sparingly for better performance

## 🌟 Why LibreTranslate?

- **Free Forever**: No hidden costs or usage limits
- **Open Source**: Transparent, community-driven development
- **High Quality**: Excellent translation accuracy
- **Privacy Focused**: No data collection or tracking
- **Multiple Instances**: Can switch between different API endpoints
- **Self-Hostable**: Option to run your own instance if needed

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Review the LibreTranslate documentation
3. Open an issue in this repository

---

**Happy Translating! 🌍✨ (100% Free!)** 