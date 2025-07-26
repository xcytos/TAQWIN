#!/usr/bin/env python3
"""
🚀 TAQWIN TOWER AGENT LIFT SYSTEM LAUNCHER
Quick start script for agent transportation system
"""

import os
import sys
from pathlib import Path

def main():
    print("🏛️ TAQWIN TOWER AGENT LIFT SYSTEM LAUNCHER 🏛️")
    print("=" * 60)
    print("🚀 Initializing agent transportation system...")
    print("📍 Location: D:\\Ethereal Glow\\python-systems")
    print("🎯 Mission: TOP 5 ranking domination")
    print("=" * 60)
    
    # Import and run the main lift system
    try:
        from agent_lift_system import main as lift_main
        lift_main()
    except ImportError as e:
        print(f"❌ Error importing lift system: {e}")
        print("🔧 Please ensure agent_lift_system.py is in the same directory")
    except Exception as e:
        print(f"❌ Error starting lift system: {e}")
        print("🔧 Please check system configuration")

if __name__ == "__main__":
    main()
