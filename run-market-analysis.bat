@echo off
REM Altcoin-Focused Market Analysis Automation Script
REM This script runs the /market-analysis command (90% altcoins focus)

REM Navigate to project directory
cd /d "C:\Users\ngeti\Downloads\binance-mcp"

REM Log the execution
echo [%date% %time%] Starting ALTCOIN-FOCUSED market analysis >> automation.log
claude "/market-analysis"
echo [%date% %time%] Altcoin analysis completed >> automation.log
echo. >> automation.log
