@echo off
echo ========================================
echo Backend Setup Script
echo ========================================
echo.

cd backend

echo Step 1: Creating virtual environment...
if exist venv (
    echo Virtual environment already exists.
) else (
    python -m venv venv
    echo Virtual environment created.
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 4: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 5: Checking model files...
if exist ml\saved_models\dropout_model.pkl (
    echo ✓ Model files found
) else (
    echo ⚠ Warning: Model files not found in ml\saved_models\
    echo   Please ensure you have trained the model or copied the model files.
)

echo.
echo Step 6: Checking database...
if exist database\students_data.json (
    echo ✓ Student database found
) else (
    echo ⚠ Warning: Student database not found
)

echo.
echo Step 7: Creating .env file...
if exist .env (
    echo .env file already exists
) else (
    copy .env.example .env
    echo .env file created from .env.example
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the backend server, run:
echo   START_BACKEND.bat
echo.
echo Or manually:
echo   cd backend
echo   venv\Scripts\activate
echo   python server.py
echo.

pause
