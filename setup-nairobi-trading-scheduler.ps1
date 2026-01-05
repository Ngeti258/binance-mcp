# Nairobi/Kenya Trading Scheduler Setup
# Optimized for EAT timezone (UTC+3)
# Sets up automated paper trading monitoring and analysis
#
# REQUIRES: Administrator privileges
# Run as: Right-click then Run as Administrator

#Requires -RunAsAdministrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "NAIROBI TRADING SCHEDULER SETUP" -ForegroundColor Cyan
Write-Host "Timezone: East Africa Time (EAT, UTC+3)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Verify BAT files exist
$RequiredFiles = @(
    "run-check-trades.bat",
    "run-4hour-majors.bat",
    "run-daily-review.bat"
)

Write-Host "Checking required files..." -ForegroundColor Yellow
foreach ($file in $RequiredFiles) {
    $filePath = Join-Path $ScriptDir $file
    if (-not (Test-Path $filePath)) {
        Write-Host "ERROR: Missing file: $file" -ForegroundColor Red
        exit 1
    }
    Write-Host "  [OK] Found: $file" -ForegroundColor Green
}
Write-Host ""

# Ask user for scheduling preferences
Write-Host "SCHEDULING OPTIONS" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. RECOMMENDED - Complete Auto Trading (All schedules)" -ForegroundColor Green
Write-Host "   Quick checks: Every 30 minutes (6AM to 11PM EAT)"
Write-Host "   Major analysis: Every 4 hours (6AM, 10AM, 2PM, 6PM, 10PM EAT)"
Write-Host "   Daily review: 11PM EAT"
Write-Host ""
Write-Host "2. Moderate - Analysis Only" -ForegroundColor Yellow
Write-Host "   Major analysis: Every 4 hours"
Write-Host "   Daily review: 11PM EAT"
Write-Host ""
Write-Host "3. Light - Daily Only" -ForegroundColor Yellow
Write-Host "   Major analysis: 6AM, 2PM, 10PM EAT"
Write-Host "   Daily review: 11PM EAT"
Write-Host ""
Write-Host "4. Custom - Manual Selection" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "Select option (1-4)"

# Task scheduler setup
$TaskName_Prefix = "CryptoTrading_Nairobi"

