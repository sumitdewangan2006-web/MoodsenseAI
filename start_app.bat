@echo off
REM MoodSense AI - Quick Start Script
REM ==================================
REM Ye script automatically environment setup karega aur app chalayega

echo ===============================================
echo    MoodSense AI - Quick Start Setup
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [1/5] Python detected!
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [2/5] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
) else (
    echo [2/5] Virtual environment already exists!
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install requirements
echo [4/5] Installing dependencies...
echo This may take a few minutes...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
echo Dependencies installed!
echo.

REM Check if model exists
if not exist "models\emotion_model.h5" (
    echo ===============================================
    echo    WARNING: Model not found!
    echo ===============================================
    echo.
    echo Before running the app, you need to:
    echo 1. Download fer2013.csv from Kaggle
    echo 2. Place it in data/ folder
    echo 3. Run: python train_model.py
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

REM Run Streamlit app
echo [5/5] Starting MoodSense AI...
echo.
echo ===============================================
echo    App will open in your browser!
echo    Press Ctrl+C to stop
echo ===============================================
echo.

streamlit run app.py

pause
