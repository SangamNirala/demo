@echo off
REM Parallel Training by Model - Smart resource distribution
REM Trains different models in parallel to avoid duplicate work

echo ================================================================================
echo PARALLEL TRAINING BY MODEL (SMART APPROACH)
echo ================================================================================
echo.
echo This script trains different models in parallel:
echo   - Terminal 1: Models 1-4 with 500 epochs
echo   - Terminal 2: Models 5-8 with 1000 epochs
echo.
echo Benefits:
echo   ✅ No duplicate work
echo   ✅ Better resource utilization
echo   ✅ Faster overall completion
echo.
echo Estimated time: ~25-35 days (both complete together)
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Starting parallel training by model...
echo.

REM Start models 1-4 with 500 epochs
start "Training: Models 1-4 (500 epochs)" cmd /k "python train_all_models_comprehensive.py --high-accuracy --model model1 && python train_all_models_comprehensive.py --high-accuracy --model model2 && python train_all_models_comprehensive.py --high-accuracy --model model3 && python train_all_models_comprehensive.py --high-accuracy --model model4"

REM Wait 5 seconds
timeout /t 5 /nobreak

REM Start models 5-8 with 1000 epochs
start "Training: Models 5-8 (1000 epochs)" cmd /k "python train_all_models_comprehensive222.py --model model5 && python train_all_models_comprehensive222.py --model model6 && python train_all_models_comprehensive222.py --model model7 && python train_all_models_comprehensive222.py --model model8"

echo.
echo ✅ Both training processes started!
echo.
echo Terminal 1: Training models 1-4 with 500 epochs
echo Terminal 2: Training models 5-8 with 1000 epochs
echo.
echo Results will be saved to:
echo   - results/comprehensive_training_YYYYMMDD_HHMMSS/
echo.
pause
