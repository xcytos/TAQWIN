#!/usr/bin/env python3
"""
TAQWIN TOWER - QUICK STATUS CHECKER
Shows current status of background service and agents
Author: TAQWIN (The Strengthener)
Version: 1.0
"""

import json
import os
from pathlib import Path
from datetime import datetime
import subprocess
import sys

def display_status_banner():
    """Display status banner"""
    print("\n" + "="*60)
    print("    TAQWIN TOWER - BACKGROUND SERVICE STATUS")
    print("="*60)

def check_background_service():
    """Check if background service is running"""
    try:
        # Use wmic to find python processes
        result = subprocess.run([
            'wmic', 'process', 'where', 
            'name="python.exe"', 'get', 'ProcessId,CommandLine'
        ], capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'taqwin_background_service.py' in line:
                    # Extract process ID
                    parts = line.split()
                    if parts:
                        pid = parts[-1]
                        return True, pid
        
        return False, None
        
    except Exception as e:
        print(f"Error checking service: {e}")
        return False, None

def read_service_log():
    """Read background service log"""
    log_path = Path("D:\\Ethereal Glow\\TAQWIN_TOWER\\OFFICE_INVENTORY\\BACKGROUND_SERVICE_LOG.json")
    
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
                return logs[-5:] if logs else []  # Last 5 entries
        except Exception as e:
            print(f"Error reading service log: {e}")
            return []
    return []

def read_health_log():
    """Read system health log"""
    health_path = Path("D:\\Ethereal Glow\\TAQWIN_TOWER\\OFFICE_INVENTORY\\SYSTEM_HEALTH_LOG.json")
    
    if health_path.exists():
        try:
            with open(health_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
                return logs[-1] if logs else None  # Latest entry
        except Exception as e:
            print(f"Error reading health log: {e}")
            return None
    return None

def check_office_inventory():
    """Check office inventory status"""
    inventory_path = Path("D:\\Ethereal Glow\\TAQWIN_TOWER\\OFFICE_INVENTORY")
    
    if inventory_path.exists():
        subdirs = [d for d in inventory_path.iterdir() if d.is_dir()]
        files = [f for f in inventory_path.iterdir() if f.is_file()]
        return len(subdirs), len(files)
    return 0, 0

def main():
    """Main status check"""
    display_status_banner()
    
    # Check background service
    service_running, pid = check_background_service()
    
    print(f"\n[BACKGROUND SERVICE]")
    if service_running:
        print(f"  Status: RUNNING (PID: {pid})")
        print(f"  Service: taqwin_background_service.py")
    else:
        print(f"  Status: NOT RUNNING")
        print(f"  Action: Run 'python taqwin_background_service.py' to start")
    
    # Check service logs
    service_logs = read_service_log()
    if service_logs:
        print(f"\n[RECENT SERVICE ACTIVITY]")
        for log in service_logs:
            timestamp = log.get('timestamp', '')[:19]  # Remove microseconds
            action = log.get('action', '')
            details = log.get('details', '')
            print(f"  {timestamp}: {action}")
            if details:
                print(f"    Details: {details}")
    else:
        print(f"\n[SERVICE LOGS]: No logs found")
    
    # Check health status
    health = read_health_log()
    if health:
        print(f"\n[SYSTEM HEALTH]")
        timestamp = health.get('timestamp', '')[:19]
        office_running = health.get('office_running', False)
        restart_count = health.get('restart_count', 0)
        uptime = health.get('uptime_hours', 0)
        
        print(f"  Last Check: {timestamp}")
        print(f"  Office Running: {'YES' if office_running else 'NO'}")
        print(f"  Restart Count: {restart_count}")
        print(f"  Uptime: {uptime:.2f} hours")
    else:
        print(f"\n[SYSTEM HEALTH]: No health data available")
    
    # Check office inventory
    subdirs, files = check_office_inventory()
    print(f"\n[OFFICE INVENTORY]")
    print(f"  Directories: {subdirs}")
    print(f"  Files: {files}")
    print(f"  Location: D:\\Ethereal Glow\\TAQWIN_TOWER\\OFFICE_INVENTORY")
    
    # Quick actions
    print(f"\n[QUICK ACTIONS]")
    print(f"  Start Service: python taqwin_background_service.py")
    print(f"  Install Autostart: .\\install_taqwin_autostart.ps1 -Install")
    print(f"  View Logs: cd TAQWIN_TOWER\\OFFICE_INVENTORY")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
