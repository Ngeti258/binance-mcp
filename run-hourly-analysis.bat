@echo off
REM Hourly Crypto Market Analysis Automation Script
REM This script navigates to the project directory and starts Claude Code with the analysis command

REM Navigate to project directory
cd /d "C:\Users\ngeti\Downloads\binance-mcp"

REM Log the execution
echo [%date% %time%] Starting hourly market analysis >> automation.log
echo. >> automation.log

REM Run ALTCOIN-FOCUSED analysis first
echo [%date% %time%] Running altcoin-focused analysis (/market-analysis)... >> automation.log
claude "/market-analysis"
echo [%date% %time%] Altcoin analysis completed >> automation.log
echo. >> automation.log

REM Wait 30 seconds between analyses to avoid rate limits
echo [%date% %time%] Waiting 30 seconds before next analysis... >> automation.log
timeout /t 30 /nobreak > nul

REM Run MAJOR COINS analysis second
echo [%date% %time%] Running major coins analysis (/majors)... >> automation.log
claude "/majors"
echo [%date% %time%] Major coins analysis completed >> automation.log
echo. >> automation.log

REM Log final completion
echo [%date% %time%] === All analyses completed successfully === >> automation.log
echo. >> automation.log
