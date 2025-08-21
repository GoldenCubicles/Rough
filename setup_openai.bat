@echo off
echo 🚀 Setting up OpenAI Translation API...
echo.

REM Check if virtual environment exists
if not exist "2ndTrans\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run setup_venv.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo ✅ Activating virtual environment...
call 2ndTrans\Scripts\activate.bat

REM Install OpenAI requirements
echo 📦 Installing OpenAI requirements...
pip install -r requirements_openai.txt

echo.
echo 🎯 Setup complete! Now you need to:
echo 1. Set your OpenAI API key:
echo    set OPENAI_API_KEY=your-key-here
echo.
echo 2. Or create a .env file with:
echo    OPENAI_API_KEY=your-key-here
echo.
echo 3. Run the API:
echo    python OpensourceAPI.py
echo.
echo 4. Test it:
echo    python test_openai_api.py
echo.
pause
