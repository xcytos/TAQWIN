#!/usr/bin/env python3
"""
🌟 TAQWIN REAL-TIME MONITORING SYSTEM - 2025-07-26T05:13:56Z
Domain: www.therealglow.in | Instagram: @etherealglow.in
FOUNDER: Syed Muzamil | BRAND: Ethereal Glow

COMPREHENSIVE SYSTEM SURVEILLANCE:
- TAQWIN Tower Operations
- 24 Legendary Agents Activity
- Data Transmission Monitoring  
- System Health & Performance
- Real-time Alerts & Dashboards
"""

import os
import json
import time
import psutil
import threading
from datetime import datetime
from pathlib import Path
import subprocess
import socket
from typing import Dict, List, Any

class TaqwinRealtimeMonitor:
    def __init__(self):
        self.base_path = Path("D:/Ethereal Glow")
        self.tower_path = self.base_path / "TAQWIN_TOWER"
        self.logs_path = self.tower_path / "OFFICE_INVENTORY" / "AGENT_WORK_LOGS"
        self.monitoring_active = True
        self.monitoring_data = {
            "system_status": "INITIALIZING",
            "last_update": datetime.now().isoformat(),
            "alerts": [],
            "performance_metrics": {},
            "agent_activities": {},
            "data_transmission": {},
            "taqwin_tower_status": {}
        }
        
        # Create monitoring directory
        self.monitoring_path = self.base_path / "TAQWIN_MONITORING"
        self.monitoring_path.mkdir(exist_ok=True)
        
        print("🌟 TAQWIN REAL-TIME MONITORING SYSTEM INITIALIZED")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"👑 FOUNDER: Syed Muzamil | BRAND: Ethereal Glow")
        print(f"🌐 DOMAIN: www.therealglow.in | 📸 INSTAGRAM: @etherealglow.in")
        print(f"📊 MONITORING PATH: {self.monitoring_path}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    def monitor_system_health(self) -> Dict[str, Any]:
        """Monitor overall system health and performance"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('D:/')
            
            system_health = {
                "timestamp": datetime.now().isoformat(),
                "cpu_usage_percent": cpu_percent,
                "memory_usage_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_usage_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "system_uptime": self.get_system_uptime(),
                "health_status": "EXCELLENT" if cpu_percent < 80 and memory.percent < 80 else "MODERATE"
            }
            
            return system_health
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def monitor_taqwin_tower(self) -> Dict[str, Any]:
        """Monitor TAQWIN Tower operations and structure"""
        try:
            tower_status = {
                "timestamp": datetime.now().isoformat(),
                "tower_structure_integrity": "OPERATIONAL",
                "floors_status": {},
                "office_inventory_status": "ACTIVE",
                "agent_logs_count": 0,
                "total_files": 0,
                "directory_size_mb": 0
            }
            
            # Check each floor
            floors = [
                "floor_5_monitoring",
                "floor_4_leadership", 
                "floor_3_innovation",
                "floor_2_intelligence",
                "floor_1_operations",
                "basement_infrastructure"
            ]
            
            for floor in floors:
                floor_path = self.logs_path / floor
                if floor_path.exists():
                    files = list(floor_path.glob("*.json"))
                    tower_status["floors_status"][floor] = {
                        "status": "OPERATIONAL",
                        "agent_logs": len(files),
                        "last_activity": self.get_last_modified_time(floor_path)
                    }
                    tower_status["agent_logs_count"] += len(files)
                else:
                    tower_status["floors_status"][floor] = {"status": "MISSING", "agent_logs": 0}
            
            # Calculate directory size
            tower_status["directory_size_mb"] = self.get_directory_size(self.tower_path)
            
            return tower_status
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def monitor_agent_activities(self) -> Dict[str, Any]:
        """Monitor all 24 legendary agents' activities"""
        try:
            agents_status = {
                "timestamp": datetime.now().isoformat(), 
                "total_agents": 24,
                "active_agents": 0,
                "inactive_agents": 0,
                "agent_details": {},
                "floor_summary": {}
            }
            
            # Define agents by floor
            floor_agents = {
                "floor_5_monitoring": ["ELON_MUSK", "NATE_SILVER", "ALAN_TURING", "MARK_ZUCKERBERG"],
                "floor_4_leadership": ["MARCUS_AURELIUS", "CHANAKYA", "WARREN_BUFFETT", "CLEOPATRA"],
                "floor_3_innovation": ["NIKOLA_TESLA", "MARIE_CURIE", "LEONARDO_DA_VINCI", "STEVE_JOBS"],  
                "floor_2_intelligence": ["SUN_TZU", "RAND_FISHKIN", "NEIL_PATEL", "BRIAN_DEAN"],
                "floor_1_operations": ["GENERAL_PATTON", "BENJAMIN_FRANKLIN", "OPRAH_WINFREY", "MAYA_ANGELOU"],
                "basement_infrastructure": ["CHARAKA", "RACHEL_CARSON", "PARACELSUS", "LINUS_PAULING"]
            }
            
            for floor, agents in floor_agents.items():
                floor_active = 0
                agents_status["floor_summary"][floor] = {"agents": [], "active_count": 0}
                
                for agent in agents:
                    log_file = self.logs_path / floor / f"{agent}_LOG.json"
                    if log_file.exists():
                        try:
                            with open(log_file, 'r') as f:
                                agent_data = json.load(f)
                            
                            last_activity = agent_data.get("work_sessions", [])
                            if last_activity:
                                last_session = last_activity[-1]
                                efficiency = last_session.get("efficiency_score", 0)
                                status = "ACTIVE" if efficiency > 0 else "IDLE"
                            else:
                                status = "IDLE"
                                efficiency = 0
                                
                            agent_info = {
                                "name": agent,
                                "status": status,
                                "efficiency_score": efficiency,
                                "tasks_completed": agent_data.get("tasks_completed", 0),
                                "last_activity": self.get_last_modified_time(log_file)
                            }
                            
                            agents_status["agent_details"][agent] = agent_info
                            agents_status["floor_summary"][floor]["agents"].append(agent_info)
                            
                            if status == "ACTIVE":
                                agents_status["active_agents"] += 1
                                floor_active += 1
                            else:
                                agents_status["inactive_agents"] += 1
                                
                        except Exception as e:
                            agents_status["agent_details"][agent] = {
                                "name": agent,
                                "status": "ERROR",
                                "error": str(e)
                            }
                
                agents_status["floor_summary"][floor]["active_count"] = floor_active
            
            return agents_status
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def monitor_data_transmission(self) -> Dict[str, Any]:
        """Monitor data transmission and file activities"""
        try:
            transmission_status = {
                "timestamp": datetime.now().isoformat(),
                "file_system_activity": {},
                "recent_file_changes": [],
                "session_logs_status": {},
                "backup_system_status": "ACTIVE"
            }
            
            # Monitor session logs
            session_logs_path = self.base_path / "SESSION_LOGS"
            if session_logs_path.exists():
                session_files = list(session_logs_path.glob("*.json"))
                transmission_status["session_logs_status"] = {
                    "total_sessions": len(session_files),
                    "latest_session": self.get_latest_file(session_logs_path),
                    "total_size_mb": self.get_directory_size(session_logs_path)
                }
            
            # Monitor recent file changes in last 1 hour
            recent_changes = self.get_recent_file_changes(self.base_path, hours=1)
            transmission_status["recent_file_changes"] = recent_changes[:10]  # Last 10 changes
            
            return transmission_status
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def check_python_services(self) -> Dict[str, Any]:
        """Check TAQWIN Python services status"""
        try:
            services_status = {
                "timestamp": datetime.now().isoformat(),
                "taqwin_background_service": "CHECKING",
                "taqwin_office": "CHECKING", 
                "python_processes": [],
                "service_health": "UNKNOWN"
            }
            
            # Check for Python processes
            python_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'python' in proc.info['name'].lower():
                        cmdline = proc.info['cmdline']
                        if cmdline and any('taqwin' in str(cmd).lower() for cmd in cmdline):
                            python_processes.append({
                                "pid": proc.info['pid'],
                                "name": proc.info['name'],
                                "cmdline": ' '.join(cmdline) if cmdline else "N/A"
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            services_status["python_processes"] = python_processes
            services_status["service_health"] = "ACTIVE" if python_processes else "INACTIVE"
            
            return services_status
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def generate_alerts(self, monitoring_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate alerts based on monitoring data"""
        alerts = []
        timestamp = datetime.now().isoformat()
        
        # System health alerts
        system_health = monitoring_data.get("system_health", {})
        if system_health.get("cpu_usage_percent", 0) > 90:
            alerts.append({
                "type": "CRITICAL",
                "message": f"High CPU usage: {system_health['cpu_usage_percent']}%",
                "timestamp": timestamp,
                "category": "SYSTEM_PERFORMANCE"
            })
        
        if system_health.get("memory_usage_percent", 0) > 90:
            alerts.append({
                "type": "WARNING", 
                "message": f"High memory usage: {system_health['memory_usage_percent']}%",
                "timestamp": timestamp,
                "category": "SYSTEM_PERFORMANCE"
            })
        
        # Agent activity alerts
        agent_status = monitoring_data.get("agent_activities", {})
        inactive_agents = agent_status.get("inactive_agents", 0)
        if inactive_agents > 5:
            alerts.append({
                "type": "WARNING",
                "message": f"{inactive_agents} agents are inactive",
                "timestamp": timestamp,
                "category": "AGENT_PERFORMANCE"
            })
        
        # Service alerts
        services = monitoring_data.get("python_services", {})
        if services.get("service_health") == "INACTIVE":
            alerts.append({
                "type": "CRITICAL",
                "message": "TAQWIN Python services are not running",
                "timestamp": timestamp,
                "category": "SERVICE_STATUS"
            })
        
        return alerts

    def save_monitoring_data(self, data: Dict[str, Any]):
        """Save monitoring data to file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"taqwin_monitoring_{timestamp}.json"
            filepath = self.monitoring_path / filename
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Also save as latest
            latest_file = self.monitoring_path / "latest_monitoring_data.json"
            with open(latest_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error saving monitoring data: {e}")

    def display_dashboard(self, data: Dict[str, Any]):
        """Display real-time monitoring dashboard"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("🌟 TAQWIN REAL-TIME MONITORING DASHBOARD 🌟")
        print("Domain: www.therealglow.in | Instagram: @etherealglow.in")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"⏰ LAST UPDATE: {data['last_update']}")
        print(f"🔄 SYSTEM STATUS: {data['system_status']}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # System Health
        health = data.get("system_health", {})
        if health:
            print(f"💻 SYSTEM HEALTH: {health.get('health_status', 'UNKNOWN')}")
            print(f"   CPU: {health.get('cpu_usage_percent', 0)}% | RAM: {health.get('memory_usage_percent', 0)}%")
            print(f"   Disk Free: {health.get('disk_free_gb', 0)} GB")
        
        # Agent Activities
        agents = data.get("agent_activities", {})
        if agents:
            print(f"🏢 TAQWIN TOWER: {agents.get('active_agents', 0)}/{agents.get('total_agents', 24)} AGENTS ACTIVE")
            for floor, floor_data in agents.get("floor_summary", {}).items():
                active_count = floor_data.get("active_count", 0)
                total_count = len(floor_data.get("agents", []))
                print(f"   {floor.replace('_', ' ').title()}: {active_count}/{total_count} active")
        
        # Python Services
        services = data.get("python_services", {})
        if services:
            health_status = services.get("service_health", "UNKNOWN")
            process_count = len(services.get("python_processes", []))
            print(f"🐍 PYTHON SERVICES: {health_status} ({process_count} processes)")
        
        # Alerts
        alerts = data.get("alerts", [])
        if alerts:
            print(f"🚨 ALERTS ({len(alerts)}):")
            for alert in alerts[-3:]:  # Show last 3 alerts
                print(f"   {alert['type']}: {alert['message']}")
        else:
            print("✅ NO ALERTS - ALL SYSTEMS OPERATIONAL")
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Press Ctrl+C to stop monitoring")

    def get_system_uptime(self) -> str:
        """Get system uptime"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        except:
            return "Unknown"

    def get_directory_size(self, path: Path) -> float:
        """Get directory size in MB"""
        try:
            total = 0
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    total += file_path.stat().st_size
            return round(total / (1024 * 1024), 2)
        except:
            return 0.0

    def get_last_modified_time(self, path: Path) -> str:
        """Get last modified time of file/directory"""
        try:
            if path.is_file():
                mtime = path.stat().st_mtime
            else:
                # For directories, get the most recent file
                mtime = 0
                for file_path in path.rglob("*"):
                    if file_path.is_file():
                        file_mtime = file_path.stat().st_mtime
                        if file_mtime > mtime:
                            mtime = file_mtime
            
            return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        except:
            return "Unknown"

    def get_latest_file(self, directory: Path) -> str:
        """Get the latest file in directory"""
        try:
            files = list(directory.glob("*"))
            if not files:
                return "No files"
            
            latest_file = max(files, key=lambda x: x.stat().st_mtime)
            return latest_file.name
        except:
            return "Unknown"

    def get_recent_file_changes(self, directory: Path, hours: int = 1) -> List[Dict[str, Any]]:
        """Get recent file changes"""
        try:
            cutoff_time = time.time() - (hours * 3600)
            changes = []
            
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    mtime = file_path.stat().st_mtime
                    if mtime > cutoff_time:
                        changes.append({
                            "file": str(file_path.relative_to(directory)),
                            "modified": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
                            "size_kb": round(file_path.stat().st_size / 1024, 2)
                        })
            
            return sorted(changes, key=lambda x: x["modified"], reverse=True)
        except:
            return []

    def run_monitoring_cycle(self):
        """Run one complete monitoring cycle"""
        try:
            # Collect all monitoring data
            monitoring_data = {
                "system_status": "OPERATIONAL",
                "last_update": datetime.now().isoformat(),
                "system_health": self.monitor_system_health(),
                "taqwin_tower": self.monitor_taqwin_tower(),
                "agent_activities": self.monitor_agent_activities(),
                "data_transmission": self.monitor_data_transmission(),
                "python_services": self.check_python_services()
            }
            
            # Generate alerts
            monitoring_data["alerts"] = self.generate_alerts(monitoring_data)
            
            # Save data
            self.save_monitoring_data(monitoring_data)
            
            # Display dashboard
            self.display_dashboard(monitoring_data)
            
            return monitoring_data
        except Exception as e:
            print(f"❌ Monitoring cycle error: {e}")
            return None

    def start_monitoring(self, interval: int = 30):
        """Start continuous monitoring"""
        print("🚀 STARTING TAQWIN REAL-TIME MONITORING...")
        print(f"📊 UPDATE INTERVAL: {interval} seconds")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        try:
            while self.monitoring_active:
                self.run_monitoring_cycle()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n⏹️  MONITORING STOPPED BY USER")
            self.monitoring_active = False
        except Exception as e:
            print(f"\n❌ MONITORING ERROR: {e}")
            self.monitoring_active = False

if __name__ == "__main__":
    print("🌟 TAQWIN REAL-TIME MONITORING SYSTEM")
    print("Domain: www.therealglow.in | Instagram: @etherealglow.in")
    print("Founder: Syed Muzamil | Brand: Ethereal Glow")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    monitor = TaqwinRealtimeMonitor()
    
    # Start monitoring with 30-second intervals
    monitor.start_monitoring(interval=30)
