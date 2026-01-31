@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
echo.

cd backend

echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\activate
    echo Then run: pip install -r requirements.txt
    pause
    exit
)

echo.
echo Starting Flask server on http://localhost:8000
echo.
python server.py

pause
