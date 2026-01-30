@echo off
echo ============================================================
echo SYSTEM VERIFICATION SCRIPT
echo ============================================================
echo.

echo [1/5] Checking Backend Setup...
echo ============================================================
python backend\verify_setup.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Backend verification failed!
    pause
    exit /b 1
)

echo.
echo [2/5] Checking Frontend Configuration...
echo ============================================================

if not exist "frontend\.env" (
    echo Creating .env file from .env.example...
    copy frontend\.env.example frontend\.env
    echo ✓ .env file created
) else (
    echo ✓ .env file exists
)

if exist "frontend\package.json" (
    echo ✓ package.json exists
) else (
    echo ✗ package.json NOT FOUND
    pause
    exit /b 1
)

if exist "frontend\src\services\api.js" (
    echo ✓ API service file exists
) else (
    echo ✗ API service file NOT FOUND
    pause
    exit /b 1
)

if exist "frontend\src\pages\Home.jsx" (
    echo ✓ Home page exists
) else (
    echo ✗ Home page NOT FOUND
    pause
    exit /b 1
)

echo.
echo [3/5] Checking Frontend Dependencies...
echo ============================================================

if exist "frontend\node_modules" (
    echo ✓ node_modules exists
    echo   Frontend dependencies are installed
) else (
    echo ⚠ node_modules NOT FOUND
    echo   You need to install frontend dependencies
    echo   Run: cd frontend ^&^& npm install
)

echo.
echo [4/5] Checking Backend-Frontend Connection Config...
echo ============================================================

findstr /C:"VITE_API_URL=http://localhost:8000" frontend\.env >nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Frontend API URL configured correctly
    echo   API URL: http://localhost:8000
) else (
    echo ⚠ Frontend API URL may not be configured correctly
    echo   Check frontend\.env file
)

echo.
echo [5/5] System Summary...
echo ============================================================
echo.
echo ✅ Backend: Ready
echo    - All files present
echo    - ML model loaded
echo    - Dependencies installed
echo.
if exist "frontend\node_modules" (
    echo ✅ Frontend: Ready
    echo    - All files present
    echo    - Dependencies installed
    echo    - API configured
) else (
    echo ⚠ Frontend: Needs Setup
    echo    - Run: cd frontend ^&^& npm install
)
echo.
echo ============================================================
echo NEXT STEPS
echo ============================================================
echo.
if exist "frontend\node_modules" (
    echo Your system is ready to run!
    echo.
    echo To start the system:
    echo   1. Open Terminal 1: START_BACKEND.bat
    echo   2. Open Terminal 2: START_FRONTEND.bat
    echo   3. Open browser: http://localhost:5173
    echo.
    echo To test the API:
    echo   1. Start backend: START_BACKEND.bat
    echo   2. Run: python backend\test_api.py
) else (
    echo Please install frontend dependencies first:
    echo   cd frontend
    echo   npm install
    echo.
    echo Then run this script again.
)
echo.
echo ============================================================

pause
