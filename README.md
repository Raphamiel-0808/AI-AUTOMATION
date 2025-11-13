# AI-AUTOMATION

This repo is for workflow automation

## Daily Task Tracker

A Python-based task tracking application that helps you manage daily tasks and automatically send email summaries to your boss or team.

### Features

- Add, complete, and manage tasks with priorities
- Track tasks by date and status
- Generate daily summaries
- Automatically email task summaries to recipients
- Simple CLI interface
- JSON-based storage (no database required)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-AUTOMATION
   ```

2. **Install dependencies (optional)**
   ```bash
   pip install -r requirements.txt
   ```

   Note: The app works with built-in Python libraries. `python-dotenv` is optional for easier `.env` file management.

3. **Set up email configuration**

   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your email credentials:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   USE_TLS=true
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   ```

   **For Gmail users:**
   - Enable 2-factor authentication
   - Generate an App Password at: https://myaccount.google.com/apppasswords
   - Use the app password (not your regular password)

### Usage

#### Add a Task

```bash
python cli.py add "Complete project documentation" --priority high
```

Priorities: `low`, `medium` (default), `high`

#### Complete a Task

```bash
python cli.py complete 1
```

#### List Tasks

```bash
# List all tasks
python cli.py list

# List only pending tasks
python cli.py list --status pending

# List completed tasks
python cli.py list --status completed

# List tasks for a specific date
python cli.py list --date 2025-11-13
```

#### View Daily Summary

```bash
# Today's summary
python cli.py summary

# Summary for a specific date
python cli.py summary --date 2025-11-12
```

#### Send Email Summary

```bash
# Send today's summary to your boss
python cli.py email boss@company.com

# Send summary for a specific date
python cli.py email boss@company.com --date 2025-11-12

# Custom subject line
python cli.py email boss@company.com --subject "Weekly Task Update"
```

#### Delete a Task

```bash
python cli.py delete 1
```

### Automation

To automatically send daily summaries, set up a cron job (Linux/Mac) or Task Scheduler (Windows):

**Linux/Mac (crontab):**

```bash
# Send email every day at 5 PM
0 17 * * * cd /path/to/AI-AUTOMATION && python cli.py email boss@company.com
```

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "Daily" at your preferred time
4. Action: Start a program
   - Program: `python`
   - Arguments: `cli.py email boss@company.com`
   - Start in: `C:\path\to\AI-AUTOMATION`

### File Structure

```
AI-AUTOMATION/
├── cli.py              # Command-line interface
├── task_tracker.py     # Task management logic
├── email_notifier.py   # Email sending functionality
├── tasks.json          # Task storage (auto-generated)
├── .env                # Email configuration (create from .env.example)
├── .env.example        # Example configuration file
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

### Example Workflow

```bash
# Start your day - add tasks
python cli.py add "Review pull requests" --priority high
python cli.py add "Update documentation" --priority medium
python cli.py add "Team meeting at 2 PM" --priority high

# Throughout the day - complete tasks
python cli.py complete 1
python cli.py complete 3

# End of day - view summary
python cli.py summary

# Send summary to boss
python cli.py email boss@company.com
```

### Troubleshooting

**Email not sending:**
- Check your email credentials in `.env`
- For Gmail, ensure you're using an App Password, not your regular password
- Check that your SMTP server and port are correct
- Try disabling antivirus/firewall temporarily

**"Module not found" errors:**
- Ensure you're in the correct directory
- Install dependencies: `pip install -r requirements.txt`

**Tasks not saving:**
- Check write permissions in the directory
- Ensure `tasks.json` isn't locked by another process

### Security Notes

- Never commit your `.env` file to version control
- Use app-specific passwords instead of main account passwords
- Keep your `tasks.json` private if it contains sensitive information

### Support

For issues or questions, please open an issue in the repository.

### License

MIT License
