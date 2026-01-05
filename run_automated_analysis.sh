#!/bin/bash
# Automated Trading Analysis - Shell Script (Linux/Mac)
# This script activates the virtual environment and runs the automated analysis

echo "================================================================================"
echo "AUTOMATED CRYPTOCURRENCY TRADING ANALYSIS"
echo "================================================================================"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Using system Python."
    echo "Run 'python3 -m venv venv' to create virtual environment."
    echo ""
fi

# Run automated analysis
echo "Running automated analysis..."
echo ""
python3 automated_analysis.py "$@"

# Check exit code
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Analysis completed successfully!"
else
    echo ""
    echo "❌ Analysis failed with error code $EXIT_CODE"
    echo "Check automated_analysis.log for details."
fi

echo ""
echo "================================================================================"
