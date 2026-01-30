@echo off
echo ========================================
echo Starting Frontend Development Server
echo ========================================
echo.

cd frontend

echo Checking for node_modules...
if not exist node_modules (
    echo Installing dependencies...
    call yarn install
)

echo.
echo Starting Vite dev server on http://localhost:5173
echo.
call yarn dev

pause
