@echo off
REM Automated Trading Analysis - Windows Batch Script
REM This script activates the virtual environment and runs the automated analysis

echo ================================================================================
echo AUTOMATED CRYPTOCURRENCY TRADING ANALYSIS
echo ================================================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Using system Python.
    echo Run 'python -m venv venv' to create virtual environment.
    echo.
)

REM Run automated analysis
echo Running automated analysis...
echo.
python automated_analysis.py %*

REM Check exit code
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Analysis completed successfully!
) else (
    echo.
    echo ❌ Analysis failed with error code %ERRORLEVEL%
    echo Check automated_analysis.log for details.
)

echo.
echo ================================================================================
echo Press any key to exit...
pause >nul
