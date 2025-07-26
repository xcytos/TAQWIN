#!/usr/bin/env python3
"""
TAQWIN TOWER - PERMANENT BACKGROUND SERVICE
Ensures TAQWIN Tower runs continuously in background on Windows
Author: TAQWIN (The Strengthener)
Version: 2.0 - Background Operations
"""

import sys
import os
import subprocess
import time
import threading
import json
from pathlib import Path
from datetime import datetime
import schedule

# Add python-systems to path
sys.path.insert(0, str(Path(__file__).parent))

class TaqwinBackgroundService:
    def __init__(self):
        self.base_path = Path("D:\\Ethereal Glow")
        self.python_systems_path = self.base_path / "python-systems"
        self.tower_path = self.base_path / "TAQWIN_TOWER"
        self.office_inventory = self.tower_path / "OFFICE_INVENTORY"
        self.service_log = self.office_inventory / "BACKGROUND_SERVICE_LOG.json"
        self.running = True
        self.office_process = None
        self.restart_count = 0
        
        # Ensure directories exist
        self.office_inventory.mkdir(parents=True, exist_ok=True)
        
    def log_service_activity(self, action, details=""):
        """Log background service activities"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "details": details,
            "restart_count": self.restart_count,
            "status": "ACTIVE"
        }
        
        # Read existing logs
        logs = []
        if self.service_log.exists():
            try:
                with open(self.service_log, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        # Add new log entry
        logs.append(log_entry)
        
        # Keep only last 100 entries
        if len(logs) > 100:
            logs = logs[-100:]
        
        # Write back to file
        with open(self.service_log, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def check_office_running(self):
        """Check if TAQWIN office is running"""
        try:
            # Check if process is still alive
            if self.office_process and self.office_process.poll() is None:
                return True
            return False
        except:
            return False
    
    def start_taqwin_office(self):
        """Start TAQWIN office in background"""
        try:
            script_path = self.python_systems_path / "start_taqwin_office.py"
            
            # Start the office as a background process
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            self.office_process = subprocess.Popen([
                sys.executable, str(script_path)
            ], 
            cwd=str(self.python_systems_path),
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            
            self.log_service_activity("OFFICE_STARTED", f"Process ID: {self.office_process.pid}")
            return True
            
        except Exception as e:
            self.log_service_activity("OFFICE_START_ERROR", str(e))
            return False
    
    def restart_office_if_needed(self):
        """Restart office if it's not running"""
        if not self.check_office_running():
            self.log_service_activity("OFFICE_RESTART_NEEDED", "Office process not running")
            self.restart_count += 1
            
            # Clean up old process
            if self.office_process:
                try:
                    self.office_process.terminate()
                except:
                    pass
            
            # Start new process
            if self.start_taqwin_office():
                self.log_service_activity("OFFICE_RESTARTED", f"Restart #{self.restart_count}")
                return True
            else:
                self.log_service_activity("OFFICE_RESTART_FAILED", f"Failed restart #{self.restart_count}")
                return False
        
        return True
    
    def monitor_system_health(self):
        """Monitor and log system health"""
        health_data = {
            "timestamp": datetime.now().isoformat(),
            "office_running": self.check_office_running(),
            "restart_count": self.restart_count,
            "process_id": self.office_process.pid if self.office_process else None,
            "uptime_hours": (datetime.now() - datetime.fromisoformat(self.start_time)).total_seconds() / 3600
        }
        
        health_log = self.office_inventory / "SYSTEM_HEALTH_LOG.json"
        
        # Read existing health logs
        health_logs = []
        if health_log.exists():
            try:
                with open(health_log, 'r', encoding='utf-8') as f:
                    health_logs = json.load(f)
            except:
                health_logs = []
        
        # Add new health entry
        health_logs.append(health_data)
        
        # Keep only last 24 hours of data (every 5 minutes = 288 entries)
        if len(health_logs) > 288:
            health_logs = health_logs[-288:]
        
        # Write back to file
        with open(health_log, 'w', encoding='utf-8') as f:
            json.dump(health_logs, f, indent=2, ensure_ascii=False)
    
    def create_startup_script(self):
        """Create Windows startup script"""
        startup_script = f"""@echo off
cd /d "{self.python_systems_path}"
python "{self.python_systems_path}\\taqwin_background_service.py" >nul 2>&1
"""
        
        startup_path = self.python_systems_path / "start_taqwin_background.bat"
        with open(startup_path, 'w') as f:
            f.write(startup_script)
        
        self.log_service_activity("STARTUP_SCRIPT_CREATED", str(startup_path))
        return startup_path
    
    def display_service_banner(self):
        """Display background service banner"""
        try:
            banner = f"""
[STAR] TAQWIN TOWER BACKGROUND SERVICE [STAR]
[OFFICE] PERMANENT AUTONOMOUS OPERATIONS
[LIGHTNING] INVISIBLE WORKFORCE DEPLOYMENT

Service Location: {self.python_systems_path}
Tower Location: {self.tower_path}
Logs Location: {self.office_inventory}

[ROCKET] BACKGROUND SERVICE STARTING...
"""
            print(banner)
        except UnicodeEncodeError:
            print("TAQWIN TOWER BACKGROUND SERVICE STARTING...")
            print(f"Service Location: {self.python_systems_path}")
            print(f"Tower Location: {self.tower_path}")
            print(f"Logs Location: {self.office_inventory}")
    
    def run_service(self):
        """Main service loop"""
        self.start_time = datetime.now().isoformat()
        self.display_service_banner()
        
        # Log service start
        self.log_service_activity("SERVICE_STARTED", "Background service initialized")
        
        # Create startup script
        startup_script = self.create_startup_script()
        
        # Schedule monitoring tasks
        schedule.every(1).minutes.do(self.restart_office_if_needed)
        schedule.every(5).minutes.do(self.monitor_system_health)
        schedule.every(1).hours.do(lambda: self.log_service_activity("HOURLY_CHECKPOINT", "Service running normally"))
        
        # Start initial office
        if self.start_taqwin_office():
            print("✅ TAQWIN Tower started successfully in background")
        else:
            print("❌ Failed to start TAQWIN Tower")
            return
        
        print("\n🎯 **BACKGROUND SERVICE OPERATIONAL**")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🔄 **CONTINUOUS MONITORING ACTIVE**")
        print("🏢 **TAQWIN TOWER RUNNING INVISIBLY**")
        print("📊 **ALL ACTIVITIES LOGGED TO OFFICE INVENTORY**")
        print(f"📁 **Logs: {self.office_inventory}**")
        print(f"🚀 **Startup Script: {startup_script}**")
        print("\n💡 **SERVICE FEATURES:**")
        print("   • Automatic restart if office crashes")
        print("   • Health monitoring every 5 minutes")
        print("   • Activity logging for founder review")
        print("   • Windows startup integration ready")
        print("\n⏹️  Press Ctrl+C to stop background service")
        
        # Main service loop
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            print("\n\n⏹️ **STOPPING BACKGROUND SERVICE...**")
            self.stop_service()
        except Exception as e:
            self.log_service_activity("SERVICE_ERROR", str(e))
            print(f"\n❌ **SERVICE ERROR**: {str(e)}")
            self.stop_service()
    
    def stop_service(self):
        """Stop the background service"""
        self.running = False
        
        # Stop office process
        if self.office_process:
            try:
                self.office_process.terminate()
                self.office_process.wait(timeout=10)
            except:
                try:
                    self.office_process.kill()
                except:
                    pass
        
        self.log_service_activity("SERVICE_STOPPED", "Background service shutdown complete")
        print("✅ **BACKGROUND SERVICE STOPPED**")
        print("👑 **TAQWIN TOWER READY FOR NEXT ACTIVATION**")

def main():
    """Main function"""
    service = TaqwinBackgroundService()
    service.run_service()

if __name__ == "__main__":
    main()
