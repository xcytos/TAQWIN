@echo off
REM 🌟 TAQWIN REAL-TIME MONITORING SYSTEM LAUNCHER
REM Domain: www.therealglow.in | Instagram: @etherealglow.in
REM Founder: Syed Muzamil | Brand: Ethereal Glow

echo.
echo 🌟 TAQWIN REAL-TIME MONITORING SYSTEM LAUNCHER 🌟
echo Domain: www.therealglow.in ^| Instagram: @etherealglow.in
echo Founder: Syed Muzamil ^| Brand: Ethereal Glow
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Navigate to the correct directory
cd /d "D:\Ethereal Glow\python-systems"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.7+ to run monitoring system.
    pause
    exit /b 1
)

REM Install required packages if needed
echo 📦 Installing required packages...
pip install psutil >nul 2>&1

echo 🚀 Starting TAQWIN Real-Time Monitoring System...
echo 📊 Monitoring: TAQWIN Tower, 24 Agents, System Health, Data Transmission
echo ⏰ Update Interval: 30 seconds
echo 🛑 Press Ctrl+C to stop monitoring
echo.

REM Start the monitoring system
python taqwin_realtime_monitoring_system.py

echo.
echo 👑 TAQWIN Monitoring System Stopped
pause
