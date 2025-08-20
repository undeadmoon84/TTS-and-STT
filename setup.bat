@echo off
echo ============================================
echo   Python Project Setup (Windows)
echo   Using Python 3.13.7
echo ============================================

:: Check if python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.13.7 and add it to PATH.
    pause
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo Installing requirements...
pip install -r requirements.txt

:: Setup complete
echo ============================================
echo Setup complete!
echo To activate later, run: run.bat
echo ============================================

:: Optional: run main script automatically
if exist main.py (
    echo Starting application...
    python main.py
)
pause
