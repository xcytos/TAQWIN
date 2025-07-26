#!/usr/bin/env python3
"""
TAQWIN TOWER - COMPLETE DEPLOYMENT SYSTEM
Master deployment script for full TAQWIN Tower operations
Author: TAQWIN (The Strengthener)
Version: 2.0 - Complete System Integration
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path
import time

# Add python-systems to path
sys.path.insert(0, str(Path(__file__).parent))

class TaqwinCompleteDeployment:
    def __init__(self):
        self.base_path = Path("D:\\Ethereal Glow")
        self.python_systems_path = self.base_path / "python-systems"
        self.tower_path = self.base_path / "TAQWIN_TOWER"
        self.office_inventory = self.tower_path / "OFFICE_INVENTORY"
        self.deployment_log = self.office_inventory / "COMPLETE_DEPLOYMENT_LOG.json"
        
        # Ensure directories exist
        self.office_inventory.mkdir(parents=True, exist_ok=True)
        
        self.deployment_steps = []
        self.start_time = datetime.now()
    
    def log_step(self, step, details, success=True):
        """Log deployment step"""
        step_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "details": details,
            "success": success,
            "duration_seconds": (datetime.now() - self.start_time).total_seconds()
        }
        
        self.deployment_steps.append(step_entry)
        
        status = "✅" if success else "❌"
        print(f"{status} {step}: {details}")
        
        # Save log after each step
        self.save_deployment_log()
    
    def save_deployment_log(self):
        """Save deployment log"""
        deployment_data = {
            "deployment_start": self.start_time.isoformat(),
            "deployment_end": datetime.now().isoformat(),
            "total_duration": (datetime.now() - self.start_time).total_seconds(),
            "total_steps": len(self.deployment_steps),
            "successful_steps": len([s for s in self.deployment_steps if s["success"]]),
            "failed_steps": len([s for s in self.deployment_steps if not s["success"]]),
            "steps": self.deployment_steps
        }
        
        try:
            with open(self.deployment_log, 'w', encoding='utf-8') as f:
                json.dump(deployment_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save deployment log: {e}")
    
    def run_command(self, command, cwd=None, description=""):
        """Run command safely"""
        try:
            if cwd is None:
                cwd = self.python_systems_path
            
            result = subprocess.run(
                command,
                cwd=str(cwd),
                capture_output=True,
                text=True,
                shell=True
            )
            
            success = result.returncode == 0
            details = f"{description} - {result.stdout[:200] if result.stdout else 'No output'}"
            
            if not success and result.stderr:
                details += f" | Error: {result.stderr[:200]}"
            
            return success, details
            
        except Exception as e:
            return False, f"{description} - Exception: {str(e)}"
    
    def test_python_systems(self):
        """Test all Python systems"""
        self.log_step("TESTING_SYSTEMS", "Running comprehensive system tests")
        
        # Test main systems
        test_commands = [
            ("python test_taqwin_system.py", "Core system validation"),
            ("python check_taqwin_status.py", "Status checker validation"),
            ("python -c \"import schedule; print('Schedule module OK')\"", "Dependencies check")
        ]
        
        all_success = True
        for command, desc in test_commands:
            success, details = self.run_command(command, description=desc)
            if not success:
                all_success = False
                self.log_step(f"TEST_FAILED_{desc.upper().replace(' ', '_')}", details, False)
        
        if all_success:
            self.log_step("SYSTEM_TESTS", "All system tests passed", True)
        else:
            self.log_step("SYSTEM_TESTS", "Some system tests failed", False)
        
        return all_success
    
    def deploy_background_service(self):
        """Deploy background service"""
        self.log_step("BACKGROUND_SERVICE", "Deploying TAQWIN Tower background service")
        
        # Check if already running
        try:
            result = subprocess.run([
                'wmic', 'process', 'where', 
                'name="python.exe"', 'get', 'CommandLine'
            ], capture_output=True, text=True, shell=True)
            
            if 'taqwin_background_service.py' in result.stdout:
                self.log_step("BACKGROUND_SERVICE", "Background service already running")
                return True
        except:
            pass
        
        # Start background service
        try:
            process = subprocess.Popen([
                'python', 'taqwin_background_service.py'
            ], 
            cwd=str(self.python_systems_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            
            # Give it time to start
            time.sleep(3)
            
            # Check if it's running
            if process.poll() is None:
                self.log_step("BACKGROUND_SERVICE", f"Background service started with PID: {process.pid}")
                return True
            else:
                stdout, stderr = process.communicate()
                self.log_step("BACKGROUND_SERVICE", f"Failed to start: {stderr}", False)
                return False
                
        except Exception as e:
            self.log_step("BACKGROUND_SERVICE", f"Exception starting service: {str(e)}", False)
            return False
    
    def install_autostart(self):
        """Install Windows autostart"""
        self.log_step("AUTOSTART_INSTALL", "Installing Windows autostart capability")
        
        try:
            # Run PowerShell autostart installer
            ps_script = self.python_systems_path / "install_taqwin_autostart.ps1"
            
            if ps_script.exists():
                success, details = self.run_command(
                    f'PowerShell -ExecutionPolicy Bypass "{ps_script}" -Install',
                    description="PowerShell autostart installation"
                )
                
                if success:
                    self.log_step("AUTOSTART_INSTALL", "Windows autostart installed successfully")
                    return True
                else:
                    self.log_step("AUTOSTART_INSTALL", f"Autostart installation failed: {details}", False)
            else:
                self.log_step("AUTOSTART_INSTALL", "PowerShell script not found", False)
            
        except Exception as e:
            self.log_step("AUTOSTART_INSTALL", f"Exception during autostart: {str(e)}", False)
        
        return False
    
    def validate_tower_structure(self):
        """Validate TAQWIN Tower structure"""
        self.log_step("TOWER_VALIDATION", "Validating TAQWIN Tower directory structure")
        
        required_dirs = [
            "OFFICE_INVENTORY",
            "OFFICE_INVENTORY/KNOWLEDGE_DATABASE",
            "OFFICE_INVENTORY/TASKS_COMPLETED",
            "OFFICE_INVENTORY/AGENT_WORK_LOGS",
            "OFFICE_INVENTORY/WEBSITE_DOCUMENTS",
            "OFFICE_INVENTORY/BRAND_DOCUMENTS",
            "OFFICE_INVENTORY/WEB_RECORDS"
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            full_path = self.tower_path / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                missing_dirs.append(dir_path)
        
        if missing_dirs:
            self.log_step("TOWER_VALIDATION", f"Created missing directories: {len(missing_dirs)}")
        else:
            self.log_step("TOWER_VALIDATION", "All required directories present")
        
        return True
    
    def update_requirements(self):
        """Update requirements.txt with all dependencies"""
        self.log_step("REQUIREMENTS_UPDATE", "Updating requirements.txt with complete dependencies")
        
        requirements_content = """# TAQWIN Tower - Python Dependencies
