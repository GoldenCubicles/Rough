@echo off
echo Setting up Gemini API environment...

REM Check if virtual environment exists
if not exist "2ndTrans\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv 2ndTrans
)

REM Activate virtual environment
echo Activating virtual environment...
call 2ndTrans\Scripts\activate.bat

REM Install Gemini dependencies
echo Installing Gemini dependencies...
pip install -r requirements_gemini.txt

echo.
echo Setup completed! 
echo.
echo To start the Gemini API:
echo   1. Edit GeminiAPI.py and add your API key
echo   2. Run: python GeminiAPI.py
echo.
echo To test the API:
echo   python test_gemini_api.py
echo.
echo Get your free Gemini API key from:
echo   https://makersuite.google.com/app/apikey
echo.
pause