# Function to create scheduled task
function Create-ScheduledTask {
    param(
        [string]$TaskName,
        [string]$Description,
        [string]$BatFile,
        [string]$TriggerType,
        [string]$Time,
        [int]$Interval
    )

    $BatPath = Join-Path $ScriptDir $BatFile
    $Action = New-ScheduledTaskAction -Execute $BatPath -WorkingDirectory $ScriptDir

    switch ($TriggerType) {
        "Once" {
            $Trigger = New-ScheduledTaskTrigger -Daily -At $Time
        }
        "Interval" {
            $StartTime = "06:00"
            $EndTime = "23:00"
            $Trigger = New-ScheduledTaskTrigger -Once -At $StartTime -RepetitionInterval (New-TimeSpan -Minutes $Interval) -RepetitionDuration (New-TimeSpan -Hours 17)
        }
        "Multiple" {
            $Times = @("06:00", "10:00", "14:00", "18:00", "22:00")
            $Triggers = @()
            foreach ($t in $Times) {
                $Triggers += New-ScheduledTaskTrigger -Daily -At $t
            }
            $Trigger = $Triggers
        }
        "TripleDaily" {
            $Times = @("06:00", "14:00", "22:00")
            $Triggers = @()
            foreach ($t in $Times) {
                $Triggers += New-ScheduledTaskTrigger -Daily -At $t
            }
            $Trigger = $Triggers
        }
    }

    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($ExistingTask) {
        Write-Host "  Updating existing task: $TaskName" -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    Register-ScheduledTask -TaskName $TaskName -Description $Description -Action $Action -Trigger $Trigger | Out-Null
    Write-Host "  [OK] Created: $TaskName" -ForegroundColor Green
}

Write-Host ""
Write-Host "Creating scheduled tasks..." -ForegroundColor Cyan
Write-Host ""

switch ($choice) {
    "1" {
        Write-Host "Setting up COMPLETE AUTO TRADING schedule..." -ForegroundColor Green

        Create-ScheduledTask `
            -TaskName "$TaskName_Prefix`_QuickCheck_30min" `
            -Description "Quick paper trading position check every 30 min" `
            -BatFile "run-check-trades.bat" `
            -TriggerType "Interval" `
            -Interval 30

        Create-ScheduledTask `
            -TaskName "$TaskName_Prefix`_MajorAnalysis_4hour" `
            -Description "Comprehensive major cryptos analysis every 4 hours" `
            -BatFile "run-4hour-majors.bat" `
            -TriggerType "Multiple"

        Create-ScheduledTask `
            -TaskName "$TaskName_Prefix`_DailyReview" `
            -Description "Daily paper trading review at 11PM" `
            -BatFile "run-daily-review.bat" `
            -TriggerType "Once" `
            -Time "23:00"

        Write-Host ""
        Write-Host "[OK] Complete auto trading schedule activated!" -ForegroundColor Green
    }
    "2" {
        Write-Host "Setting up MODERATE schedule..." -ForegroundColor Yellow

        Create-ScheduledTask `
            -TaskName "$TaskName_Prefix`_MajorAnalysis_4hour" `
            -Description "Comprehensive major cryptos analysis every 4 hours" `
            -BatFile "run-4hour-majors.bat" `
            -TriggerType "Multiple"

        Create-ScheduledTask `
            -TaskName "$TaskName_Prefix`_DailyReview" `
            -Description "Daily paper trading review at 11PM" `
            -BatFile "run-daily-review.bat" `
            -TriggerType "Once" `
            -Time "23:00"

        Write-Host ""
        Write-Host "[OK] Moderate schedule activated!" -ForegroundColor Yellow
    }
    "3" {
        Write-Host "Setting up LIGHT schedule..." -ForegroundColor Yellow

        Create-ScheduledTask `
            -TaskName "$TaskName_Prefix`_MajorAnalysis_3x" `
            -Description "Major cryptos analysis 3x daily" `
            -BatFile "run-4hour-majors.bat" `
            -TriggerType "TripleDaily"

        Create-ScheduledTask `
            -TaskName "$TaskName_Prefix`_DailyReview" `
            -Description "Daily paper trading review at 11PM" `
            -BatFile "run-daily-review.bat" `
            -TriggerType "Once" `
            -Time "23:00"

        Write-Host ""
        Write-Host "[OK] Light schedule activated!" -ForegroundColor Yellow
    }
    "4" {
        Write-Host "Custom scheduling not yet implemented." -ForegroundColor Red
        Write-Host "Please edit this script or use Windows Task Scheduler manually." -ForegroundColor Red
    }
    default {
        Write-Host "Invalid selection. Exiting." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SETUP COMPLETE!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Created scheduled tasks:" -ForegroundColor Green
Get-ScheduledTask | Where-Object { $_.TaskName -like "$TaskName_Prefix*" } | ForEach-Object {
    Write-Host "  - $($_.TaskName)" -ForegroundColor White
    Write-Host "    $($_.Description)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Open Task Scheduler (taskschd.msc) to verify tasks" -ForegroundColor White
Write-Host "2. Test tasks manually by right-clicking then Run" -ForegroundColor White
Write-Host "3. Monitor logs in: $ScriptDir\logs" -ForegroundColor White
Write-Host "4. Analysis reports saved to: $ScriptDir\analysis_reports" -ForegroundColor White
Write-Host ""

Write-Host "NAIROBI TIMEZONE NOTES:" -ForegroundColor Cyan
Write-Host "- EAT is UTC+3 (no daylight saving)" -ForegroundColor White
Write-Host "- Best trading hours: 2PM to 6PM EAT (London and NY overlap)" -ForegroundColor White
Write-Host "- FOMC announcements: Typically 10PM EAT (2PM EST)" -ForegroundColor White
Write-Host "- Market opens: Asian 3AM, London 10AM, NY 3PM EAT" -ForegroundColor White
Write-Host ""

Write-Host "TO DISABLE AUTOMATION:" -ForegroundColor Red
Write-Host "  Get-ScheduledTask | Where-Object TaskName -like CryptoTrading_Nairobi* | Disable-ScheduledTask" -ForegroundColor Gray
Write-Host ""

Write-Host "TO REMOVE ALL TASKS:" -ForegroundColor Red
Write-Host "  Get-ScheduledTask | Where-Object TaskName -like CryptoTrading_Nairobi* | Unregister-ScheduledTask" -ForegroundColor Gray
Write-Host ""

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
