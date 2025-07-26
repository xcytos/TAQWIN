@echo off
cls
echo.
echo ================================================================
echo   🌟 ENHANCED WARP EMAIL AUTOMATION - ONE-CLICK COMPLETE LAUNCH
echo   Ethereal Glow R&D Project 9 - WEAS-2025-ENHANCED
echo   🔥 Clipboard Integration + Incognito Mode + Complete Automation
echo   Created by: TAQWIN Legendary Agent Council
echo ================================================================
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

echo 📦 Installing enhanced dependencies...
echo Installing: selenium, requests, webdriver-manager, pyperclip...
pip install selenium==4.15.2 webdriver-manager==4.0.1 requests==2.31.0 pyperclip==1.8.2 --quiet --disable-pip-version-check

if %errorlevel% neq 0 (
    echo ⚠️  Dependency installation had issues, continuing anyway...
) else (
    echo ✅ Enhanced dependencies installed successfully
)

echo.
echo 🔥 ENHANCED FEATURES:
echo    ✨ Automatic clipboard integration for email and links
echo    🕵️ Incognito browser mode for enhanced privacy
echo    🚀 Complete end-to-end automation workflow
echo    📧 Advanced temporary email generation
echo    🔗 Smart verification link extraction
echo    🖥️ Browser stays open for immediate access
echo.

echo 🌟 Launching Enhanced Warp Email Automation System...
echo.
echo 🔄 The Enhanced GUI will open in a few seconds...
echo 📋 Enhanced Instructions:
echo    1. Click "🚀 START COMPLETE AUTOMATION" button
echo    2. Email will be auto-generated and copied to clipboard
echo    3. Incognito browser will open automatically
echo    4. Email will be auto-pasted and submitted
echo    5. System monitors inbox automatically
echo    6. Verification link auto-copied to clipboard
echo    7. Verification processed automatically
echo    8. Warp access granted with browser staying open
echo.

timeout /t 5 /nobreak >nul

echo 🔥 Starting ENHANCED automation system now...
python warp_automation_enhanced.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error occurred while running the enhanced automation system
    echo.
    echo 🛠️  Enhanced Troubleshooting:
    echo    - Ensure Google Chrome is installed and updated
    echo    - Check internet connection stability
    echo    - Verify Python 3.9+ installation
    echo    - Check if pyperclip clipboard access is working
    echo    - Ensure no antivirus blocking browser automation
    echo.
    pause
) else (
    echo.
    echo 🎉 ENHANCED AUTOMATION COMPLETED SUCCESSFULLY!
    echo ✅ Email generated and copied to clipboard
    echo ✅ Verification link copied to clipboard  
    echo ✅ Warp access granted in incognito browser
    echo ✅ Ready for immediate use!
    echo.
)

echo.
echo 📋 Enhanced session completed. Press any key to exit...
pause >nul
