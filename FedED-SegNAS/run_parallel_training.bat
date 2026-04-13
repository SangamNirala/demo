@echo off
REM Parallel Training Script - Runs both configurations simultaneously
REM WARNING: This requires significant system resources!

echo ================================================================================
echo PARALLEL TRAINING WORKFLOW
echo ================================================================================
echo.
echo This script will run BOTH trainings simultaneously:
echo   - Terminal 1: 500-epoch training (HIGH_ACCURACY config)
echo   - Terminal 2: 1000-epoch training (PAPER config)
echo.
echo ⚠️  WARNING: This requires:
echo   - 8+ CPU cores
echo   - 16+ GB RAM
echo   - Both will run slower (1.5-2x longer each)
echo.
echo Estimated time: 18-42 days (both complete together)
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Starting parallel training...
echo.

REM Start first training in a new window
start "Training: 500 Epochs (HIGH_ACCURACY)" cmd /k "python train_all_models_comprehensive.py --high-accuracy"

REM Wait 5 seconds to avoid startup conflicts
timeout /t 5 /nobreak

REM Start second training in another new window
start "Training: 1000 Epochs (PAPER)" cmd /k "python train_all_models_comprehensive222.py"

echo.
echo ✅ Both training processes started in separate windows!
echo.
echo Monitor progress in:
echo   - Window 1: 500-epoch training
echo   - Window 2: 1000-epoch training
echo.
echo Results will be saved to separate timestamped folders:
echo   - results/comprehensive_training_YYYYMMDD_HHMMSS/
echo.
echo To stop training:
echo   - Close the respective terminal window, or
echo   - Press Ctrl+C in that window
echo.
pause