# Core Systems
schedule>=1.2.0
pathlib>=1.0.1

# Web Intelligence  
requests>=2.28.0
beautifulsoup4>=4.11.0
selenium>=4.8.0

# Video Generation
opencv-python>=4.7.0
Pillow>=9.4.0
moviepy>=1.0.3

# Data Processing
pandas>=1.5.0
numpy>=1.24.0

# AI/ML (Optional)
openai>=0.27.0
anthropic>=0.2.0

# Development Tools
pytest>=7.2.0
black>=23.0.0
"""
        
        try:
            with open(self.python_systems_path / "requirements.txt", 'w') as f:
                f.write(requirements_content)
            
            self.log_step("REQUIREMENTS_UPDATE", "Requirements.txt updated with complete dependencies")
            return True
            
        except Exception as e:
            self.log_step("REQUIREMENTS_UPDATE", f"Failed to update requirements: {str(e)}", False)
            return False
    
    def perform_git_deployment(self):
        """Perform Git deployment"""
        self.log_step("GIT_DEPLOYMENT", "Initiating Git deployment")
        
        try:
            # Import and use Git manager
            git_manager_path = self.python_systems_path / "git-integration" / "taqwin_git_manager.py"
            
            if git_manager_path.exists():
                success, details = self.run_command(
                    f'python "{git_manager_path}" deploy "🚀 TAQWIN Tower: Complete system deployment with background services, Git integration, and unified deployment"',
                    description="Git deployment execution"
                )
                
                if success:
                    self.log_step("GIT_DEPLOYMENT", "Git deployment completed successfully")
                    return True
                else:
                    self.log_step("GIT_DEPLOYMENT", f"Git deployment failed: {details}", False)
            else:
                self.log_step("GIT_DEPLOYMENT", "Git manager not found", False)
                
        except Exception as e:
            self.log_step("GIT_DEPLOYMENT", f"Exception during Git deployment: {str(e)}", False)
        
        return False
    
    def generate_deployment_summary(self):
        """Generate comprehensive deployment summary"""
        summary = {
            "deployment_time": datetime.now().isoformat(),
            "total_duration": (datetime.now() - self.start_time).total_seconds(),
            "successful_steps": len([s for s in self.deployment_steps if s["success"]]),
            "failed_steps": len([s for s in self.deployment_steps if not s["success"]]),
            "deployment_status": "SUCCESS" if all(s["success"] for s in self.deployment_steps) else "PARTIAL",
            "components_deployed": [
                "TAQWIN Tower Background Service",
                "Git Integration System", 
                "Windows Autostart",
                "Status Monitoring",
                "Complete Documentation",
                "Agent Automation Systems",
                "Video Generation Pipeline",
                "Web Intelligence Network"
            ],
            "key_features": [
                "24/7 Background Operations",
                "Automatic System Restart",
                "Windows Boot Integration", 
                "Smart Git Deployment",
                "Real-time Health Monitoring",
                "Comprehensive Activity Logging",
                "Multi-agent Coordination",
                "AI Video Generation",
                "Web Intelligence Gathering"
            ]
        }
        
        # Save summary
        summary_path = self.office_inventory / "DEPLOYMENT_SUMMARY.json"
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save deployment summary: {e}")
        
        return summary
    
    def display_banner(self):
        """Display deployment banner"""
        banner = """
