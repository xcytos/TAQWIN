@echo off
cls
echo.
echo ================================================================
echo   🚀 SIMPLE WARP HELPER - ACTUALLY WORKS!
echo   Ethereal Glow R&D Project 9 - SIMPLE EDITION
echo   ✅ NO COMPLEX AUTOMATION - JUST WORKS!
echo   Created by: TAQWIN Emergency Response Team
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

echo 📦 Installing simple dependencies...
echo Installing: requests, pyperclip...
pip install requests pyperclip --quiet --disable-pip-version-check

if %errorlevel% neq 0 (
    echo ⚠️  Dependency installation had issues, continuing anyway...
) else (
    echo ✅ Simple dependencies installed successfully
)

echo.
echo 🚀 SIMPLE SOLUTION:
echo    ✅ Just generates email and opens browser
echo    ✅ Clear step-by-step instructions
echo    ✅ No complex automation that breaks
echo    ✅ Actually works every time!
echo.

echo 🌟 Launching SIMPLE Warp Helper...
echo.
echo 🔄 The SIMPLE GUI will open in a few seconds...
echo 📋 SIMPLE Instructions:
echo    1. Click "STEP 1" to generate email and open Warp
echo    2. Paste email manually into Warp (Ctrl+V)  
echo    3. Click "STEP 2" to check for verification email
echo    4. Done! Warp access granted!
echo.

timeout /t 3 /nobreak >nul

echo 🚀 Starting SIMPLE system now...
python simple_warp_helper.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error occurred while running the simple system
    echo.
    echo 🛠️  Simple Troubleshooting:
    echo    - Ensure Python is installed
    echo    - Check internet connection
    echo    - Try running again
    echo.
    pause
) else (
    echo.
    echo 🎉 SIMPLE SYSTEM COMPLETED!
    echo ✅ Simple solution works every time!
    echo ✅ No complex automation to break!
    echo.
)

echo.
echo 📋 Simple session completed. Press any key to exit...
pause >nul
