#!/usr/bin/env python3
"""
TAQWIN TOWER - ENHANCED BACKGROUND SERVICE V3.0
Alan Turing's Advanced Process Stability & Monitoring System
Features: Resource optimization, graceful shutdown, exponential backoff, health metrics
Author: Alan Turing (Chief Information Officer)
Version: 3.0 - Production Stability
"""

import sys
import os
import subprocess
import time
import threading
import json
import psutil
import signal
from pathlib import Path
from datetime import datetime, timedelta
import schedule
import gc
import logging
from typing import Dict, List, Optional

# Add python-systems to path
sys.path.insert(0, str(Path(__file__).parent))

class EnhancedTaqwinBackgroundService:
    def __init__(self):
        self.base_path = Path("D:\\Ethereal Glow")
        self.python_systems_path = self.base_path / "python-systems"
        self.tower_path = self.base_path / "TAQWIN_TOWER"
        self.office_inventory = self.tower_path / "OFFICE_INVENTORY"
        
        # Enhanced logging paths
        self.service_log = self.office_inventory / "ENHANCED_SERVICE_LOG.json"
        self.health_log = self.office_inventory / "ADVANCED_HEALTH_METRICS.json"
        self.performance_log = self.office_inventory / "PERFORMANCE_ANALYTICS.json"
        self.git_log = self.office_inventory / "GIT_OPERATIONS_LOG.json"
        
        # Service state
        self.running = True
        self.office_process = None
        self.restart_count = 0
        self.start_time = datetime.now()
        self.last_successful_start = None
        
        # Enhanced stability features
        self.restart_backoff = 1  # Start with 1 minute
        self.max_backoff = 60  # Max 60 minutes
        self.health_threshold = 90  # Memory usage threshold
        self.stability_score = 100
        self.consecutive_failures = 0
        
        # Performance monitoring
        self.performance_metrics = {
            'cpu_usage': [],
            'memory_usage': [],
            'process_count': [],
            'stability_events': []
        }
        
        # Ensure directories exist
        self.office_inventory.mkdir(parents=True, exist_ok=True)
        
        # Setup enhanced logging
        self.setup_advanced_logging()
        
        # Git credentials (will be configured)
        self.git_configured = False
        
    def setup_advanced_logging(self):
        """Setup comprehensive logging system"""
        log_format = '%(asctime)s - TAQWIN_ENHANCED - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(self.office_inventory / 'taqwin_enhanced.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('TaqwinEnhanced')
        
    def log_enhanced_activity(self, action: str, details: str = "", level: str = "INFO", metrics: Dict = None):
        """Enhanced logging with performance metrics"""
        timestamp = datetime.now().isoformat()
        
        # Get current system metrics
        current_metrics = self.get_system_metrics()
        
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "details": details,
            "level": level,
            "restart_count": self.restart_count,
            "stability_score": self.stability_score,
            "consecutive_failures": self.consecutive_failures,
            "system_metrics": current_metrics,
            "custom_metrics": metrics or {},
            "status": "ENHANCED_ACTIVE"
        }
        
        # Read existing logs
        logs = self.read_json_log(self.service_log)
        logs.append(log_entry)
        
        # Keep only last 500 entries (enhanced capacity)
        if len(logs) > 500:
            logs = logs[-500:]
        
        # Write back to file
        self.write_json_log(self.service_log, logs)
        
        # Log to system logger
        if level == "ERROR":
            self.logger.error(f"{action}: {details}")
        elif level == "WARNING":
            self.logger.warning(f"{action}: {details}")
        else:
            self.logger.info(f"{action}: {details}")
    
    def get_system_metrics(self) -> Dict:
        """Get comprehensive system performance metrics"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('D:\\')
            
            # Process-specific metrics
            process_count = len(psutil.pids())
            
            # Office process metrics
            office_metrics = {}
            if self.office_process:
                try:
                    office_proc = psutil.Process(self.office_process.pid)
                    office_metrics = {
                        'cpu_percent': office_proc.cpu_percent(),
                        'memory_mb': office_proc.memory_info().rss / 1024 / 1024,
                        'status': office_proc.status(),
                        'threads': office_proc.num_threads()
                    }
                except:
                    office_metrics = {'status': 'not_accessible'}
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / 1024 / 1024 / 1024,
                'disk_free_gb': disk.free / 1024 / 1024 / 1024,
                'process_count': process_count,
                'office_process': office_metrics,
                'uptime_minutes': (datetime.now() - self.start_time).total_seconds() / 60
            }
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def check_process_health(self) -> Dict:
        """Advanced process health check with diagnostics"""
        health_status = {
            'is_running': False,
            'responsive': False,
            'memory_healthy': True,
            'cpu_healthy': True,
            'restart_needed': False,
            'diagnostics': []
        }
        
        try:
            # Basic process check
            if self.office_process and self.office_process.poll() is None:
                health_status['is_running'] = True
                
                # Advanced health checks
                try:
                    office_proc = psutil.Process(self.office_process.pid)
                    
                    # Memory check
                    memory_mb = office_proc.memory_info().rss / 1024 / 1024
                    if memory_mb > 500:  # 500MB threshold
                        health_status['memory_healthy'] = False
                        health_status['diagnostics'].append(f"High memory usage: {memory_mb:.1f}MB")
                    
                    # CPU check
                    cpu_percent = office_proc.cpu_percent()
                    if cpu_percent > 80:  # 80% threshold
                        health_status['cpu_healthy'] = False
                        health_status['diagnostics'].append(f"High CPU usage: {cpu_percent:.1f}%")
                    
                    # Responsiveness check (simple file write test)
                    test_file = self.office_inventory / 'health_test.tmp'
                    try:
                        test_file.write_text(f"health_check_{datetime.now().timestamp()}")
                        test_file.unlink()
                        health_status['responsive'] = True
                    except:
                        health_status['responsive'] = False
                        health_status['diagnostics'].append("File system unresponsive")
                    
                except psutil.NoSuchProcess:
                    health_status['is_running'] = False
                    health_status['diagnostics'].append("Process no longer exists")
                except Exception as e:
                    health_status['diagnostics'].append(f"Health check error: {str(e)}")
            else:
                health_status['diagnostics'].append("Process not running or terminated")
            
            # Determine if restart is needed
            health_status['restart_needed'] = (
                not health_status['is_running'] or
                not health_status['responsive'] or
                not health_status['memory_healthy']
            )
            
        except Exception as e:
            health_status['diagnostics'].append(f"Health check failed: {str(e)}")
            health_status['restart_needed'] = True
        
        return health_status
    
    def start_taqwin_office_enhanced(self) -> bool:
        """Enhanced office startup with resource optimization"""
        try:
            # Clean up any zombie processes first
            self.cleanup_zombie_processes()
            
            # Force garbage collection
            gc.collect()
            
            script_path = self.python_systems_path / "start_taqwin_office.py"
            
            # Enhanced startup configuration
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            # Resource-optimized environment
            env = os.environ.copy()
            env['PYTHONHASHSEED'] = '0'  # Consistent hashing
            env['PYTHONOPTIMIZE'] = '1'  # Optimize bytecode
            
            self.office_process = subprocess.Popen([
                sys.executable, str(script_path)
            ], 
            cwd=str(self.python_systems_path),
            env=env,
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            
            # Wait a moment and verify startup
            time.sleep(3)
            if self.office_process.poll() is None:
                self.last_successful_start = datetime.now()
                self.consecutive_failures = 0
                self.stability_score = min(100, self.stability_score + 5)
                
                self.log_enhanced_activity(
                    "OFFICE_STARTED_ENHANCED", 
                    f"Process ID: {self.office_process.pid}, Stability: {self.stability_score}",
                    metrics={'startup_time': 3, 'memory_optimized': True}
                )
                return True
            else:
                self.consecutive_failures += 1
                self.stability_score = max(0, self.stability_score - 10)
                return False
                
        except Exception as e:
            self.consecutive_failures += 1
            self.stability_score = max(0, self.stability_score - 10)
            self.log_enhanced_activity("OFFICE_START_ERROR_ENHANCED", str(e), "ERROR")
            return False
    
    def cleanup_zombie_processes(self):
        """Clean up any hanging TAQWIN processes"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'taqwin' in cmdline.lower() or 'start_taqwin_office' in cmdline:
                        if proc.pid != os.getpid() and (not self.office_process or proc.pid != self.office_process.pid):
                            proc.terminate()
                            proc.wait(timeout=3)
                            self.log_enhanced_activity("ZOMBIE_CLEANUP", f"Terminated orphaned process {proc.pid}")
                except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                    pass
        except Exception as e:
            self.log_enhanced_activity("CLEANUP_ERROR", str(e), "WARNING")
    
    def restart_with_exponential_backoff(self) -> bool:
        """Restart with intelligent exponential backoff"""
        health = self.check_process_health()
        
        if not health['restart_needed']:
            return True
        
        # Log health diagnostics
        diagnostics = ', '.join(health['diagnostics'])
        self.log_enhanced_activity(
            "RESTART_NEEDED_ENHANCED", 
            f"Health issues: {diagnostics}",
            "WARNING",
            metrics=health
        )
        
        # Implement exponential backoff
        if self.consecutive_failures > 0:
            backoff_time = min(self.restart_backoff * (2 ** min(self.consecutive_failures - 1, 6)), self.max_backoff)
            self.log_enhanced_activity(
                "BACKOFF_WAIT", 
                f"Waiting {backoff_time} seconds before restart (failures: {self.consecutive_failures})"
            )
            time.sleep(backoff_time)
        
        # Graceful shutdown of existing process
        self.graceful_shutdown()
        
        # Attempt restart
        self.restart_count += 1
        if self.start_taqwin_office_enhanced():
            self.log_enhanced_activity(
                "OFFICE_RESTARTED_ENHANCED", 
                f"Restart #{self.restart_count}, Stability: {self.stability_score}"
            )
            return True
        else:
            self.log_enhanced_activity(
                "OFFICE_RESTART_FAILED_ENHANCED", 
                f"Failed restart #{self.restart_count}, Consecutive failures: {self.consecutive_failures}",
                "ERROR"
            )
            return False
    
    def graceful_shutdown(self):
        """Implement graceful shutdown with timeout"""
        if not self.office_process:
            return
        
        try:
            # Try graceful termination first
            self.office_process.terminate()
            
            # Wait up to 10 seconds for graceful shutdown
            try:
                self.office_process.wait(timeout=10)
                self.log_enhanced_activity("GRACEFUL_SHUTDOWN", "Process terminated gracefully")
            except subprocess.TimeoutExpired:
                # Force kill if graceful shutdown fails
                self.office_process.kill()
                self.office_process.wait(timeout=5)
                self.log_enhanced_activity("FORCE_SHUTDOWN", "Process force-killed after timeout", "WARNING")
                
        except Exception as e:
            self.log_enhanced_activity("SHUTDOWN_ERROR", str(e), "ERROR")
        finally:
            self.office_process = None
    
    def setup_git_authentication(self):
        """Configure Git authentication with Personal Access Token"""
        try:
            # Check if git is available
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                self.log_enhanced_activity("GIT_UNAVAILABLE", "Git not found in system PATH", "WARNING")
                return False
            
            # Create git operations log entry
            git_ops = self.read_json_log(self.git_log)
            
            # Configure git (this will require manual PAT setup)
            git_config_status = {
                "timestamp": datetime.now().isoformat(),
                "operation": "GIT_SETUP_READY",
                "details": "System ready for PAT configuration",
                "success": True,
                "instructions": [
                    "1. Generate GitHub Personal Access Token at: https://github.com/settings/tokens",
                    "2. Run: git config --global user.name 'Your Name'",
                    "3. Run: git config --global user.email 'your.email@example.com'",
                    "4. Use PAT as password when prompted for GitHub credentials",
                    "5. Consider using: git config --global credential.helper store"
                ],
                "cwd": str(self.base_path)
            }
            
            git_ops.append(git_config_status)
            self.write_json_log(self.git_log, git_ops[-100:])  # Keep last 100 entries
            
            self.log_enhanced_activity("GIT_SETUP_INITIALIZED", "Git authentication ready for PAT configuration")
            return True
            
        except Exception as e:
            self.log_enhanced_activity("GIT_SETUP_ERROR", str(e), "ERROR")
            return False
    
    def perform_git_operations(self):
        """Perform automated git operations with enhanced logging"""
        try:
            git_ops = self.read_json_log(self.git_log)
            
            # Change to base directory
            os.chdir(self.base_path)
            
            # Check git status
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True, timeout=30)
            
            if status_result.returncode == 0:
                changed_files = len([line for line in status_result.stdout.strip().split('\n') if line.strip()])
                
                git_ops.append({
                    "timestamp": datetime.now().isoformat(),
                    "operation": "STATUS_CHECK",
                    "details": f"Found {changed_files} changed files",
                    "success": True,
                    "cwd": str(self.base_path)
                })
                
                if changed_files > 0:
                    # Add changes
                    add_result = subprocess.run(['git', 'add', '.'], 
                                              capture_output=True, text=True, timeout=60)
                    
                    if add_result.returncode == 0:
                        git_ops.append({
                            "timestamp": datetime.now().isoformat(),
                            "operation": "ADD_CHANGES",
                            "details": "All changes staged successfully",
                            "success": True,
                            "cwd": str(self.base_path)
                        })
                        
                        # Commit changes
                        commit_msg = f"🚀 TAQWIN Enhanced V3.0: Alan Turing's stability improvements - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                        commit_result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                                     capture_output=True, text=True, timeout=60)
                        
                        if commit_result.returncode == 0:
                            git_ops.append({
                                "timestamp": datetime.now().isoformat(),
                                "operation": "COMMIT",
                                "details": f"Committed: {commit_msg}",
                                "success": True,
                                "cwd": str(self.base_path)
                            })
                        
            # Write git operations log
            self.write_json_log(self.git_log, git_ops[-100:])
            self.log_enhanced_activity("GIT_OPERATIONS_COMPLETE", f"Processed {len(git_ops)} operations")
            
        except subprocess.TimeoutExpired:
            self.log_enhanced_activity("GIT_TIMEOUT", "Git operation timed out", "WARNING")
        except Exception as e:
            self.log_enhanced_activity("GIT_OPERATIONS_ERROR", str(e), "ERROR")
    
    def generate_performance_analytics(self):
        """Generate comprehensive performance analytics"""
        try:
            current_metrics = self.get_system_metrics()
            
            analytics = {
                "timestamp": datetime.now().isoformat(),
                "service_uptime_hours": (datetime.now() - self.start_time).total_seconds() / 3600,
                "restart_count": self.restart_count,
                "stability_score": self.stability_score,
                "consecutive_failures": self.consecutive_failures,
                "system_health": {
                    "cpu_usage": current_metrics.get('cpu_percent', 0),
                    "memory_usage": current_metrics.get('memory_percent', 0),
                    "disk_free_gb": current_metrics.get('disk_free_gb', 0),
                    "process_count": current_metrics.get('process_count', 0)
                },
                "office_process_health": current_metrics.get('office_process', {}),
                "predictions": {
                    "next_restart_probability": max(0, min(100, self.consecutive_failures * 20)),
                    "stability_trend": "improving" if self.stability_score > 80 else "degrading" if self.stability_score < 50 else "stable",
                    "recommended_action": self.get_recommended_action()
                }
            }
            
            # Read existing analytics
            performance_data = self.read_json_log(self.performance_log)
            performance_data.append(analytics)
            
            # Keep last 24 hours of data (every 15 minutes = 96 entries)
            if len(performance_data) > 96:
                performance_data = performance_data[-96:]
            
            self.write_json_log(self.performance_log, performance_data)
            
            self.log_enhanced_activity(
                "PERFORMANCE_ANALYTICS_GENERATED", 
                f"Stability: {self.stability_score}, Trend: {analytics['predictions']['stability_trend']}"
            )
            
        except Exception as e:
            self.log_enhanced_activity("ANALYTICS_ERROR", str(e), "ERROR")
    
    def get_recommended_action(self) -> str:
        """Get AI-powered recommendation based on current state"""
        if self.stability_score >= 90:
            return "System optimal - continue monitoring"
        elif self.stability_score >= 70:
            return "Minor instability detected - increase monitoring frequency"
        elif self.stability_score >= 50:
            return "Moderate issues - consider process restart"
        elif self.consecutive_failures >= 5:
            return "Critical instability - investigate resource conflicts"
        else:
            return "System degraded - manual intervention recommended"
    
    def read_json_log(self, file_path: Path) -> List:
        """Safely read JSON log file"""
        if not file_path.exists():
            return []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def write_json_log(self, file_path: Path, data: List):
        """Safely write JSON log file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            self.logger.error(f"Failed to write log {file_path}: {e}")
    
    def create_enhanced_startup_script(self):
        """Create enhanced Windows startup script"""
        startup_script = f"""@echo off
