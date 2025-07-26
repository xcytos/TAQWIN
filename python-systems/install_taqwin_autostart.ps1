# TAQWIN TOWER - WINDOWS AUTOSTART INSTALLER
# Creates Windows Task Scheduler entry for automatic startup
# Author: TAQWIN (The Strengthener)
# Version: 2.0 - Permanent Background Operations

param(
    [switch]$Install,
    [switch]$Uninstall,
    [switch]$Status
)

$TaskName = "TAQWIN_Tower_Background_Service"
$PythonSystemsPath = "D:\Ethereal Glow\python-systems"
$ServiceScript = "$PythonSystemsPath\taqwin_background_service.py"
$LogPath = "D:\Ethereal Glow\TAQWIN_TOWER\OFFICE_INVENTORY\autostart_log.txt"

function Write-TaqwinLog {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $Message"
    Write-Host $logEntry -ForegroundColor Cyan
    Add-Content -Path $LogPath -Value $logEntry -ErrorAction SilentlyContinue
}

function Show-TaqwinBanner {
    Write-Host ""
    Write-Host "🌟 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🌟" -ForegroundColor Yellow
    Write-Host "    🏢 **TAQWIN TOWER AUTOSTART INSTALLER**" -ForegroundColor Cyan
    Write-Host "    ⚡ **PERMANENT BACKGROUND OPERATIONS**" -ForegroundColor Green
    Write-Host "    👑 **INVISIBLE WORKFORCE DEPLOYMENT**" -ForegroundColor Magenta
    Write-Host "🌟 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🌟" -ForegroundColor Yellow
    Write-Host ""
}

