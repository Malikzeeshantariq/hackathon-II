# Phase I - In-Memory Console Todo Application

A minimal viable console-based todo application built with Python 3.13 that stores tasks entirely in memory.

## Features

- ✅ Add tasks with title and description
- ✅ View all tasks with status indicators
- ✅ Mark tasks as complete/incomplete (toggle)
- ✅ Update task title and/or description
- ✅ Delete tasks by ID
- ✅ Interactive command-loop interface

## Requirements

- Python 3.13 or higher
- No external dependencies (stdlib only)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd hackathon-II

# Checkout the feature branch
git checkout 001-phase-i-console-todo
```

## Usage

```bash
# Run the application
python3 src/main.py
```

### Available Commands

- `add` - Add a new task (prompts for title and description)
- `list` - Display all tasks
- `complete <id>` - Toggle task completion status
- `update <id>` - Update task title and/or description
- `delete <id>` - Delete a task
- `help` - Show available commands
- `exit` or `quit` - Exit the application

### Example Session

```
> add
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
Task added successfully!

TODO LIST
=========
[1] [ ] Buy groceries
    Milk, eggs, bread

> complete 1

TODO LIST
=========
[1] [✓] Buy groceries
    Milk, eggs, bread

> exit
Goodbye!
```

## Project Structure

```
hackathon-II/
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry point and CLI loop
│   └── todo.py          # Task model and TodoManager
├── specs/               # Feature specifications and design docs
├── .gitignore
├── README.md
└── pyproject.toml
```

## Success Criteria

- Add a task and see it in list < 10 seconds
- Complete all 5 operations within 2 minutes
- Handle 100 tasks without performance issues
- Clear error messages, no crashes
- Toggle task status without losing data

## Development

This project follows Spec-Driven Development methodology. All code is generated from specifications located in `specs/001-phase-i-console-todo/`.

- **Spec**: `specs/001-phase-i-console-todo/spec.md`
- **Plan**: `specs/001-phase-i-console-todo/plan.md`
- **Tasks**: `specs/001-phase-i-console-todo/tasks.md`

## Phase Roadmap

- **Phase I** (Current): In-memory console application ✅
- **Phase II**: File-based persistence
- **Phase III**: Natural language chatbot interface
- **Phase IV**: Local Kubernetes deployment (Minikube)
- **Phase V**: Production Kubernetes (DigitalOcean)

## License

Hackathon II Project - The Evolution of Todo
