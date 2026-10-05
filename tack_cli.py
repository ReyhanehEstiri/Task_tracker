import sys
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"
VALID_STATUSES = ("todo", "in-progress", "done")


def load_tasks():
    """Read tasks from the JSON file. Create the file if it doesn't exist."""
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError
            return data
    except (json.JSONDecodeError, ValueError):
        print(f"Error: {TASKS_FILE} is corrupted or has an invalid format.")
        sys.exit(1)


def save_tasks(tasks):
    """Write tasks to the JSON file."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def parse_id(value):
    try:
        return int(value)
    except ValueError:
        print("Error: ID must be a number.")
        sys.exit(1)


def add_task(description):
    if not description.strip():
        print("Error: Description cannot be empty.")
        return
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now(),
        "updatedAt": now(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")


def update_task(task_id, description):
    if not description.strip():
        print("Error: Description cannot be empty.")
        return
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return
    task["description"] = description
    task["updatedAt"] = now()
    save_tasks(tasks)
    print("Task updated successfully")


def delete_task(task_id):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return
    tasks.remove(task)
    save_tasks(tasks)
    print("Task deleted successfully")


def mark_task(task_id, status):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return
    task["status"] = status
    task["updatedAt"] = now()
    save_tasks(tasks)
    print(f"Task marked as {status}")


def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        print(
            f"[{t['id']}] {t['description']} - {t['status']} "
            f"(created: {t['createdAt']}, updated: {t['updatedAt']})"
        )


def print_usage():
    print("Usage: python task_cli.py <command> [arguments]")
    print("Commands:")
    print('  add "description"')
    print('  update <id> "new description"')
    print("  delete <id>")
    print("  mark-in-progress <id>")
    print("  mark-done <id>")
    print("  list [todo|in-progress|done]")


def main():
    args = sys.argv[1:]

    if not args:
        print_usage()
        return

    command = args[0]

    if command == "add":
        if len(args) != 2:
            print('Usage: add "description"')
            return
        add_task(args[1])

    elif command == "update":
        if len(args) != 3:
            print('Usage: update <id> "new description"')
            return
        update_task(parse_id(args[1]), args[2])

    elif command == "delete":
        if len(args) != 2:
            print("Usage: delete <id>")
            return
        delete_task(parse_id(args[1]))

    elif command == "mark-in-progress":
        if len(args) != 2:
            print("Usage: mark-in-progress <id>")
            return
        mark_task(parse_id(args[1]), "in-progress")

    elif command == "mark-done":
        if len(args) != 2:
            print("Usage: mark-done <id>")
            return
        mark_task(parse_id(args[1]), "done")

    elif command == "list":
        if len(args) == 1:
            list_tasks()
        elif len(args) == 2 and args[1] in VALID_STATUSES:
            list_tasks(args[1])
        else:
            print("Usage: list [todo|in-progress|done]")

    else:
        print(f"Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    main()