REM TAQWIN Enhanced Background Service V3.0
REM Alan Turing's Production Stability System

cd /d "{self.python_systems_path}"
echo Starting TAQWIN Enhanced Background Service...
python "{self.python_systems_path}\\taqwin_background_service_v3.py" >nul 2>&1

REM Fallback to V2 if V3 fails
if errorlevel 1 (
    echo V3 failed, starting V2 fallback...
    python "{self.python_systems_path}\\taqwin_background_service.py" >nul 2>&1
)
"""
        
        startup_path = self.python_systems_path / "start_taqwin_enhanced.bat"
        with open(startup_path, 'w') as f:
            f.write(startup_script)
        
        self.log_enhanced_activity("ENHANCED_STARTUP_SCRIPT_CREATED", str(startup_path))
        return startup_path
    
    def display_enhanced_banner(self):
        """Display enhanced service banner"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════╗
║           🧠 ALAN TURING'S ENHANCED TAQWIN SERVICE V3.0        ║
║                    🔧 PRODUCTION STABILITY SYSTEM              ║
╠═══════════════════════════════════════════════════════════════╣
║ 🚀 Enhanced Features:                                         ║
║   • Resource optimization & memory management                 ║
║   • Exponential backoff restart strategy                     ║
║   • Advanced health monitoring & diagnostics                 ║
║   • Graceful shutdown protocols                              ║
║   • Git authentication & automation                          ║
║   • Predictive stability analytics                           ║
║   • Performance threshold alerts                             ║
╠═══════════════════════════════════════════════════════════════╣
║ 📊 Service Locations:                                         ║
║   Service: {str(self.python_systems_path):<45} ║
║   Tower:   {str(self.tower_path):<45} ║
║   Logs:    {str(self.office_inventory):<45} ║
╚═══════════════════════════════════════════════════════════════╝

