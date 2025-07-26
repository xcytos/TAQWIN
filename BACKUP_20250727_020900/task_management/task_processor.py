#!/usr/bin/env python3
"""
TAQWIN TOWER - TASK MANAGEMENT SYSTEM
Handles task creation, assignment, and execution tracking
Author: TAQWIN (The Strengthener)
Version: 1.0
"""

import json
import os
from datetime import datetime
from pathlib import Path
from enum import Enum

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"

class TaqwinTaskProcessor:
    def __init__(self):
        self.tower_path = Path("D:\\Ethereal Glow\\TAQWIN_TOWER")
        self.inventory_path = self.tower_path / "OFFICE_INVENTORY"
        self.tasks_path = self.inventory_path / "TASKS_COMPLETED"
        
        # Department mapping for task assignment
        self.departments = {
            "SEO": "FLOOR_2_INTELLIGENCE",
            "CONTENT": "FLOOR_2_INTELLIGENCE", 
            "INNOVATION": "FLOOR_3_INNOVATION",
            "STRATEGY": "FLOOR_4_LEADERSHIP",
            "OPERATIONS": "FLOOR_1_OPERATIONS",
            "MONITORING": "FLOOR_5_MONITORING",
            "RESEARCH": "BASEMENT_INFRASTRUCTURE"
        }
        
        self.task_counter = 0
        self._load_existing_tasks()
    
    def _load_existing_tasks(self):
        """Load existing task counter from system"""
        task_index_file = self.tasks_path / "task_index.json"
        if task_index_file.exists():
            with open(task_index_file, 'r') as f:
                data = json.load(f)
                self.task_counter = data.get("last_task_id", 0)
    
    def create_task(self, title, description, department=None, priority=TaskPriority.MEDIUM, assigned_by="FOUNDER"):
        """Create a new task and assign to appropriate department"""
        self.task_counter += 1
        
        task_id = f"TASK{self.task_counter:04d}"
        
        # Auto-assign department based on keywords if not specified
        if not department:
            department = self._auto_assign_department(title, description)
        
        task = {
            "task_id": task_id,
            "title": title,
            "description": description,
            "department": department,
            "priority": priority.name,
            "status": TaskStatus.PENDING.value,
            "assigned_by": assigned_by,
            "created_at": datetime.now().isoformat(),
            "assigned_agents": self._get_department_agents(department),
            "estimated_duration": self._estimate_duration(description),
            "progress": 0,
            "work_log": []
        }
        
        # Save task to department folder
        self._save_task(task)
        
        # Update task index
        self._update_task_index()
        
        print(f"✅ Task {task_id} created and assigned to {department}")
        return task_id
    
    def _auto_assign_department(self, title, description):
        """Auto-assign department based on task keywords"""
        text = (title + " " + description).lower()
        
        if any(word in text for word in ["seo", "ranking", "keyword", "search"]):
            return "FLOOR_2_INTELLIGENCE"
        elif any(word in text for word in ["innovation", "ai", "development", "research"]):
            return "FLOOR_3_INNOVATION"
        elif any(word in text for word in ["strategy", "planning", "decision", "budget"]):
            return "FLOOR_4_LEADERSHIP"
        elif any(word in text for word in ["monitoring", "analytics", "performance"]):
            return "FLOOR_5_MONITORING"
        elif any(word in text for word in ["content", "writing", "marketing", "brand"]):
            return "FLOOR_1_OPERATIONS"
        else:
            return "FLOOR_1_OPERATIONS"  # Default assignment
    
    def _get_department_agents(self, department):
        """Get agents assigned to a department"""
        agent_mapping = {
            "FLOOR_5_MONITORING": ["Elon Musk", "Nate Silver", "Alan Turing", "Mark Zuckerberg"],
            "FLOOR_4_LEADERSHIP": ["Marcus Aurelius", "Chanakya", "Warren Buffett", "Cleopatra"],
            "FLOOR_3_INNOVATION": ["Nikola Tesla", "Marie Curie", "Leonardo Da Vinci", "Steve Jobs"],
            "FLOOR_2_INTELLIGENCE": ["Sun Tzu", "Rand Fishkin", "Neil Patel", "Brian Dean"],
            "FLOOR_1_OPERATIONS": ["General Patton", "Benjamin Franklin", "Oprah Winfrey", "Maya Angelou"],
            "BASEMENT_INFRASTRUCTURE": ["Charaka", "Rachel Carson", "Paracelsus", "Linus Pauling"]
        }
        return agent_mapping.get(department, [])
    
    def _estimate_duration(self, description):
        """Estimate task duration based on complexity"""
        complexity_keywords = {
            "simple": 1,
            "quick": 1,
            "basic": 2,
            "standard": 3,
            "complex": 5,
            "advanced": 7,
            "comprehensive": 10
        }
        
        description_lower = description.lower()
        for keyword, hours in complexity_keywords.items():
            if keyword in description_lower:
                return f"{hours} hours"
        
        return "3 hours"  # Default estimation
    
    def _save_task(self, task):
        """Save task to appropriate department folder"""
        department_folder = self.tasks_path / task["department"].lower()
        department_folder.mkdir(exist_ok=True)
        
        task_file = department_folder / f"{task['task_id']}.json"
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)
    
    def _update_task_index(self):
        """Update the task index counter"""
        task_index_file = self.tasks_path / "task_index.json"
        index_data = {
            "last_task_id": self.task_counter,
            "total_tasks_created": self.task_counter,
            "last_updated": datetime.now().isoformat()
        }
        with open(task_index_file, 'w') as f:
            json.dump(index_data, f, indent=2)
    
    def update_task_progress(self, task_id, progress, work_notes=""):
        """Update task progress and add work log entry"""
        task_file = self._find_task_file(task_id)
        if not task_file:
            print(f"❌ Task {task_id} not found")
            return False
        
        with open(task_file, 'r') as f:
            task = json.load(f)
        
        # Update progress
        task["progress"] = progress
        
        # Update status based on progress
        if progress >= 100:
            task["status"] = TaskStatus.COMPLETED.value
            task["completed_at"] = datetime.now().isoformat()
        elif progress > 0:
            task["status"] = TaskStatus.IN_PROGRESS.value
        
        # Add work log entry
        work_entry = {
            "timestamp": datetime.now().isoformat(),
            "progress": progress,
            "notes": work_notes,
            "updated_by": "AGENT_SYSTEM"
        }
        task["work_log"].append(work_entry)
        
        # Save updated task
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)
        
        print(f"✅ Task {task_id} updated to {progress}% complete")
        return True
    
    def _find_task_file(self, task_id):
        """Find task file across all departments"""
        for dept_folder in self.tasks_path.iterdir():
            if dept_folder.is_dir():
                task_file = dept_folder / f"{task_id}.json"
                if task_file.exists():
                    return task_file
        return None
    
    def get_pending_tasks(self, department=None):
        """Get all pending tasks, optionally filtered by department"""
        pending_tasks = []
        
        search_folders = [self.tasks_path / department.lower()] if department else [d for d in self.tasks_path.iterdir() if d.is_dir()]
        
        for dept_folder in search_folders:
            if dept_folder.is_dir():
                for task_file in dept_folder.glob("TASK*.json"):
                    with open(task_file, 'r') as f:
                        task = json.load(f)
                        if task["status"] in [TaskStatus.PENDING.value, TaskStatus.IN_PROGRESS.value]:
                            pending_tasks.append(task)
        
        return sorted(pending_tasks, key=lambda x: TaskPriority[x["priority"]].value, reverse=True)
    
    def generate_task_report(self):
        """Generate comprehensive task report"""
        all_tasks = []
        task_stats = {
            "total": 0,
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "blocked": 0
        }
        
        for dept_folder in self.tasks_path.iterdir():
            if dept_folder.is_dir() and not dept_folder.name.endswith('.json'):
                for task_file in dept_folder.glob("TASK*.json"):
                    with open(task_file, 'r') as f:
                        task = json.load(f)
                        all_tasks.append(task)
                        task_stats["total"] += 1
                        task_stats[task["status"].lower()] += 1
        
        report = {
            "report_generated": datetime.now().isoformat(),
            "task_statistics": task_stats,
            "department_breakdown": self._get_department_breakdown(all_tasks),
            "high_priority_tasks": [t for t in all_tasks if t["priority"] == "HIGH" and t["status"] != "COMPLETED"],
            "recent_completions": [t for t in all_tasks if t["status"] == "COMPLETED"][-10:]
        }
        
        # Save report
        report_file = self.inventory_path / "TASKS_COMPLETED" / "task_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _get_department_breakdown(self, tasks):
        """Get task breakdown by department"""
        dept_stats = {}
        for task in tasks:
            dept = task["department"]
            if dept not in dept_stats:
                dept_stats[dept] = {"total": 0, "completed": 0, "pending": 0}
            
            dept_stats[dept]["total"] += 1
            if task["status"] == "COMPLETED":
                dept_stats[dept]["completed"] += 1
            elif task["status"] in ["PENDING", "IN_PROGRESS"]:
                dept_stats[dept]["pending"] += 1
        
        return dept_stats

# Example usage and testing functions
def create_sample_tasks():
    """Create sample tasks for testing"""
    processor = TaqwinTaskProcessor()
    
    sample_tasks = [
        ("SEO Optimization", "Optimize website for Multani Mitti keywords", None, TaskPriority.HIGH),
        ("AI Video Pipeline", "Complete automation of video generation system", None, TaskPriority.CRITICAL),
        ("Market Analysis", "Analyze competitor pricing strategies", None, TaskPriority.MEDIUM),
        ("Content Creation", "Create grandmother wisdom blog series", None, TaskPriority.MEDIUM),
        ("Performance Monitoring", "Set up real-time analytics dashboard", None, TaskPriority.HIGH)
    ]
    
    for title, desc, dept, priority in sample_tasks:
        processor.create_task(title, desc, dept, priority)
    
    print("✅ Sample tasks created successfully")

if __name__ == "__main__":
    # Test the task processor
    create_sample_tasks()
    
    processor = TaqwinTaskProcessor()
    pending = processor.get_pending_tasks()
    print(f"\n📋 {len(pending)} pending tasks found")
    
    # Generate report
    report = processor.generate_task_report()
    print(f"📊 Task report generated: {report['task_statistics']['total']} total tasks")
