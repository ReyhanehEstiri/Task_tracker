# Task Tracker CLI


A simple command line app to manage tasks, built with pure Python.

This project is based on the [Task Tracker](https://roadmap.sh/projects/task-tracker) challenge from roadmap.sh.


## Usage

```bash
# Add a task
python task_cli.py add "Buy groceries"

# Update or delete a task
python task_cli.py update 1 "Buy groceries and cook dinner"
python task_cli.py delete 1

# Change status
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 1

# List tasks
python task_cli.py list
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```

## Task properties

| Field         | Description                                |
|---------------|--------------------------------------------|
| `id`          | Unique identifier                          |
| `description` | Short description of the task              |
| `status`      | `todo`, `in-progress`, or `done`           |
| `createdAt`   | Date and time the task was created         |
| `updatedAt`   | Date and time the task was last updated    |

Tasks are stored in `tasks.json` in the current directory. The file is created automatically if it does not exist.
