@echo off
REM ================================================================
REM Automated Claude Code Trade Checker
REM Starts Claude Code CLI to check and manage open positions
REM FULLY AUTOMATED - NO USER INPUT REQUIRED
REM ================================================================

REM Change to script directory
cd /d "%~dp0"

REM Create logs directory
if not exist "logs" mkdir logs

REM Log execution start
echo [%date% %time%] Starting Claude Code trade check >> logs\claude_runs.log

REM Run Claude Code to check trades
REM Uses -p for non-interactive, --permission-mode dontAsk for auto-approve
claude -p --permission-mode dontAsk "Run python check_trades.py and show me the results" >> logs\claude_check_trades_output.log 2>&1

REM Log completion
echo [%date% %time%] Claude Code trade check completed >> logs\claude_runs.log

exit /b 0
