#!/usr/bin/env python3

import sys
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

# Ensure file exists
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "w") as f:
        json.dump([], f, indent=4)

def load_tasks():
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add":
        print("Add command coming next...")

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()