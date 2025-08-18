#!/bin/bash

echo "========================================"
echo "    Setting up Virtual Environment"
echo "========================================"
echo ""
echo "This script will create and activate a virtual environment named '2ndTrans'"
echo "and install all required dependencies."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

echo "✅ Python found"
python3 --version

echo ""
echo "Creating virtual environment '2ndTrans'..."
python3 -m venv 2ndTrans

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created successfully"

echo ""
echo "Activating virtual environment..."
source 2ndTrans/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo "✅ Dependencies installed successfully"

echo ""
echo "========================================"
echo "    Setup Complete! 🎉"
echo "========================================"
echo ""
echo "Your virtual environment '2ndTrans' is ready!"
echo ""
echo "To use it in the future:"
echo "1. Navigate to this directory"
echo "2. Run: source 2ndTrans/bin/activate"
echo "3. Run: python app.py"
echo ""
echo "To test your setup, run: python test_setup.py"
echo ""
echo "Press Enter to test the setup..."
read

echo ""
echo "Running setup test..."
python test_setup.py

echo ""
echo "========================================"
echo "    Ready to Run! 🚀"
echo "========================================"
echo ""
echo "Your translator is ready! Run: python app.py"
echo ""
echo "Press Enter to exit..."
read 