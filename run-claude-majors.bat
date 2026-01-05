@echo off
REM ================================================================
REM Automated Claude Code Majors Analysis
REM Starts Claude Code CLI and runs /majors + /paper-trade commands
REM FULLY AUTOMATED - NO USER INPUT REQUIRED
REM ================================================================

REM Change to script directory
cd /d "%~dp0"

REM Create logs directory
if not exist "logs" mkdir logs

REM Log execution start
echo [%date% %time%] Starting Claude Code majors analysis >> logs\claude_runs.log

REM Run Claude Code with the /majors command followed by /paper-trade
REM Flags:
REM   -p (--print) = non-interactive mode
REM   --permission-mode dontAsk = auto-approve tool usage
REM   --allowedTools = specify allowed tools for security
claude -p --permission-mode dontAsk "/majors" >> logs\claude_majors_output.log 2>&1

REM Log completion
echo [%date% %time%] Claude Code majors analysis completed >> logs\claude_runs.log

REM Exit
exit /b 0
