# PowerShell script to set up two separate scheduled tasks with 30-minute offset
# Run this script as Administrator

$Task1Name = "CryptoAltcoinAnalysisHourly"
$Task2Name = "CryptoMajorsAnalysisHourly"

$Script1Path = "C:\Users\ngeti\Downloads\binance-mcp\run-market-analysis.bat"
$Script2Path = "C:\Users\ngeti\Downloads\binance-mcp\run-majors-analysis.bat"

$Description1 = "Hourly altcoin-focused crypto market analysis (90% altcoins)"
$Description2 = "Hourly major coins crypto market analysis (top 15 only)"

Write-Host "=== Setting Up Dual Crypto Analysis Scheduler ===" -ForegroundColor Cyan
Write-Host ""

# Remove existing tasks if they exist
$existingTask1 = Get-ScheduledTask -TaskName $Task1Name -ErrorAction SilentlyContinue
if ($existingTask1) {
    Write-Host "Removing existing task: $Task1Name" -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $Task1Name -Confirm:$false
}

$existingTask2 = Get-ScheduledTask -TaskName $Task2Name -ErrorAction SilentlyContinue
if ($existingTask2) {
    Write-Host "Removing existing task: $Task2Name" -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $Task2Name -Confirm:$false
}

# Remove old single task if it exists
$oldTask = Get-ScheduledTask -TaskName "CryptoMarketAnalysisHourly" -ErrorAction SilentlyContinue
if ($oldTask) {
    Write-Host "Removing old single task: CryptoMarketAnalysisHourly" -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName "CryptoMarketAnalysisHourly" -Confirm:$false
}

Write-Host ""
Write-Host "Creating Task 1: Altcoin Analysis (runs on the hour: X:00)" -ForegroundColor Green

# Task 1: Altcoin Analysis - Runs on the hour (X:00)
$Action1 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$Script1Path`""
$Trigger1 = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddHours((Get-Date).Hour) -RepetitionInterval (New-TimeSpan -Hours 1)

$Settings1 = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $Task1Name `
    -Action $Action1 `
    -Trigger $Trigger1 `
    -Settings $Settings1 `
    -Description $Description1

Write-Host "[SUCCESS] Created: $Task1Name" -ForegroundColor Green
Write-Host ""

Write-Host "Creating Task 2: Major Coins Analysis (runs at half-past: X:30)" -ForegroundColor Green

# Task 2: Major Coins Analysis - Runs 30 minutes after the hour (X:30)
$Action2 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$Script2Path`""

# Calculate next X:30 time
$now = Get-Date
$nextHalfHour = $now.Date.AddHours($now.Hour).AddMinutes(30)
if ($now.Minute -ge 30) {
    $nextHalfHour = $nextHalfHour.AddHours(1)
}

$Trigger2 = New-ScheduledTaskTrigger -Once -At $nextHalfHour -RepetitionInterval (New-TimeSpan -Hours 1)

$Settings2 = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $Task2Name `
    -Action $Action2 `
    -Trigger $Trigger2 `
    -Settings $Settings2 `
    -Description $Description2

Write-Host "[SUCCESS] Created: $Task2Name" -ForegroundColor Green
Write-Host ""

Write-Host "=== Setup Complete! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Schedule:" -ForegroundColor Yellow
Write-Host "  - Altcoin Analysis (/market-analysis): Every hour at X:00 (e.g., 14:00, 15:00, 16:00)"
Write-Host "  - Major Coins Analysis (/majors):      Every hour at X:30 (e.g., 14:30, 15:30, 16:30)"
Write-Host ""
Write-Host "Next Run Times:" -ForegroundColor Yellow
$task1Info = Get-ScheduledTaskInfo -TaskName $Task1Name
$task2Info = Get-ScheduledTaskInfo -TaskName $Task2Name
Write-Host "  - Altcoin Analysis:   $($task1Info.NextRunTime)"
Write-Host "  - Major Coins Analysis: $($task2Info.NextRunTime)"
Write-Host ""
Write-Host "To manage tasks:" -ForegroundColor Cyan
Write-Host "  View:    Get-ScheduledTask | Where-Object {`$_.TaskName -like '*Crypto*'}"
Write-Host "  Disable: Disable-ScheduledTask -TaskName '$Task1Name'"
Write-Host "  Enable:  Enable-ScheduledTask -TaskName '$Task1Name'"
Write-Host "  Remove:  Unregister-ScheduledTask -TaskName '$Task1Name'"
Write-Host "  Run now: Start-ScheduledTask -TaskName '$Task1Name'"
Write-Host ""
Write-Host "Log file: automation.log" -ForegroundColor Cyan
Write-Host ""
