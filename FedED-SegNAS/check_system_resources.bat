@echo off
REM System Resource Checker - Check if your system can handle parallel training

echo ================================================================================
echo SYSTEM RESOURCE CHECK
echo ================================================================================
echo.
echo Checking if your system can handle parallel training...
echo.

REM Check CPU cores
echo [CPU Information]
wmic cpu get NumberOfCores,NumberOfLogicalProcessors /format:list
echo.

REM Check RAM
echo [Memory Information]
wmic ComputerSystem get TotalPhysicalMemory /format:list
wmic OS get FreePhysicalMemory /format:list
echo.

REM Check current CPU usage
echo [Current CPU Usage]
wmic cpu get loadpercentage /format:list
echo.

REM Check Python processes
echo [Current Python Processes]
tasklist /FI "IMAGENAME eq python.exe" /FO TABLE
echo.

echo ================================================================================
echo RECOMMENDATIONS
echo ================================================================================
echo.
echo For PARALLEL training, you need:
echo   ✅ 8+ CPU cores (or 16+ logical processors)
echo   ✅ 16+ GB total RAM
echo   ✅ 12+ GB free RAM
echo   ✅ CPU usage below 40%%
echo.
echo For SEQUENTIAL training:
echo   ✅ 4+ CPU cores
echo   ✅ 8+ GB total RAM
echo   ✅ 6+ GB free RAM
echo.
echo Current Python training processes: Check above
echo.
pause
