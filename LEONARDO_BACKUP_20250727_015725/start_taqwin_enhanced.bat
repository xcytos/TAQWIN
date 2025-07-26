@echo off
REM TAQWIN Enhanced Background Service V3.0
REM Alan Turing's Production Stability System

cd /d "D:\Ethereal Glow\python-systems"
echo Starting TAQWIN Enhanced Background Service...
python "D:\Ethereal Glow\python-systems\taqwin_background_service_v3.py" >nul 2>&1

REM Fallback to V2 if V3 fails
if errorlevel 1 (
    echo V3 failed, starting V2 fallback...
    python "D:\Ethereal Glow\python-systems\taqwin_background_service.py" >nul 2>&1
)
