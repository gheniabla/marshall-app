@echo off
REM Marshall Defense Database - Quick Start Script for Windows

echo ==========================================
echo ^^!^! MARSHALL DEFENSE DATABASE
echo ==========================================
echo.

REM Check Python
echo Checking Python version...
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo %PYTHON_VERSION%
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo ✓ Dependencies installed
echo.

REM Initialize database
echo Scraping and populating database...
python scripts\populate_db.py --action populate
echo.

REM Add sample scores
echo Adding sample readiness scores...
python scripts\populate_db.py --action add-scores
echo.

REM Start server
echo ==========================================
echo Launching FastAPI Server
echo ==========================================
echo.
echo Access the application at:
echo   Web: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
