#!/bin/bash

echo "========================================"
echo "    Streamlit Translator Setup"
echo "========================================"
echo

echo "🚀 Creating virtual environment..."
python3 -m venv 2ndTrans

echo
echo "✅ Activating virtual environment..."
source 2ndTrans/bin/activate

echo
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "🎉 Setup complete!"
echo
echo "📋 To run the application:"
echo
echo "1. Start the API backend:"
echo "   python api.py"
echo
echo "2. In a new terminal, start Streamlit:"
echo "   streamlit run streamlit_app.py"
echo
echo "🌐 The Streamlit app will open at: http://localhost:8501"
echo "🔌 The API will run at: http://localhost:8000"
echo
echo "Press Enter to exit..."
read 