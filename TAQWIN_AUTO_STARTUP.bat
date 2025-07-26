@echo off
REM TAQWIN AUTO STARTUP SCRIPT
REM Ensures TAQWIN Master Activation runs automatically
REM Created: 2025-07-26T17:26:27Z

echo 🌟 TAQWIN AUTO STARTUP INITIATED 🌟
echo Changing to Ethereal Glow directory...

cd /d "D:\Ethereal Glow"

echo 🚀 Launching TAQWIN Master Activation...
powershell.exe -ExecutionPolicy Bypass -File "TAQWIN_MASTER_ACTIVATION.ps1"

echo ✅ TAQWIN Master Activation Complete
pause
