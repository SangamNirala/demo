@echo off
REM Sequential Training Script - Runs 500 epochs then 1000 epochs
REM This ensures no resource conflicts and optimal performance

echo ================================================================================
echo SEQUENTIAL TRAINING WORKFLOW
echo ================================================================================
echo.
echo This script will run:
echo   1. First:  500-epoch training (HIGH_ACCURACY config)
echo   2. Second: 1000-epoch training (PAPER config)
echo.
echo Estimated total time: 12-21 days + 41 days = 53-62 days
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo ================================================================================
echo PHASE 1: Training with 500 epochs (HIGH_ACCURACY)
echo ================================================================================
echo Start time: %date% %time%
echo.

python train_all_models_comprehensive.py --high-accuracy

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ERROR: Phase 1 training failed!
    echo Check the logs in results/comprehensive_training_* folder
    pause
    exit /b 1
)

echo.
echo ✅ Phase 1 complete!
echo.
echo ================================================================================
echo PHASE 2: Training with 1000 epochs (PAPER config)
echo ================================================================================
echo Start time: %date% %time%
echo.

python train_all_models_comprehensive222.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ERROR: Phase 2 training failed!
    echo Check the logs in results/comprehensive_training_* folder
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo ✅ ALL TRAINING COMPLETE!
echo ================================================================================
echo End time: %date% %time%
echo.
echo Results are saved in:
echo   - results/comprehensive_training_* folders
echo.
echo Next steps:
echo   1. Review final_summary.txt in each results folder
echo   2. Compare accuracies between 500 and 1000 epoch runs
echo   3. Analyze the plots/ subdirectories
echo.
pause
