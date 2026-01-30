@echo off
echo ============================================================
echo BACKEND-FRONTEND CONNECTION TEST
echo ============================================================
echo.
echo This script will test if the backend and frontend can communicate.
echo.
echo IMPORTANT: Make sure the backend server is running!
echo            Run START_BACKEND.bat in another terminal first.
echo.
pause
echo.

echo [1/3] Testing Backend Health...
echo ============================================================
curl -s http://localhost:8000/api/health
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Backend is responding
) else (
    echo.
    echo ✗ Backend is NOT responding
    echo   Make sure backend is running: START_BACKEND.bat
    pause
    exit /b 1
)

echo.
echo.
echo [2/3] Testing Student Data Endpoint...
echo ============================================================
echo Testing with roll number: 2023BT2086
curl -s http://localhost:8000/api/student/2023BT2086
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Student endpoint is working
) else (
    echo.
    echo ✗ Student endpoint failed
)

echo.
echo.
echo [3/3] Testing Prediction Endpoint...
echo ============================================================
echo Testing prediction for roll number: 2023BT2086
curl -X POST -s http://localhost:8000/api/predict/2023BT2086
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Prediction endpoint is working
) else (
    echo.
    echo ✗ Prediction endpoint failed
)

echo.
echo.
echo ============================================================
echo CONNECTION TEST COMPLETE
echo ============================================================
echo.
echo If all tests passed, your backend is ready!
echo The frontend will be able to connect to these endpoints.
echo.
echo Next: Start the frontend with START_FRONTEND.bat
echo.
pause
