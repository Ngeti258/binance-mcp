# ================================================================
# Claude Code Automated Trading Scheduler Setup
# Sets up Windows Task Scheduler for fully automated trading
# Run this script as Administrator
# ================================================================

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Claude Code Trading Automation Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator. Some tasks may fail to create." -ForegroundColor Yellow
    Write-Host "Consider running PowerShell as Administrator." -ForegroundColor Yellow
    Write-Host ""
}

# Task 1: Trade Checker - Multiple times per hour (every 30 min = 48 triggers per day)
Write-Host "Creating Task 1: Trade Checker (every 30 minutes)..." -ForegroundColor Green
$action1 = New-ScheduledTaskAction -Execute "$scriptPath\run-claude-check-trades.bat" -WorkingDirectory $scriptPath

# Create triggers for every 30 minutes (00:00, 00:30, 01:00, 01:30, etc.)
$triggers1 = @()
for ($hour = 0; $hour -lt 24; $hour++) {
    $triggers1 += New-ScheduledTaskTrigger -Daily -At ("{0:D2}:00" -f $hour)
    $triggers1 += New-ScheduledTaskTrigger -Daily -At ("{0:D2}:30" -f $hour)
}

$settings1 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 15)
try {
    Register-ScheduledTask -TaskName "Claude-Trading-CheckTrades" -Action $action1 -Trigger $triggers1 -Settings $settings1 -Force | Out-Null
    Write-Host "  [OK] Trade Checker task created (runs every 30 minutes)" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] Could not create Trade Checker task: $_" -ForegroundColor Red
}

# Task 2: Majors Analysis - Every 4 hours (6 AM, 10 AM, 2 PM, 6 PM, 10 PM)
Write-Host "Creating Task 2: Majors Analysis (5 times daily)..." -ForegroundColor Green
$action2 = New-ScheduledTaskAction -Execute "$scriptPath\run-claude-majors.bat" -WorkingDirectory $scriptPath
$triggers2 = @(
    New-ScheduledTaskTrigger -Daily -At "06:00"
    New-ScheduledTaskTrigger -Daily -At "10:00"
    New-ScheduledTaskTrigger -Daily -At "14:00"
    New-ScheduledTaskTrigger -Daily -At "18:00"
    New-ScheduledTaskTrigger -Daily -At "22:00"
)
$settings2 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 1)
try {
    Register-ScheduledTask -TaskName "Claude-Trading-MajorsAnalysis" -Action $action2 -Trigger $triggers2 -Settings $settings2 -Force | Out-Null
    Write-Host "  [OK] Majors Analysis task created (6AM, 10AM, 2PM, 6PM, 10PM)" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] Could not create Majors Analysis task: $_" -ForegroundColor Red
}

# Task 3: Daily Review - Once at 11 PM
Write-Host "Creating Task 3: Daily Review (11 PM)..." -ForegroundColor Green
$action3 = New-ScheduledTaskAction -Execute "$scriptPath\run-claude-daily-review.bat" -WorkingDirectory $scriptPath
$trigger3 = New-ScheduledTaskTrigger -Daily -At "23:00"
$settings3 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30)
try {
    Register-ScheduledTask -TaskName "Claude-Trading-DailyReview" -Action $action3 -Trigger $trigger3 -Settings $settings3 -Force | Out-Null
    Write-Host "  [OK] Daily Review task created (runs at 11 PM)" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] Could not create Daily Review task: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Scheduled Tasks Created:" -ForegroundColor White
Write-Host "  1. Claude-Trading-CheckTrades    - Every 30 minutes (48x/day)" -ForegroundColor Gray
Write-Host "  2. Claude-Trading-MajorsAnalysis - 6AM, 10AM, 2PM, 6PM, 10PM" -ForegroundColor Gray
Write-Host "  3. Claude-Trading-DailyReview    - 11 PM daily" -ForegroundColor Gray
Write-Host ""
Write-Host "To verify tasks exist, run:" -ForegroundColor Yellow
Write-Host '  Get-ScheduledTask | Where-Object {$_.TaskName -like "Claude-*"}' -ForegroundColor Gray
Write-Host ""
Write-Host "To test manually:" -ForegroundColor Yellow
Write-Host "  .\run-claude-majors.bat" -ForegroundColor Gray
Write-Host ""
Write-Host "Logs saved to: $scriptPath\logs\" -ForegroundColor Green
