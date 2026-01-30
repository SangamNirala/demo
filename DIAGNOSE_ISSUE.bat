@echo off
echo ============================================================
echo DIAGNOSTIC SCRIPT - Troubleshooting Connection Issues
echo ============================================================
echo.

echo Step 1: Checking if backend server is running...
echo ============================================================
curl -s http://localhost:8000/api/health >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✓ Backend server is RUNNING
    echo.
    curl http://localhost:8000/api/health
    echo.
) else (
    echo ✗ Backend server is NOT RUNNING
    echo.
    echo SOLUTION: Start the backend server first!
    echo   Run: START_BACKEND.bat
    echo.
    pause
    exit /b 1
)

echo.
echo Step 2: Testing student endpoint with roll number 2023BT2086...
echo ============================================================
curl -i http://localhost:8000/api/student/2023BT2086
echo.

echo.
echo Step 3: Checking CORS configuration...
echo ============================================================
echo Frontend URL should be allowed in CORS settings.
echo Expected: http://localhost:5173
echo.

echo.
echo Step 4: Checking frontend .env file...
echo ============================================================
if exist "frontend\.env" (
    echo ✓ .env file exists
    type frontend\.env
) else (
    echo ✗ .env file NOT FOUND
    echo Creating .env file...
    copy frontend\.env.example frontend\.env
)

echo.
echo.
echo Step 5: Common Issues and Solutions...
echo ============================================================
echo.
echo Issue 1: "Failed to fetch" error
echo   → Backend is not running
echo   → Solution: Run START_BACKEND.bat
echo.
echo Issue 2: CORS error
echo   → Frontend URL not allowed
echo   → Solution: Check backend CORS settings
echo.
echo Issue 3: "Student not found"
echo   → Roll number doesn't exist or typo
echo   → Solution: Use roll numbers from FRONTEND_TESTING_GUIDE.md
echo.
echo Issue 4: Network error
echo   → Wrong API URL in frontend
echo   → Solution: Check frontend/.env has VITE_API_URL=http://localhost:8000
echo.
echo ============================================================
echo.
pause
