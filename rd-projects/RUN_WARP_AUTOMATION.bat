@echo off
cls
echo.
echo ========================================================
echo   🌟 WARP EMAIL AUTOMATION SYSTEM - ONE-CLICK LAUNCH
echo   Ethereal Glow R&D Project 9 - WEAS-2025
echo   Created by: TAQWIN Legendary Agent Council
echo ========================================================
echo.

cd /d "D:\Ethereal Glow\rd-projects"

echo 📍 Current Directory: %CD%
echo.

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.9+ from: https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python installation verified
echo.

echo 📦 Installing required dependencies...
echo Installing: selenium, requests, webdriver-manager, pyperclip...
pip install selenium==4.15.2 webdriver-manager==4.0.1 requests==2.31.0 pyperclip==1.8.2 --quiet --disable-pip-version-check

if %errorlevel% neq 0 (
    echo ⚠️  Dependency installation had issues, continuing anyway...
) else (
    echo ✅ Dependencies installed successfully
)

echo.
echo 🚀 Launching Warp Email Automation System...
echo.
echo 🔄 The GUI will open in a few seconds...
echo 📋 Instructions:
echo    1. Click "🚀 Start Automation" button
echo    2. Wait for temporary email generation
echo    3. Monitor progress in the log window
echo    4. Browser will open automatically with Warp access
echo.

timeout /t 3 /nobreak >nul

echo 🌟 Starting automation system now...
python warp_email_automation.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error occurred while running the automation system
    echo.
    echo 🛠️  Troubleshooting:
    echo    - Ensure Google Chrome is installed
    echo    - Check internet connection
    echo    - Verify Python installation
    echo.
    pause
) else (
    echo.
    echo ✅ Automation system completed successfully!
    echo.
)

echo.
echo 📋 Session completed. Press any key to exit...
pause >nul
