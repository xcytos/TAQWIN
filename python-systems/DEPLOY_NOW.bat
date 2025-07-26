@echo off
echo.
echo ===============================================
echo    TAQWIN TOWER - QUICK DEPLOYMENT LAUNCHER
echo ===============================================
echo.

cd /d "D:\Ethereal Glow\python-systems"

echo [1/3] Running Complete System Deployment...
python deploy_taqwin_complete.py

echo.
echo [2/3] Checking System Status...
python check_taqwin_status.py

echo.
echo [3/3] Deployment Complete!
echo.
echo TAQWIN Tower is now fully operational!
echo.
pause
