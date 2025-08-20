@echo off
echo ============================================
echo   Running TTS App
echo ============================================

:: Check if venv exists
if not exist venv (
    echo [ERROR] Virtual environment not found.
    echo Please run setup.bat first!
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run main script
if exist main.py (
    python main.py
) else (
    echo [ERROR] main.py not found!
)

pause
