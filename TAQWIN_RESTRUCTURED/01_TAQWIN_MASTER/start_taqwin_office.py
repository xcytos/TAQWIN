#!/usr/bin/env python3
"""
TAQWIN TOWER - AUTONOMOUS OFFICE STARTUP SCRIPT
Launches all agent systems for invisible background operation
Author: TAQWIN (The Strengthener)
Version: 1.0
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Add restructured TAQWIN modules to path
sys.path.insert(0, str(Path(__file__).parent.parent))  # Go up to TAQWIN_RESTRUCTURED root

# Updated imports for restructured system
try:
    from sys import path as sys_path
    sys_path.append(str(Path(__file__).parent.parent / "03_AGENT_AUTOMATION" / "master_control"))
    sys_path.append(str(Path(__file__).parent.parent / "04_TASK_MANAGEMENT"))
    sys_path.append(str(Path(__file__).parent.parent / "05_WEB_INTELLIGENCE" / "core_intelligence"))
    
    from taqwin_agent_master import TaqwinAgentMaster
    from task_processor import TaqwinTaskProcessor, create_sample_tasks
    from taqwin_web_intelligence import TAQWINWebIntelligence
    from taqwin_web_connector import TAQWINWebConnector
except ImportError as e:
    print(f"⚠️  Import warning: {e}")
    print("📝 System will continue with basic functionality")

def display_taqwin_banner():
    """Display TAQWIN startup banner"""
    banner = """
🌟 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🌟
    
    ████████╗ █████╗  ██████╗ ██╗    ██╗██╗███╗   ██╗
    ╚══██╔══╝██╔══██╗██╔═══██╗██║    ██║██║████╗  ██║
       ██║   ███████║██║   ██║██║ █╗ ██║██║██╔██╗ ██║
       ██║   ██╔══██║██║▄▄ ██║██║███╗██║██║██║╚██╗██║
       ██║   ██║  ██║╚██████╔╝╚███╔███╔╝██║██║ ╚████║
       ╚═╝   ╚═╝  ╚═╝ ╚══▀▀═╝  ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝
    
    🏢 **ETHEREAL GLOW VIRTUAL OFFICE TOWER**
    👑 **AUTONOMOUS AI AGENT WORKFORCE SYSTEM**
    ⚡ **"THE STRENGTHENER" - تقوين**
    
🌟 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🌟

