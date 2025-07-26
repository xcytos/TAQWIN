#!/usr/bin/env python3
"""
TAQWIN TOWER - GIT INTEGRATION MANAGER
Automated Git operations for continuous deployment
Author: TAQWIN (The Strengthener)
Version: 1.0
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
import sys

class TaqwinGitManager:
    def __init__(self):
        self.base_path = Path("D:\\Ethereal Glow")
        self.git_log_path = self.base_path / "TAQWIN_TOWER" / "OFFICE_INVENTORY" / "GIT_OPERATIONS_LOG.json"
        self.operations_log = []
        
        # Ensure log directory exists
        self.git_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing log
        self.load_operations_log()
        
    def load_operations_log(self):
        """Load existing Git operations log"""
        if self.git_log_path.exists():
            try:
                with open(self.git_log_path, 'r', encoding='utf-8') as f:
                    self.operations_log = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load Git log: {e}")
                self.operations_log = []
        else:
            self.operations_log = []
    
    def save_operations_log(self):
        """Save Git operations log"""
        try:
            with open(self.git_log_path, 'w', encoding='utf-8') as f:
                json.dump(self.operations_log, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving Git log: {e}")
    
    def log_operation(self, operation, details, success=True):
        """Log Git operation"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details,
            "success": success,
            "cwd": str(self.base_path)
        }
        
        self.operations_log.append(log_entry)
        
        # Keep only last 100 operations
        if len(self.operations_log) > 100:
            self.operations_log = self.operations_log[-100:]
        
        self.save_operations_log()
        
        status = "SUCCESS" if success else "FAILED"
        print(f"[{status}] {operation}: {details}")
    
    def run_git_command(self, command, capture_output=True):
        """Run Git command safely"""
        try:
            result = subprocess.run(
                command,
                cwd=str(self.base_path),
                capture_output=capture_output,
                text=True,
                shell=True
            )
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except Exception as e:
            return False, "", str(e)
    
    def check_git_status(self):
        """Check Git repository status"""
        success, stdout, stderr = self.run_git_command("git status --porcelain")
        
        if not success:
            self.log_operation("STATUS_CHECK", f"Failed: {stderr}", False)
            return False, []
        
        # Parse changed files
        changed_files = []
        if stdout.strip():
            for line in stdout.strip().split('\n'):
                if line.strip():
                    status = line[:2]
                    filename = line[3:]
                    changed_files.append({"status": status, "file": filename})
        
        self.log_operation("STATUS_CHECK", f"Found {len(changed_files)} changed files")
        return True, changed_files
    
    def add_all_changes(self):
        """Add all changes to staging"""
        success, stdout, stderr = self.run_git_command("git add .")
        
        if success:
            self.log_operation("ADD_CHANGES", "All changes staged successfully")
        else:
            self.log_operation("ADD_CHANGES", f"Failed: {stderr}", False)
        
        return success
    
    def commit_changes(self, message):
        """Commit changes with message"""
        # Escape quotes in commit message
        safe_message = message.replace('"', '\\"')
        
        success, stdout, stderr = self.run_git_command(f'git commit -m "{safe_message}"')
        
        if success:
            self.log_operation("COMMIT", f"Committed: {message}")
        else:
            self.log_operation("COMMIT", f"Failed: {stderr}", False)
        
        return success
    
    def push_changes(self, branch="main"):
        """Push changes to remote repository"""
        success, stdout, stderr = self.run_git_command(f"git push origin {branch}")
        
        if success:
            self.log_operation("PUSH", f"Pushed to {branch} successfully")
        else:
            self.log_operation("PUSH", f"Failed: {stderr}", False)
        
        return success
    
    def generate_smart_commit_message(self, changed_files):
        """Generate intelligent commit message based on changes"""
        if not changed_files:
            return "Update: General system maintenance"
        
        # Analyze file types and changes
        categories = {
            "python": 0,
            "docs": 0,
            "config": 0,
            "video": 0,
            "intelligence": 0,
            "tower": 0
        }
        
        for file_info in changed_files:
            filename = file_info["file"].lower()
            
            if filename.endswith('.py'):
                categories["python"] += 1
            elif filename.endswith(('.md', '.txt', '.json')):
                categories["docs"] += 1
            elif 'video' in filename:
                categories["video"] += 1
            elif 'intelligence' in filename or 'web-intelligence' in filename:
                categories["intelligence"] += 1
            elif 'taqwin_tower' in filename or 'office_inventory' in filename:
                categories["tower"] += 1
            else:
                categories["config"] += 1
        
        # Generate message based on primary category
        primary = max(categories, key=categories.get)
        total_files = len(changed_files)
        
        messages = {
            "python": f"🐍 TAQWIN Tower: Enhanced Python automation systems ({total_files} files)",
            "docs": f"📚 TAQWIN Documentation: Strategic intelligence updates ({total_files} files)",
            "video": f"🎬 AI Video System: Advanced generation capabilities ({total_files} files)", 
            "intelligence": f"🧠 Web Intelligence: Enhanced research and analysis ({total_files} files)",
            "tower": f"🏢 TAQWIN Tower: Office operations and agent deployment ({total_files} files)",
            "config": f"⚙️ System Configuration: Infrastructure and setup updates ({total_files} files)"
        }
        
        return messages.get(primary, f"🔄 TAQWIN System Update: Multi-component enhancements ({total_files} files)")
    
    def full_deployment_commit(self, custom_message=None):
        """Perform complete Git deployment"""
        print("\n🚀 **TAQWIN GIT DEPLOYMENT INITIATED**")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Check status
        success, changed_files = self.check_git_status()
        if not success:
            print("❌ Failed to check Git status")
            return False
        
        if not changed_files:
            print("✅ No changes to commit")
            return True
        
        print(f"📄 Found {len(changed_files)} changed files:")
        for file_info in changed_files[:10]:  # Show first 10
            print(f"   {file_info['status']} {file_info['file']}")
        
        if len(changed_files) > 10:
            print(f"   ... and {len(changed_files) - 10} more files")
        
        # Add changes
        if not self.add_all_changes():
            print("❌ Failed to add changes")
            return False
        
        # Generate or use commit message
        if custom_message:
            commit_message = custom_message
        else:
            commit_message = self.generate_smart_commit_message(changed_files)
        
        print(f"\n💬 Commit Message: {commit_message}")
        
        # Commit changes
        if not self.commit_changes(commit_message):
            print("❌ Failed to commit changes")
            return False
        
        # Push changes
        if not self.push_changes():
            print("❌ Failed to push changes")
            return False
        
        print("\n🎉 **GIT DEPLOYMENT COMPLETED SUCCESSFULLY**")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        return True
    
    def get_deployment_summary(self):
        """Get summary of recent Git operations"""
        recent_ops = self.operations_log[-10:] if self.operations_log else []
        
        summary = {
            "total_operations": len(self.operations_log),
            "recent_operations": recent_ops,
            "last_successful_push": None,
            "last_commit": None
        }
        
        # Find last successful operations
        for op in reversed(self.operations_log):
            if op["operation"] == "PUSH" and op["success"] and not summary["last_successful_push"]:
                summary["last_successful_push"] = op
            elif op["operation"] == "COMMIT" and op["success"] and not summary["last_commit"]:
                summary["last_commit"] = op
        
        return summary

def main():
    """Main Git management function"""
    git_manager = TaqwinGitManager()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "status":
            success, changed_files = git_manager.check_git_status()
            if success:
                print(f"Changed files: {len(changed_files)}")
                for file_info in changed_files:
                    print(f"  {file_info['status']} {file_info['file']}")
            else:
                print("Failed to get status")
        
        elif command == "deploy":
            custom_message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
            git_manager.full_deployment_commit(custom_message)
        
        elif command == "summary":
            summary = git_manager.get_deployment_summary()
            print(json.dumps(summary, indent=2))
        
        else:
            print("Usage: python taqwin_git_manager.py [status|deploy|summary] [message]")
    
    else:
        # Interactive mode
        git_manager.full_deployment_commit()

if __name__ == "__main__":
    main()