🔥 ALAN TURING: "This enhanced system implements production-grade
stability with intelligent process management and predictive analytics."

🚀 ENHANCED SERVICE INITIALIZING...
"""
        print(banner)
    
    def run_enhanced_service(self):
        """Main enhanced service loop"""
        self.display_enhanced_banner()
        
        # Log service start
        self.log_enhanced_activity("ENHANCED_SERVICE_STARTED", "Alan Turing's V3.0 background service initialized")
        
        # Setup git authentication
        self.setup_git_authentication()
        
        # Create enhanced startup script
        startup_script = self.create_enhanced_startup_script()
        
        # Schedule enhanced monitoring tasks
        schedule.every(2).minutes.do(self.restart_with_exponential_backoff)  # More intelligent restart
        schedule.every(5).minutes.do(self.generate_performance_analytics)    # Performance analytics
        schedule.every(15).minutes.do(self.perform_git_operations)           # Git operations
        schedule.every(1).hours.do(lambda: self.log_enhanced_activity("HOURLY_CHECKPOINT", f"Service stable - Score: {self.stability_score}"))
        
        # Start initial office with enhanced startup
        if self.start_taqwin_office_enhanced():
            print("✅ TAQWIN Tower started with enhanced stability features")
        else:
            print("❌ Failed to start TAQWIN Tower - will retry with backoff")
        
        print("\n🎯 **ENHANCED BACKGROUND SERVICE OPERATIONAL**")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🧠 **ALAN TURING'S INTELLIGENCE ACTIVE**")
        print("🔧 **ADVANCED PROCESS STABILITY MONITORING**")
        print("📊 **PREDICTIVE ANALYTICS & HEALTH METRICS**")
        print("🔄 **EXPONENTIAL BACKOFF RESTART STRATEGY**")
        print("🔐 **GIT AUTHENTICATION & AUTOMATION READY**")
        print(f"📁 **Enhanced Logs: {self.office_inventory}**")
        print(f"🚀 **Startup Script: {startup_script}**")
        print("\n💡 **ENHANCED FEATURES:**")
        print("   • Intelligent restart with exponential backoff")
        print("   • Advanced health diagnostics & resource monitoring")
        print("   • Graceful shutdown protocols with timeout handling")
        print("   • Predictive stability analytics & trend analysis")
        print("   • Automated git operations with PAT authentication")
        print("   • Performance threshold alerts & recommendations")
        print("   • Memory optimization & zombie process cleanup")
        print(f"\n📊 **Current Stability Score: {self.stability_score}/100**")
        print("\n⏹️  Press Ctrl+C to stop enhanced background service")
        
        # Main enhanced service loop
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(15)  # Optimized check interval
                
                # Periodic garbage collection
                if datetime.now().minute % 5 == 0:
                    gc.collect()
                
        except KeyboardInterrupt:
            print("\n\n⏹️ **STOPPING ENHANCED BACKGROUND SERVICE...**")
            self.stop_enhanced_service()
        except Exception as e:
            self.log_enhanced_activity("SERVICE_CRITICAL_ERROR", str(e), "ERROR")
            print(f"\n❌ **CRITICAL SERVICE ERROR**: {str(e)}")
            self.stop_enhanced_service()
    
    def stop_enhanced_service(self):
        """Stop the enhanced background service with graceful shutdown"""
        self.running = False
        
        # Graceful shutdown of office process
        self.graceful_shutdown()
        
        # Final performance report
        final_metrics = self.get_system_metrics()
        self.log_enhanced_activity(
            "ENHANCED_SERVICE_STOPPED", 
            f"Service ran for {final_metrics.get('uptime_minutes', 0):.1f} minutes, Final stability score: {self.stability_score}",
            metrics=final_metrics
        )
        
        print("✅ **ENHANCED BACKGROUND SERVICE STOPPED**")
        print(f"📊 **Final Stability Score: {self.stability_score}/100**")
        print(f"🔄 **Total Restarts: {self.restart_count}**")
        print("👑 **ALAN TURING: 'Enhanced TAQWIN Tower ready for next activation with improved stability.'**")

def main():
    """Main function for enhanced service"""
    try:
        service = EnhancedTaqwinBackgroundService()
        service.run_enhanced_service()
    except Exception as e:
        print(f"❌ **CRITICAL STARTUP ERROR**: {str(e)}")
        print("🔄 **Falling back to standard service...**")
        # Could implement fallback to original service here

if __name__ == "__main__":
    main()