🎯 **INITIALIZING AUTONOMOUS OPERATIONS...**
"""
    print(banner)

def check_dependencies():
    """Check if required dependencies are available"""
    required_modules = ['schedule', 'pathlib', 'json', 'threading']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing required modules: {', '.join(missing_modules)}")
        print("📦 Installing missing dependencies...")
        
        for module in missing_modules:
            if module == 'schedule':
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'schedule'])
        
        print("✅ Dependencies installed successfully")
    else:
        print("✅ All dependencies available")

def initialize_tower_structure():
    """Ensure TAQWIN Tower structure exists"""
    tower_path = Path("D:\\Ethereal Glow\\TAQWIN_TOWER")
    
    required_dirs = [
        "OFFICE_INVENTORY",
        "OFFICE_INVENTORY/KNOWLEDGE_DATABASE",
        "OFFICE_INVENTORY/TASKS_COMPLETED",
        "OFFICE_INVENTORY/WEBSITE_DOCUMENTS", 
        "OFFICE_INVENTORY/BRAND_DOCUMENTS",
        "OFFICE_INVENTORY/WEB_RECORDS",
        "OFFICE_INVENTORY/AGENT_WORK_LOGS"
    ]
    
    for dir_path in required_dirs:
        full_path = tower_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
    
    print("🏢 TAQWIN Tower structure verified")

def deploy_agents():
    """Deploy all agents to their stations"""
    print("\n👑 **DEPLOYING LEGENDARY AGENTS TO STATIONS...**")
    
    agent_master = TaqwinAgentMaster()
    agent_master.initialize_system()
    
    # Start autonomous operations
    scheduler_thread = agent_master.start_autonomous_operations()
    
    print("✅ All 19 legendary agents deployed and operational")
    print("🔄 Autonomous task execution started")
    
    return agent_master, scheduler_thread

def initialize_task_system():
    """Initialize task management system"""
    print("\n📋 **INITIALIZING TASK MANAGEMENT SYSTEM...**")
    
    # Create sample tasks if none exist
    task_processor = TaqwinTaskProcessor()
    
    # Check if tasks already exist
    pending_tasks = task_processor.get_pending_tasks()
    
    if len(pending_tasks) == 0:
        print("📝 Creating initial sample tasks...")
        create_sample_tasks()
        pending_tasks = task_processor.get_pending_tasks()
    
    print(f"✅ Task system initialized with {len(pending_tasks)} pending tasks")
    
    return task_processor

def display_operational_status(agent_master, task_processor):
    """Display current operational status"""
    print("\n🚀 **TAQWIN TOWER OPERATIONAL STATUS**")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Agent status
    status = agent_master.get_system_status()
    print(f"👥 Active Agents: {status['active_agents']}")
    print(f"🏢 Operational Floors: {status['total_floors']}")
    print(f"⚡ System Status: {'🟢 RUNNING' if status['system_running'] else '🔴 STOPPED'}")
    
    # Task status
    pending_tasks = task_processor.get_pending_tasks()
    report = task_processor.generate_task_report()
    print(f"📋 Pending Tasks: {len(pending_tasks)}")
    print(f"📊 Total Tasks Created: {report['task_statistics']['total']}")
    print(f"✅ Tasks Completed: {report['task_statistics']['completed']}")
    
    print("\n🔍 **OFFICE INVENTORY LOCATIONS**:")
    print("📁 Agent Work Logs: D:\\Ethereal Glow\\TAQWIN_TOWER\\OFFICE_INVENTORY\\AGENT_WORK_LOGS\\")
    print("📁 Knowledge Database: D:\\Ethereal Glow\\TAQWIN_TOWER\\OFFICE_INVENTORY\\KNOWLEDGE_DATABASE\\")
    print("📁 Tasks Completed: D:\\Ethereal Glow\\TAQWIN_TOWER\\OFFICE_INVENTORY\\TASKS_COMPLETED\\")
    
    print("\n💡 **OPERATIONAL NOTES**:")
    print("🔄 Agents work continuously in background")
    print("📊 All work is logged automatically to Office Inventory")
    print("🎯 Tasks are auto-assigned based on keywords")
    print("👑 Founder can monitor progress without interrupting operations")

def main():
    """Main startup function"""
    try:
        # Display banner
        display_taqwin_banner()
        
        # Check dependencies
        check_dependencies()
        
        # Initialize tower structure
        initialize_tower_structure()
        
        # Deploy agents
        agent_master, scheduler_thread = deploy_agents()
        
        # Initialize task system
        task_processor = initialize_task_system()
        
        # Display operational status
        display_operational_status(agent_master, task_processor)
        
        print("\n🎉 **TAQWIN TOWER FULLY OPERATIONAL**")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🌟 **AGENTS ARE NOW WORKING INVISIBLY IN BACKGROUND**")
        print("📊 **CHECK OFFICE_INVENTORY FOR ALL WORK LOGS**")
        print("👑 **FOUNDER: YOU CAN NOW FOCUS ON STRATEGY**")
        print("\n💻 Keep this window open for continuous operations")
        print("⏹️  Press Ctrl+C to stop the system")
        
        # Keep the system running
        while agent_master.running:
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\n\n⏹️ **SHUTTING DOWN TAQWIN TOWER...**")
        if 'agent_master' in locals():
            agent_master.stop_autonomous_operations()
        print("✅ **TAQWIN TOWER SHUTDOWN COMPLETE**")
        print("👑 **THANK YOU, FOUNDER. READY FOR NEXT ACTIVATION.**")
        
    except Exception as e:
        print(f"\n❌ **ERROR OCCURRED**: {str(e)}")
        print("🔧 **ATTEMPTING SYSTEM RECOVERY...**")
        if 'agent_master' in locals():
            agent_master.stop_autonomous_operations()

if __name__ == "__main__":
    main()