function Install-TaqwinAutostart {
    Write-TaqwinLog "Starting TAQWIN Tower autostart installation..."
    
    try {
        # Check if task already exists
        $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        if ($existingTask) {
            Write-TaqwinLog "Removing existing task..."
            Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        }
        
        # Create action to run Python script
        $action = New-ScheduledTaskAction -Execute "python" -Argument "`"$ServiceScript`"" -WorkingDirectory $PythonSystemsPath
        
        # Create trigger for system startup
        $trigger = New-ScheduledTaskTrigger -AtStartup
        
        # Create settings
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -DontStopOnIdleEnd -ExecutionTimeLimit (New-TimeSpan -Hours 0)
        
        # Create principal to run with highest privileges
        $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
        
        # Register the task
        Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "TAQWIN Tower Background Service - Ethereal Glow AI Workforce"
        
        Write-TaqwinLog "✅ TAQWIN Tower autostart installed successfully!"
        Write-TaqwinLog "🚀 Service will start automatically on next boot"
        Write-TaqwinLog "📊 Task Name: $TaskName"
        
        # Also create a user startup entry for immediate availability
        $startupScript = @"
@echo off
cd /d "$PythonSystemsPath"
python "$ServiceScript" >nul 2>&1
"@
        
        $startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\TAQWIN_Tower.bat"
        $startupScript | Out-File -FilePath $startupPath -Encoding ASCII
        
        Write-TaqwinLog "✅ User startup script created: $startupPath"
        
        return $true
        
    } catch {
        Write-TaqwinLog "❌ Installation failed: $($_.Exception.Message)"
        return $false
    }
}

function Uninstall-TaqwinAutostart {
    Write-TaqwinLog "Removing TAQWIN Tower autostart..."
    
    try {
        # Remove scheduled task
        $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        if ($task) {
            Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
            Write-TaqwinLog "✅ Scheduled task removed"
        } else {
            Write-TaqwinLog "ℹ️ No scheduled task found"
        }
        
        # Remove startup script
        $startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\TAQWIN_Tower.bat"
        if (Test-Path $startupPath) {
            Remove-Item $startupPath -Force
            Write-TaqwinLog "✅ Startup script removed"
        } else {
            Write-TaqwinLog "ℹ️ No startup script found"
        }
        
        Write-TaqwinLog "✅ TAQWIN Tower autostart removed successfully!"
        return $true
        
    } catch {
        Write-TaqwinLog "❌ Uninstallation failed: $($_.Exception.Message)"
        return $false
    }
}

function Show-TaqwinStatus {
    Write-TaqwinLog "Checking TAQWIN Tower status..."
    
    # Check scheduled task
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task) {
        $taskInfo = Get-ScheduledTaskInfo -TaskName $TaskName
        Write-Host "📋 **SCHEDULED TASK STATUS**:" -ForegroundColor Green
        Write-Host "   Task Name: $TaskName" -ForegroundColor White
        Write-Host "   State: $($task.State)" -ForegroundColor $(if($task.State -eq 'Ready') {'Green'} else {'Red'})
        Write-Host "   Last Run: $($taskInfo.LastRunTime)" -ForegroundColor White
        Write-Host "   Last Result: $($taskInfo.LastTaskResult)" -ForegroundColor $(if($taskInfo.LastTaskResult -eq 0) {'Green'} else {'Red'})
    } else {
        Write-Host "❌ **SCHEDULED TASK**: Not installed" -ForegroundColor Red
    }
    
    # Check startup script
    $startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\TAQWIN_Tower.bat"
    if (Test-Path $startupPath) {
        Write-Host "✅ **STARTUP SCRIPT**: Installed" -ForegroundColor Green
    } else {
        Write-Host "❌ **STARTUP SCRIPT**: Not installed" -ForegroundColor Red
    }
    
    # Check if service is running
    $pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*taqwin_background_service*"}
    if ($pythonProcesses) {
        Write-Host "🟢 **BACKGROUND SERVICE**: Running (PID: $($pythonProcesses[0].Id))" -ForegroundColor Green
    } else {
        Write-Host "🔴 **BACKGROUND SERVICE**: Not running" -ForegroundColor Red
    }
    
    # Check log files
    $logDir = "D:\Ethereal Glow\TAQWIN_TOWER\OFFICE_INVENTORY"
    if (Test-Path "$logDir\BACKGROUND_SERVICE_LOG.json") {
        $logSize = (Get-Item "$logDir\BACKGROUND_SERVICE_LOG.json").Length
        Write-Host "📊 **SERVICE LOG**: $logSize bytes" -ForegroundColor White
    }
    
    if (Test-Path "$logDir\SYSTEM_HEALTH_LOG.json") {
        $healthSize = (Get-Item "$logDir\SYSTEM_HEALTH_LOG.json").Length
        Write-Host "💊 **HEALTH LOG**: $healthSize bytes" -ForegroundColor White
    }
}

function Start-TaqwinNow {
    Write-TaqwinLog "Starting TAQWIN Tower background service immediately..."
    
    try {
        $process = Start-Process -FilePath "python" -ArgumentList "`"$ServiceScript`"" -WorkingDirectory $PythonSystemsPath -WindowStyle Hidden -PassThru
        Write-TaqwinLog "✅ TAQWIN Tower started with PID: $($process.Id)"
        Write-Host "🚀 **TAQWIN TOWER STARTED SUCCESSFULLY**" -ForegroundColor Green
        Write-Host "📊 Process ID: $($process.Id)" -ForegroundColor White
        Write-Host "🏢 Running invisibly in background" -ForegroundColor Cyan
        
    } catch {
        Write-TaqwinLog "❌ Failed to start TAQWIN Tower: $($_.Exception.Message)"
        Write-Host "❌ **FAILED TO START TAQWIN TOWER**" -ForegroundColor Red
    }
}

# Main execution
Show-TaqwinBanner

# Ensure log directory exists
$logDir = Split-Path $LogPath -Parent
if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

if ($Install) {
    if (Install-TaqwinAutostart) {
        Write-Host "🎉 **INSTALLATION COMPLETE**" -ForegroundColor Green
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
        Write-Host "✅ TAQWIN Tower will start automatically on boot" -ForegroundColor Green
        Write-Host "🚀 Would you like to start it now? (Y/N): " -ForegroundColor Cyan -NoNewline
        $response = Read-Host
        if ($response -match '^[Yy]') {
            Start-TaqwinNow
        }
    }
} elseif ($Uninstall) {
    if (Uninstall-TaqwinAutostart) {
        Write-Host "✅ **UNINSTALLATION COMPLETE**" -ForegroundColor Green
    }
} elseif ($Status) {
    Show-TaqwinStatus
} else {
    Write-Host "🎯 **TAQWIN TOWER AUTOSTART MANAGER**" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor White
    Write-Host "  -Install    Install autostart (requires admin)" -ForegroundColor Green
    Write-Host "  -Uninstall  Remove autostart" -ForegroundColor Red
    Write-Host "  -Status     Check current status" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\install_taqwin_autostart.ps1 -Install" -ForegroundColor Cyan
    Write-Host "  .\install_taqwin_autostart.ps1 -Status" -ForegroundColor Cyan
    Write-Host "  .\install_taqwin_autostart.ps1 -Uninstall" -ForegroundColor Cyan
}
