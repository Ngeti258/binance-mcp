@echo off
REM ================================================================
REM Automated Claude Code Daily Review
REM Starts Claude Code CLI to generate daily performance review
REM FULLY AUTOMATED - NO USER INPUT REQUIRED
REM ================================================================

REM Change to script directory
cd /d "%~dp0"

REM Create logs directory
if not exist "logs" mkdir logs
if not exist "logs\daily_reviews" mkdir logs\daily_reviews

REM Log execution start
echo [%date% %time%] Starting Claude Code daily review >> logs\claude_runs.log

REM Run Claude Code for daily review
REM Uses -p for non-interactive, --permission-mode dontAsk for auto-approve
claude -p --permission-mode dontAsk "Run python daily_review.py and show me the results" >> logs\claude_daily_review_output.log 2>&1

REM Log completion
echo [%date% %time%] Claude Code daily review completed >> logs\claude_runs.log

exit /b 0
