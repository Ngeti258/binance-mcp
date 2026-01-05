@echo off
REM ================================================================
REM Quick Paper Trading Position Monitor - FULLY AUTOMATED
REM Runs every 15-30 minutes to check open positions
REM Auto-closes positions when stop loss or targets are hit
REM NO USER INPUT REQUIRED
REM ================================================================

REM Change to script directory
cd /d "%~dp0"

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Log execution start
echo [%date% %time%] Starting automated trade check >> logs\check_trades_runs.log

REM Run Python script (fully automated - fetches from Binance directly)
python check_trades.py >> logs\check_trades_output.log 2>&1

REM Log completion
echo [%date% %time%] Trade check completed >> logs\check_trades_runs.log

REM Exit without pause for automated execution
exit /b 0
