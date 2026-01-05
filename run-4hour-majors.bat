@echo off
REM ================================================================
REM 4-Hour Major Cryptocurrencies Analysis - FULLY AUTOMATED
REM Runs at: 6 AM, 10 AM, 2 PM, 6 PM, 10 PM EAT (Nairobi timezone)
REM Analyzes 15 major cryptos with technical indicators
REM NO USER INPUT REQUIRED
REM ================================================================

REM Change to script directory
cd /d "%~dp0"

REM Create directories if they don't exist
if not exist "logs" mkdir logs
if not exist "analysis_reports" mkdir analysis_reports

REM Log execution start
echo [%date% %time%] Starting 4-hour majors analysis >> logs\analysis_runs.log

REM Run Python script (fully automated)
python automated_majors_analysis.py >> logs\analysis_output.log 2>&1

REM Log completion
echo [%date% %time%] Majors analysis completed >> logs\analysis_runs.log

REM Exit without pause for automated execution
exit /b 0
