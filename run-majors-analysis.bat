@echo off
REM Major Coins Analysis Automation Script
REM This script runs the /majors command (top 15 coins only)

REM Navigate to project directory
cd /d "C:\Users\ngeti\Downloads\binance-mcp"

REM Log the execution
echo [%date% %time%] Starting MAJOR COINS analysis >> automation.log
claude "/majors"
echo [%date% %time%] Major coins analysis completed >> automation.log
echo. >> automation.log
