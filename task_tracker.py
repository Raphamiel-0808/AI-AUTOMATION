"""
Daily Task Tracker Module
Handles task creation, completion, and retrieval operations
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class TaskTracker:
    """Manages daily tasks and their completion status"""

    def __init__(self, data_file: str = "tasks.json"):
        """
        Initialize the task tracker

        Args:
            data_file: Path to the JSON file storing tasks
        """
        self.data_file = data_file
        self.tasks = self._load_tasks()

    def _load_tasks(self) -> List[Dict]:
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save_tasks(self) -> None:
        """Save tasks to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, description: str, priority: str = "medium") -> Dict:
        """
        Add a new task

        Args:
            description: Task description
            priority: Task priority (low, medium, high)

        Returns:
            The created task dictionary
        """
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        self.tasks.append(task)
        self._save_tasks()
        return task

    def complete_task(self, task_id: int) -> Optional[Dict]:
        """
        Mark a task as completed

        Args:
            task_id: ID of the task to complete

        Returns:
            The updated task or None if not found
        """
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                self._save_tasks()
                return task
        return None

    def get_tasks(self, status: Optional[str] = None, date: Optional[str] = None) -> List[Dict]:
        """
        Get tasks filtered by status and/or date

        Args:
            status: Filter by status (pending, completed, all)
            date: Filter by date (ISO format YYYY-MM-DD)

        Returns:
            List of tasks matching the filters
        """
        filtered_tasks = self.tasks

        if status and status != "all":
            filtered_tasks = [t for t in filtered_tasks if t["status"] == status]

        if date:
            filtered_tasks = [
                t for t in filtered_tasks
                if t["created_at"].startswith(date) or
                   (t["completed_at"] and t["completed_at"].startswith(date))
            ]

        return filtered_tasks

    def get_today_tasks(self) -> Dict[str, List[Dict]]:
        """
        Get today's tasks organized by status

        Returns:
            Dictionary with 'completed' and 'pending' task lists
        """
        today = datetime.now().strftime("%Y-%m-%d")
        all_today_tasks = self.get_tasks(date=today)

        return {
            "completed": [t for t in all_today_tasks if t["status"] == "completed"],
            "pending": [t for t in all_today_tasks if t["status"] == "pending"]
        }

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task

        Args:
            task_id: ID of the task to delete

        Returns:
            True if deleted, False if not found
        """
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                self._save_tasks()
                return True
        return False

    def get_daily_summary(self, date: Optional[str] = None) -> str:
        """
        Generate a formatted daily summary

        Args:
            date: Date to summarize (defaults to today)

        Returns:
            Formatted string summary
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        tasks = self.get_tasks(date=date)
        completed = [t for t in tasks if t["status"] == "completed"]
        pending = [t for t in tasks if t["status"] == "pending"]

        summary = f"Daily Task Summary - {date}\n"
        summary += "=" * 50 + "\n\n"

        summary += f"Completed Tasks ({len(completed)}):\n"
        summary += "-" * 50 + "\n"
        if completed:
            for task in completed:
                priority_marker = "🔴" if task["priority"] == "high" else "🟡" if task["priority"] == "medium" else "🟢"
                summary += f"  ✓ [{priority_marker}] {task['description']}\n"
        else:
            summary += "  No tasks completed today.\n"

        summary += "\n"
        summary += f"Pending Tasks ({len(pending)}):\n"
        summary += "-" * 50 + "\n"
        if pending:
            for task in pending:
                priority_marker = "🔴" if task["priority"] == "high" else "🟡" if task["priority"] == "medium" else "🟢"
                summary += f"  ○ [{priority_marker}] {task['description']}\n"
        else:
            summary += "  All tasks completed!\n"

        return summary
