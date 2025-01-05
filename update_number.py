#!/usr/bin/env python3
import os
import random
import subprocess
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def read_number():
    with open('number.txt', 'r') as f:
        return int(f.read().strip())


def write_number(num):
    with open('number.txt', 'w') as f:
        f.write(str(num))


def git_commit():
    # Stage the changes
    subprocess.run(['git', 'add', 'number.txt'])

    # Create commit with current date
    date = datetime.now().strftime('%Y-%m-%d')
    commit_message = f"Update number: {date}"
    subprocess.run(['git', 'commit', '-m', commit_message])


def git_push():
    # Push the committed changes to GitHub
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)


def schedule_task_with_random_time():
    """Schedule the script to run at a random time using Windows Task Scheduler."""
    # Generate random hour (0-23) and minute (0-59)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)

    # Task name
    task_name = "UpdateNumberTask"

    # Path to Python executable and the script
    python_path = subprocess.run(["where", "python"], capture_output=True, text=True).stdout.strip()
    script_path = os.path.join(script_dir, "update_number.py")

    # Command to create the task
    schedule_command = (
        f"schtasks /Create /F /SC DAILY /ST {random_hour:02d}:{random_minute:02d} "
        f"/TN {task_name} /TR \"{python_path} {script_path}\""
    )

    # Run the command
    result = subprocess.run(schedule_command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Task scheduled successfully to run at {random_hour:02d}:{random_minute:02d} tomorrow.")
    else:
        print("Error scheduling task:")
        print(result.stderr)


def main():
    try:
        current_number = read_number()
        new_number = current_number + 1
        write_number(new_number)

        git_commit()
        git_push()

        schedule_task_with_random_time()

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
