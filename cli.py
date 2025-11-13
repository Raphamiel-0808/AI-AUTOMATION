#!/usr/bin/env python3
"""
Daily Task Tracker CLI
Command-line interface for managing tasks and sending email summaries
"""

import argparse
import sys
import os
from datetime import datetime
from task_tracker import TaskTracker
from email_notifier import EmailNotifier

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use system env vars


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Daily Task Tracker - Track your tasks and email summaries to your boss",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a new task
  python cli.py add "Complete project documentation" --priority high

  # Complete a task
  python cli.py complete 1

  # List all tasks
  python cli.py list

  # List only pending tasks
  python cli.py list --status pending

  # Show today's summary
  python cli.py summary

  # Send daily summary email
  python cli.py email boss@company.com

  # Send summary for a specific date
  python cli.py email boss@company.com --date 2025-11-12
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Add task command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument("--priority", choices=["low", "medium", "high"],
                           default="medium", help="Task priority (default: medium)")

    # Complete task command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to complete")

    # List tasks command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", choices=["pending", "completed", "all"],
                            default="all", help="Filter by status (default: all)")
    list_parser.add_argument("--date", help="Filter by date (YYYY-MM-DD)")

    # Delete task command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show daily task summary")
    summary_parser.add_argument("--date", help="Date for summary (YYYY-MM-DD, default: today)")

    # Email command
    email_parser = subparsers.add_parser("email", help="Send daily summary via email")
    email_parser.add_argument("recipient", help="Email address of the recipient")
    email_parser.add_argument("--date", help="Date for summary (YYYY-MM-DD, default: today)")
    email_parser.add_argument("--subject", help="Custom email subject")

    args = parser.parse_args()

    # Show help if no command specified
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize task tracker
    tracker = TaskTracker()

    # Execute command
    if args.command == "add":
        handle_add(tracker, args)
    elif args.command == "complete":
        handle_complete(tracker, args)
    elif args.command == "list":
        handle_list(tracker, args)
    elif args.command == "delete":
        handle_delete(tracker, args)
    elif args.command == "summary":
        handle_summary(tracker, args)
    elif args.command == "email":
        handle_email(tracker, args)


def handle_add(tracker: TaskTracker, args):
    """Handle add task command"""
    task = tracker.add_task(args.description, args.priority)
    print(f"✓ Task added successfully!")
    print(f"  ID: {task['id']}")
    print(f"  Description: {task['description']}")
    print(f"  Priority: {task['priority']}")


def handle_complete(tracker: TaskTracker, args):
    """Handle complete task command"""
    task = tracker.complete_task(args.task_id)
    if task:
        print(f"✓ Task #{args.task_id} marked as completed!")
        print(f"  Description: {task['description']}")
    else:
        print(f"✗ Task #{args.task_id} not found")
        sys.exit(1)


def handle_list(tracker: TaskTracker, args):
    """Handle list tasks command"""
    tasks = tracker.get_tasks(status=args.status if args.status != "all" else None,
                             date=args.date)

    if not tasks:
        print("No tasks found.")
        return

    print(f"\nTasks ({len(tasks)}):")
    print("=" * 80)

    for task in tasks:
        status_symbol = "✓" if task["status"] == "completed" else "○"
        priority_marker = "🔴" if task["priority"] == "high" else "🟡" if task["priority"] == "medium" else "🟢"

        print(f"{status_symbol} [ID: {task['id']}] [{priority_marker}] {task['description']}")
        print(f"  Status: {task['status']} | Created: {task['created_at'][:10]}", end="")

        if task["completed_at"]:
            print(f" | Completed: {task['completed_at'][:10]}")
        else:
            print()
        print("-" * 80)


def handle_delete(tracker: TaskTracker, args):
    """Handle delete task command"""
    if tracker.delete_task(args.task_id):
        print(f"✓ Task #{args.task_id} deleted successfully")
    else:
        print(f"✗ Task #{args.task_id} not found")
        sys.exit(1)


def handle_summary(tracker: TaskTracker, args):
    """Handle summary command"""
    summary = tracker.get_daily_summary(args.date)
    print(summary)


def handle_email(tracker: TaskTracker, args):
    """Handle email command"""
    # Get summary
    summary = tracker.get_daily_summary(args.date)

    # Initialize email notifier from environment variables
    notifier = EmailNotifier.from_env()

    if not notifier:
        print("\n✗ Email configuration not found!")
        print("\nPlease set the following environment variables:")
        print("  - SMTP_SERVER (e.g., smtp.gmail.com)")
        print("  - SMTP_PORT (e.g., 587)")
        print("  - SENDER_EMAIL (your email address)")
        print("  - SENDER_PASSWORD (your email password or app password)")
        print("\nOr create a .env file with these variables.")
        sys.exit(1)

    # Send email
    print(f"\nSending email to {args.recipient}...")
    success = notifier.send_daily_summary(args.recipient, summary, args.subject)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
