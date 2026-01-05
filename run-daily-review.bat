@echo off
REM ================================================================
REM Daily Paper Trading Review - FULLY AUTOMATED
REM Runs once per day at 11 PM EAT (Nairobi timezone)
REM Reviews closed trades, calculates stats, identifies patterns
REM NO USER INPUT REQUIRED
REM ================================================================

REM Change to script directory
cd /d "%~dp0"

REM Create logs directory
if not exist "logs" mkdir logs
if not exist "logs\daily_reviews" mkdir logs\daily_reviews

REM Log execution start
echo [%date% %time%] Starting daily review >> logs\daily_reviews.log

REM Run Python script (fully automated)
python daily_review.py >> logs\daily_review_output.log 2>&1

REM Log completion
echo [%date% %time%] Daily review completed >> logs\daily_reviews.log

REM Exit without pause for automated execution
exit /b 0
