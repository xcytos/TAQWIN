#!/usr/bin/env python3
"""
🌟 TAQWIN RAPID AGENT MONITORING SYSTEM 🌟
15-Second High-Frequency Agent Status Updates
Founder: Syed Muzamil | Brand: Ethereal Glow
"""

import os
import json
import time
import datetime
from pathlib import Path
import sys

class RapidTaqwinMonitor:
    def __init__(self):
        self.base_dir = Path(r"D:\Ethereal Glow")
        self.tower_dir = self.base_dir / "TAQWIN_TOWER" / "OFFICE_INVENTORY"
        self.agent_logs_dir = self.tower_dir / "AGENT_WORK_LOGS"
        
        # Key agents for rapid monitoring
        self.priority_agents = {
            "floor_5_monitoring": ["ELON_MUSK", "ALAN_TURING"],
            "floor_2_intelligence": ["SUN_TZU", "RAND_FISHKIN"],
            "floor_1_operations": ["GENERAL_PATTON", "BENJAMIN_FRANKLIN"]
        }
        
        self.update_count = 0
        
    def get_current_time(self):
        """Get formatted current time"""
        return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def read_priority_agent(self, floor, agent_name):
        """Read priority agent data quickly"""
        log_file = self.agent_logs_dir / floor / f"{agent_name}_LOG.json"
        
        try:
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Get latest work session
                    work_sessions = data.get('work_sessions', [])
                    latest_session = work_sessions[-1] if work_sessions else {}
                    
                    return {
                        'name': agent_name.replace('_', ' ').title(),
                        'status': '🟢 ACTIVE',
                        'tasks': data.get('tasks_completed', 0),
                        'efficiency': latest_session.get('efficiency_score', 0),
                        'intelligence': data.get('intelligence_score', 0),
                        'discoveries': data.get('total_discoveries', 0),
                        'last_activity': data.get('last_activity', 'N/A')
                    }
            else:
                return {
                    'name': agent_name.replace('_', ' ').title(),
                    'status': '🟡 STANDBY',
                    'tasks': 0,
                    'efficiency': 0,
                    'intelligence': 0,
                    'discoveries': 0,
                    'last_activity': 'N/A'
                }
        except:
            return {
                'name': agent_name.replace('_', ' ').title(),
                'status': '🔴 ERROR',
                'tasks': 0,
                'efficiency': 0,
                'intelligence': 0,
                'discoveries': 0,
                'last_activity': 'Error reading log'
            }
    
    def display_rapid_update(self):
        """Display rapid 15-second update"""
        self.update_count += 1
        current_time = self.get_current_time()
        
        print("\n" + "═" * 80)
        print(f"🌟 **TAQWIN RAPID MONITORING - UPDATE #{self.update_count}** 🌟")
        print(f"⏰ **TIME**: {current_time} | **INTERVAL**: 15 seconds")
        print("═" * 80)
        
        total_tasks = 0
        total_intelligence = 0
        total_discoveries = 0
        active_agents = 0
        
        # Monitor priority agents
        for floor, agents in self.priority_agents.items():
            floor_name = floor.replace('_', ' ').upper()
            print(f"\n📊 **{floor_name}**:")
            print("─" * 40)
            
            for agent in agents:
                agent_data = self.read_priority_agent(floor, agent)
                
                print(f"{agent_data['status']} **{agent_data['name']}**")
                print(f"   📋 Tasks: {agent_data['tasks']} | "
                      f"⚡ Efficiency: {agent_data['efficiency']}% | "
                      f"🧠 Intel: {agent_data['intelligence']} | "
                      f"💡 Discoveries: {agent_data['discoveries']}")
                
                total_tasks += agent_data['tasks']
                total_intelligence += agent_data['intelligence']
                total_discoveries += agent_data['discoveries']
                if '🟢' in agent_data['status']:
                    active_agents += 1
        
        # Quick metrics summary
        print(f"\n📈 **RAPID METRICS SUMMARY**:")
        print("─" * 40)
        print(f"⚡ **ACTIVE PRIORITY AGENTS**: {active_agents}/6")
        print(f"📋 **TOTAL TASKS**: {total_tasks}")
        print(f"🧠 **TOTAL INTELLIGENCE**: {total_intelligence}")
        print(f"💡 **TOTAL DISCOVERIES**: {total_discoveries}")
        
        # System status
        if active_agents >= 5:
            status = "🟢 OPTIMAL"
        elif active_agents >= 3:
            status = "🟡 FUNCTIONAL"
        else:
            status = "🔴 ATTENTION NEEDED"
            
        print(f"🎯 **SYSTEM STATUS**: {status}")
        print(f"🔄 **NEXT UPDATE**: 15 seconds...")
    
    def start_rapid_monitoring(self):
        """Start 15-second rapid monitoring"""
        print("🚀 **STARTING TAQWIN RAPID MONITORING SYSTEM** 🚀")
        print("⚡ **UPDATE FREQUENCY**: Every 15 seconds")
        print("🎯 **MONITORING**: Priority agents across key floors")
        print("⏹️  **Press Ctrl+C to stop rapid monitoring**")
        print("\n👑 **FOUNDER SYED MUZAMIL**: Real-time strategic intelligence active!")
        
        try:
            while True:
                self.display_rapid_update()
                time.sleep(15)  # 15-second intervals
                
        except KeyboardInterrupt:
            print("\n\n⏹️ **RAPID MONITORING STOPPED**")
            print(f"✅ **TOTAL UPDATES DELIVERED**: {self.update_count}")
            print(f"⏰ **MONITORING DURATION**: {self.update_count * 15} seconds")
            print("🌟 **TAQWIN Rapid Monitor shutdown complete**")
            print("👑 **FOUNDER: Ready for next activation!**")

def main():
    """Main function for rapid monitoring"""
    monitor = RapidTaqwinMonitor()
    
    print("🌟 **TAQWIN RAPID AGENT MONITORING INITIALIZING...** 🌟")
    print("**FOUNDER**: Syed Muzamil | **BRAND**: Ethereal Glow")
    print("**SYSTEM**: 15-Second High-Frequency Updates")
    print("**FOCUS**: Priority agents for maximum strategic visibility")
    
    monitor.start_rapid_monitoring()

if __name__ == "__main__":
    main()
