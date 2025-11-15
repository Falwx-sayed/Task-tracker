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

def add_task(description):
    tasks = load_tasks()
    new_id = 1 if len(tasks) == 0 else tasks[-1]["id"] + 1
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "created_at":now,
        "updatedAt": now
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added: {description} (ID: {new_id})")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    for task in tasks:
        print(f"[{task['id']}] {task['description']} - {task['status']} (Created: {task['created_at']}, Updated: {task['updatedAt']})")

def list_tasks_by_status(status):
    tasks = load_tasks()
    filtered_tasks = [task for task in tasks if task['status'] == status]
    
    if not filtered_tasks:
        print(f"No tasks with status '{status}' found.")
        return
    
    for task in filtered_tasks:
        print(f"[{task['id']}] {task['description']} - {task['status']} (Created: {task['created_at']}, Updated: {task['updatedAt']})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    found = False

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found = True
            break

    if not found:
        print(f"Task with ID {task_id} not found.")
        return

    save_tasks(tasks)
    print(f"Task {task_id} updated successfully.")

def mark_task(task_id, status):
    tasks = load_tasks()
    found = False

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found = True
            break

    if not found:
        print(f"Task with ID {task_id} not found.")
        return

    save_tasks(tasks)
    print(f"Task {task_id} marked as {status}.")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(new_tasks) == len(tasks):
        print(f"Task with ID {task_id} not found.")
        return

    save_tasks(new_tasks)
    print(f"Task {task_id} deleted successfully.")


def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Missing task description")
            return

        description = " ".join(sys.argv[2:])
        add_task(description)

    elif command == "list":
        # If no status passed: list all
        if len(sys.argv) == 2:
            list_tasks()
            return

        status = sys.argv[2].lower()

        valid_statuses = ["todo", "done", "in-progress"]

        if status not in valid_statuses:
            print("Invalid status. Use: todo | done | in-progress")
            return

        list_tasks_by_status(status)

    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: task-cli update <id> <new description>")
            return

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        new_description = " ".join(sys.argv[3:])
        update_task(task_id, new_description)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: task-cli delete <id>")
            return

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        delete_task(task_id)

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-in-progress <id>")
            return

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        mark_task(task_id, "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-done <id>")
            return

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        mark_task(task_id, "done")



    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()