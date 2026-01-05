# PowerShell script to set up Windows Task Scheduler for hourly market analysis
# Run this script as Administrator

$TaskName = "CryptoMarketAnalysisHourly"
$ScriptPath = "C:\Users\ngeti\Downloads\binance-mcp\run-hourly-analysis.bat"
$Description = "Automated hourly cryptocurrency market analysis using Claude Code and MCP servers"

# Remove existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create a new scheduled task action
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ScriptPath`""

# Create hourly trigger (runs every hour, every day)
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)

# Set task settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -MultipleInstances IgnoreNew

# Register the scheduled task (will run as current user)
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description $Description

Write-Host "Successfully created scheduled task '$TaskName'!"
Write-Host "The task will run every hour starting from now."
Write-Host ""
Write-Host "To manage the task:"
Write-Host "  - View: Get-ScheduledTask -TaskName '$TaskName'"
Write-Host "  - Disable: Disable-ScheduledTask -TaskName '$TaskName'"
Write-Host "  - Enable: Enable-ScheduledTask -TaskName '$TaskName'"
Write-Host "  - Remove: Unregister-ScheduledTask -TaskName '$TaskName'"
Write-Host "  - Run now: Start-ScheduledTask -TaskName '$TaskName'"
Write-Host ""
Write-Host "Note: Task runs as BUILTIN\USERS by default. To change user context:"
Write-Host "  Open Task Scheduler > Find '$TaskName' > Properties > General tab > Change User"