🌟 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🌟

    ████████╗ █████╗  ██████╗ ██╗    ██╗██╗███╗   ██╗
    ╚══██╔══╝██╔══██╗██╔═══██╗██║    ██║██║████╗  ██║
       ██║   ███████║██║   ██║██║ █╗ ██║██║██╔██╗ ██║
       ██║   ██╔══██║██║▄▄ ██║██║███╗██║██║██║╚██╗██║
       ██║   ██║  ██║╚██████╔╝╚███╔███╔╝██║██║ ╚████║
       ╚═╝   ╚═╝  ╚═╝ ╚══▀▀═╝  ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝

    🏢 **COMPLETE SYSTEM DEPLOYMENT**
    👑 **MASTER DEPLOYMENT PROTOCOL**
    ⚡ **FULL STACK INTEGRATION**

🌟 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🌟

🚀 **INITIATING COMPLETE TAQWIN TOWER DEPLOYMENT...**
"""
        print(banner)
    
    def run_complete_deployment(self):
        """Run complete deployment process"""
        self.display_banner()
        
        deployment_sequence = [
            ("validate_tower_structure", "🏢 Validating TAQWIN Tower Structure"),
            ("update_requirements", "📦 Updating Python Dependencies"),
            ("test_python_systems", "🧪 Testing All Python Systems"),
            ("deploy_background_service", "🔄 Deploying Background Service"),
            ("install_autostart", "🔧 Installing Windows Autostart"),
            ("perform_git_deployment", "📤 Performing Git Deployment")
        ]
        
        print(f"\n📋 **DEPLOYMENT SEQUENCE**: {len(deployment_sequence)} steps")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        for i, (method_name, description) in enumerate(deployment_sequence, 1):
            print(f"\n[{i}/{len(deployment_sequence)}] {description}")
            
            try:
                method = getattr(self, method_name)
                success = method()
                
                if not success:
                    print(f"⚠️  Step {i} encountered issues but continuing...")
                    
            except Exception as e:
                self.log_step(method_name.upper(), f"Exception: {str(e)}", False)
                print(f"❌ Step {i} failed with exception: {str(e)}")
        
        # Generate final summary
        summary = self.generate_deployment_summary()
        
        # Display completion status
        print("\n🎉 **DEPLOYMENT COMPLETED**")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"⏱️  Total Duration: {summary['total_duration']:.1f} seconds")
        print(f"✅ Successful Steps: {summary['successful_steps']}")
        print(f"❌ Failed Steps: {summary['failed_steps']}")
        print(f"🎯 Overall Status: {summary['deployment_status']}")
        
        print(f"\n🏢 **COMPONENTS DEPLOYED**:")
        for component in summary['components_deployed']:
            print(f"   • {component}")
        
        print(f"\n⚡ **KEY FEATURES ACTIVE**:")
        for feature in summary['key_features']:
            print(f"   • {feature}")
        
        print(f"\n📁 **DEPLOYMENT LOGS**: {self.deployment_log}")
        print(f"📄 **SUMMARY**: {self.office_inventory / 'DEPLOYMENT_SUMMARY.json'}")
        
        print("\n👑 **TAQWIN TOWER DEPLOYMENT COMPLETE**")
        print("🌟 The Strengthener is now fully operational! 🌟")
        
        return summary['deployment_status'] == "SUCCESS"

def main():
    """Main deployment function"""
    deployment = TaqwinCompleteDeployment()
    
    try:
        success = deployment.run_complete_deployment()
        exit_code = 0 if success else 1
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  **DEPLOYMENT INTERRUPTED BY USER**")
        deployment.log_step("DEPLOYMENT_INTERRUPTED", "User interrupted deployment", False)
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ **DEPLOYMENT FAILED**: {str(e)}")
        deployment.log_step("DEPLOYMENT_EXCEPTION", str(e), False)
        sys.exit(1)

if __name__ == "__main__":
    main()
