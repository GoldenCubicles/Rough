@echo off
echo ========================================
echo    Setting up Virtual Environment
echo ========================================
echo.
echo This script will create and activate a virtual environment named "2ndTrans"
echo and install all required dependencies.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo ✅ Python found
python --version

echo.
echo Creating virtual environment "2ndTrans"...
python -m venv 2ndTrans

if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created successfully

echo.
echo Activating virtual environment...
call 2ndTrans\Scripts\activate

if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated

echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

echo.
echo ========================================
echo    Setup Complete! 🎉
echo ========================================
echo.
echo Your virtual environment "2ndTrans" is ready!
echo.
echo To use it in the future:
echo 1. Navigate to this directory
echo 2. Run: 2ndTrans\Scripts\activate
echo 3. Run: python app.py
echo.
echo To test your setup, run: python test_setup.py
echo.
echo Press any key to test the setup...
pause >nul

echo.
echo Running setup test...
python test_setup.py

echo.
echo ========================================
echo    Ready to Run! 🚀
echo ========================================
echo.
echo Your translator is ready! Run: python app.py
echo.
pause 