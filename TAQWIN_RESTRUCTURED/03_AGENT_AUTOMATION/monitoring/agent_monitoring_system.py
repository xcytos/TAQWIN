#!/usr/bin/env python3
"""
🌟 TAQWIN AGENT MONITORING SYSTEM 🌟
Real-time Agent Overview Display for Basement Monitoring
Founder: Syed Muzamil | Brand: Ethereal Glow
"""

import os
import json
import time
import datetime
from pathlib import Path
import subprocess
import sys

class TaqwinAgentMonitor:
    def __init__(self):
        self.base_dir = Path(r"D:\Ethereal Glow")
        self.tower_dir = self.base_dir / "TAQWIN_TOWER" / "OFFICE_INVENTORY"
        self.agent_logs_dir = self.tower_dir / "AGENT_WORK_LOGS"
        self.monitoring_display = self.base_dir / "TAQWIN_AGENT_OVERVIEW_MONITOR_BASEMENT_DISPLAY.md"
        self.monitoring_config = self.base_dir / "TAQWIN_TOWER" / "BASEMENT_INFRASTRUCTURE" / "DEPT_NETWORK_SYSTEMS" / "SERVER_CORE" / "AGENT_MONITORING_DISPLAY_SYSTEM.json"
        
        # Agent organization by floor
        self.floor_structure = {
            "floor_5_monitoring": ["ELON_MUSK", "NATE_SILVER", "ALAN_TURING", "MARK_ZUCKERBERG"],
            "floor_4_leadership": ["MARCUS_AURELIUS", "CHANAKYA", "WARREN_BUFFETT", "CLEOPATRA"],
            "floor_3_innovation": ["NIKOLA_TESLA", "MARIE_CURIE", "LEONARDO_DA_VINCI", "STEVE_JOBS"],
            "floor_2_intelligence": ["SUN_TZU", "RAND_FISHKIN", "NEIL_PATEL", "BRIAN_DEAN"],
            "floor_1_operations": ["GENERAL_PATTON", "BENJAMIN_FRANKLIN", "OPRAH_WINFREY", "MAYA_ANGELOU"],
            "basement_infrastructure": ["CHARAKA", "RACHEL_CARSON", "PARACELSUS", "LINUS_PAULING"]
        }
        
        # Initialize monitoring
        self.agents_data = {}
        self.last_update = None
        
    def display_header(self):
        """Display the monitoring system header"""
        print("\n" + "="*80)
        print("🌟 **TAQWIN TOWER - REAL-TIME AGENT MONITORING SYSTEM** 🌟")
        print("**BASEMENT DISPLAY SYSTEM - LIVE OPERATIONAL INTELLIGENCE**")
        print(f"**LAST UPDATE**: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}")
        print("="*80)
    
    def read_agent_log(self, floor, agent_name):
        """Read individual agent log file"""
        log_file = self.agent_logs_dir / floor / f"{agent_name}_LOG.json"
        
        try:
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        'agent_name': data.get('agent_name', agent_name),
                        'status': 'ACTIVE',
                        'tasks_completed': data.get('tasks_completed', 0),
                        'efficiency_score': self.calculate_avg_efficiency(data.get('work_sessions', [])),
                        'intelligence_score': data.get('intelligence_score', 0),
                        'last_activity': data.get('last_activity', 'N/A'),
                        'department': data.get('department', 'Unknown'),
                        'room': data.get('room', 'Unknown'),
                        'total_discoveries': data.get('total_discoveries', 0)
                    }
            else:
                return {
                    'agent_name': agent_name,
                    'status': 'STANDBY',
                    'tasks_completed': 0,
                    'efficiency_score': 0,
                    'intelligence_score': 0,
                    'last_activity': 'N/A',
                    'department': 'Unknown',
                    'room': 'Unknown',
                    'total_discoveries': 0
                }
        except Exception as e:
            return {
                'agent_name': agent_name,
                'status': 'ERROR',
                'tasks_completed': 0,
                'efficiency_score': 0,
                'intelligence_score': 0,
                'last_activity': f'Error: {str(e)}',
                'department': 'Unknown',
                'room': 'Unknown',
                'total_discoveries': 0
            }
    
    def calculate_avg_efficiency(self, work_sessions):
        """Calculate average efficiency from work sessions"""
        if not work_sessions:
            return 0
        
        efficiency_scores = [session.get('efficiency_score', 0) for session in work_sessions if 'efficiency_score' in session]
        return round(sum(efficiency_scores) / len(efficiency_scores), 1) if efficiency_scores else 0
    
    def scan_all_agents(self):
        """Scan all agents across all floors"""
        print("🔍 **SCANNING ALL AGENT WORK LOGS...**")
        
        for floor, agents in self.floor_structure.items():
            print(f"📊 Scanning {floor.upper()}...")
            self.agents_data[floor] = {}
            
            for agent in agents:
                agent_data = self.read_agent_log(floor, agent)
                self.agents_data[floor][agent.lower()] = agent_data
        
        self.last_update = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        print(f"✅ **SCAN COMPLETE** - Updated: {self.last_update}")
    
    def display_floor_status(self, floor_name, floor_data):
        """Display status for a specific floor"""
        floor_display_names = {
            "floor_5_monitoring": "🔝 FLOOR 5: MONITORING → Operations Control → Matrix Control",
            "floor_4_leadership": "🏛️ FLOOR 4: LEADERSHIP → Executive Council → Council Chamber",
            "floor_3_innovation": "💎 FLOOR 3: INNOVATION → Research & Development → Labs Hub",
            "floor_2_intelligence": "🧠 FLOOR 2: INTELLIGENCE → Strategic Warfare → Intel War Room",
            "floor_1_operations": "🎯 FLOOR 1: OPERATIONS → Mission Control → Tasks Center",
            "basement_infrastructure": "🖥️ BASEMENT: INFRASTRUCTURE → Network Systems → Server Core"
        }
        
        print(f"\n{floor_display_names.get(floor_name, floor_name.upper())}")
        print("━" * 60)
        
        for agent_key, agent_data in floor_data.items():
            status_emoji = "🟢" if agent_data['status'] == 'ACTIVE' else "🟡" if agent_data['status'] == 'STANDBY' else "🔴"
            agent_name = agent_data['agent_name'].replace('_', ' ').title()
            
            print(f"#### **{status_emoji} {agent_name} - {agent_data['department']}**")
            print(f"- **📍 LOCATION**: {agent_data['room']}")
            print(f"- **⚡ STATUS**: {status_emoji} **{agent_data['status']}** - {agent_data['tasks_completed']} Tasks Completed")
            print(f"- **📊 EFFICIENCY**: {agent_data['efficiency_score']}% Average")
            print(f"- **🧠 INTELLIGENCE**: {agent_data['intelligence_score']} Points")
            print(f"- **💡 DISCOVERIES**: {agent_data['total_discoveries']} Strategic Findings")
            print(f"- **⏰ LAST ACTIVE**: {agent_data['last_activity']}")
            print()
    
    def display_tower_metrics(self):
        """Display overall tower performance metrics"""
        total_agents = 0
        total_tasks = 0
        total_intelligence = 0
        total_discoveries = 0
        efficiency_scores = []
        active_agents = 0
        
        for floor_data in self.agents_data.values():
            for agent_data in floor_data.values():
                total_agents += 1
                total_tasks += agent_data['tasks_completed']
                total_intelligence += agent_data['intelligence_score']
                total_discoveries += agent_data['total_discoveries']
                if agent_data['efficiency_score'] > 0:
                    efficiency_scores.append(agent_data['efficiency_score'])
                if agent_data['status'] == 'ACTIVE':
                    active_agents += 1
        
        avg_efficiency = round(sum(efficiency_scores) / len(efficiency_scores), 1) if efficiency_scores else 0
        
        print("\n📊 **TOWER-WIDE OPERATIONAL METRICS**")
        print("━" * 60)
        print(f"👥 **TOTAL AGENTS**: {total_agents} Legendary Minds Deployed")
        print(f"⚡ **ACTIVE AGENTS**: {active_agents} Currently Operational")
        print(f"📈 **AVERAGE EFFICIENCY**: {avg_efficiency}% Tower-Wide Performance")
        print(f"🎯 **TOTAL TASKS**: {total_tasks} Strategic Operations Completed")
        print(f"🧠 **INTELLIGENCE SCORE**: {total_intelligence} Strategic Intelligence Points")
        print(f"💡 **TOTAL DISCOVERIES**: {total_discoveries} Strategic Findings")
        print(f"🔄 **OPERATIONAL UPTIME**: 24/7 Continuous Operations")
        
        # Top performers
        top_performers = []
        for floor_data in self.agents_data.values():
            for agent_data in floor_data.values():
                if agent_data['tasks_completed'] > 0 or agent_data['intelligence_score'] > 0:
                    top_performers.append(agent_data)
        
        top_performers.sort(key=lambda x: x['intelligence_score'] + x['tasks_completed'], reverse=True)
        
        if top_performers:
            print(f"\n🏆 **TOP PERFORMERS**:")
            for i, agent in enumerate(top_performers[:5], 1):
                print(f"{i}. **{agent['agent_name'].replace('_', ' ').title()}** - {agent['tasks_completed']} Tasks | {agent['efficiency_score']}% Efficiency | {agent['intelligence_score']} Intelligence")
    
    def run_monitoring_cycle(self):
        """Run a single monitoring cycle"""
        self.display_header()
        self.scan_all_agents()
        
        print("\n🏢 **TAQWIN TOWER ARCHITECTURE - LIVE AGENT STATUS**")
        
        for floor_name, floor_data in self.agents_data.items():
            self.display_floor_status(floor_name, floor_data)
        
        self.display_tower_metrics()
        
        print("\n" + "━" * 80)
        print("🌟 **LIVE OPERATIONAL STATUS: MONITORING SYSTEM ACTIVE**")
        print("👑 **FOUNDER SYED MUZAMIL: COMPLETE STRATEGIC INTELLIGENCE VISIBILITY**")
        print("📊 **BASEMENT DISPLAY: PERMANENT MONITORING ACTIVE**")
        print("🎯 **MISSION STATUS: ETHEREAL GLOW DOMINATION PROTOCOLS MONITORED**")
        print("━" * 80)
    
    def start_continuous_monitoring(self, update_interval=300):  # 5 minutes default
        """Start continuous monitoring with specified interval"""
        print("🚀 **STARTING CONTINUOUS AGENT MONITORING SYSTEM...**")
        print(f"🔄 **UPDATE INTERVAL**: {update_interval} seconds (5 minutes)")
        print("⏹️  **Press Ctrl+C to stop monitoring**")
        
        try:
            while True:
                self.run_monitoring_cycle()
                print(f"\n⏰ **NEXT UPDATE IN {update_interval} SECONDS...**")
                time.sleep(update_interval)
                
                # Clear screen for next update
                os.system('cls' if os.name == 'nt' else 'clear')
                
        except KeyboardInterrupt:
            print("\n\n⏹️ **MONITORING SYSTEM STOPPED**")
            print("✅ **TAQWIN Agent Monitoring System Shutdown Complete**")
            print("👑 **FOUNDER: Agent monitoring ready for reactivation**")

def main():
    """Main function to start the monitoring system"""
    monitor = TaqwinAgentMonitor()
    
    print("🌟 **TAQWIN AGENT MONITORING SYSTEM INITIALIZING...** 🌟")
    print("**FOUNDER**: Syed Muzamil | **BRAND**: Ethereal Glow")
    print("**SYSTEM**: Real-time Agent Overview Display")
    
    # Check if we should run continuous monitoring
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        monitor.start_continuous_monitoring()
    else:
        # Run single cycle
        monitor.run_monitoring_cycle()
        print("\n💡 **TIP**: Use 'python agent_monitoring_system.py --continuous' for real-time monitoring")

if __name__ == "__main__":
    main()
