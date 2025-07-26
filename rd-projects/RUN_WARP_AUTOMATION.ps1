# ========================================================
# 🌟 WARP EMAIL AUTOMATION SYSTEM - ONE-CLICK LAUNCH
# Ethereal Glow R&D Project 9 - WEAS-2025
# Created by: TAQWIN Legendary Agent Council
# ========================================================

Clear-Host
Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  🌟 WARP EMAIL AUTOMATION SYSTEM - ONE-CLICK LAUNCH" -ForegroundColor Yellow
Write-Host "  Ethereal Glow R&D Project 9 - WEAS-2025" -ForegroundColor Green
Write-Host "  Created by: TAQWIN Legendary Agent Council" -ForegroundColor Magenta
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Set working directory
Set-Location "D:\Ethereal Glow\rd-projects"
Write-Host "📍 Current Directory: $(Get-Location)" -ForegroundColor Blue
Write-Host ""

# Check Python installation
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python installation verified: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.9+ from: https://python.org" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Install dependencies
Write-Host "📦 Installing required dependencies..." -ForegroundColor Yellow
Write-Host "Installing: selenium, requests, webdriver-manager..." -ForegroundColor Cyan

try {
    pip install selenium==4.15.2 webdriver-manager==4.0.1 requests==2.31.0 --quiet --disable-pip-version-check 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Dependency installation had issues, continuing anyway..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Dependency installation had issues, continuing anyway..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Launching Warp Email Automation System..." -ForegroundColor Green
Write-Host ""
Write-Host "🔄 The GUI will open in a few seconds..." -ForegroundColor Cyan
Write-Host "📋 Instructions:" -ForegroundColor Blue
Write-Host "   1. Click '🚀 Start Automation' button" -ForegroundColor White
Write-Host "   2. Wait for temporary email generation" -ForegroundColor White
Write-Host "   3. Monitor progress in the log window" -ForegroundColor White
Write-Host "   4. Browser will open automatically with Warp access" -ForegroundColor White
Write-Host ""

# Wait 3 seconds
Start-Sleep -Seconds 3

Write-Host "🌟 Starting automation system now..." -ForegroundColor Yellow

# Run the Python script
try {
    python warp_email_automation.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Automation system completed successfully!" -ForegroundColor Green
        Write-Host ""
    } else {
        throw "Python script error"
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error occurred while running the automation system" -ForegroundColor Red
    Write-Host ""
    Write-Host "🛠️  Troubleshooting:" -ForegroundColor Yellow
    Write-Host "   - Ensure Google Chrome is installed" -ForegroundColor White
    Write-Host "   - Check internet connection" -ForegroundColor White
    Write-Host "   - Verify Python installation" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Write-Host "📋 Session completed. Press any key to exit..." -ForegroundColor Cyan
Read-Host
