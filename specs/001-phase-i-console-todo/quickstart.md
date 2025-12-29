# Quick Start Guide: Phase I - In-Memory Console Todo Application

**Feature**: 001-phase-i-console-todo
**Date**: 2025-12-30
**Target Users**: Developers, testers, and evaluators of Phase I

## Prerequisites

### System Requirements

- **Operating System**: WSL 2 with Ubuntu 22.04 (Windows) or any Linux/macOS
- **Python**: Version 3.13 or higher
- **Package Manager**: UV (recommended) or pip
- **Terminal**: Any terminal or console application

### Verify Python Installation

```bash
python3 --version
# Expected output: Python 3.13.x or higher
```

If Python 3.13+ is not installed:
```bash
# Ubuntu/Debian (WSL 2)
sudo apt update
sudo apt install python3.13

# macOS (Homebrew)
brew install python@3.13
```

### Install UV Package Manager (Optional but Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd hackathon-II
```

### Step 2: Checkout Feature Branch

```bash
git checkout 001-phase-i-console-todo
```

### Step 3: Verify Project Structure

```bash
ls -la src/
# Expected output:
# main.py
# todo.py
# __init__.py
```

### Step 4: No Dependencies to Install

Phase I uses Python standard library only - no external dependencies required!

```bash
# No pip install or uv sync needed for Phase I
```

---

## Running the Application

### Basic Usage

```bash
# From project root directory
python3 src/main.py
```

### Expected Startup Output

```
TODO LIST - Phase I
===================
Type 'help' for available commands.

>
```

---

## Using the Application

### Available Commands

| Command | Syntax | Description | Example |
|---------|--------|-------------|---------|
| `help` | `help` | Display available commands | `help` |
| `add` | `add` | Add a new task (prompts for title and description) | `add` |
| `list` | `list` | Display all tasks | `list` |
| `complete` | `complete <id>` | Toggle task completion status | `complete 1` |
| `update` | `update <id>` | Update task title and/or description | `update 2` |
| `delete` | `delete <id>` | Delete a task by ID | `delete 3` |
| `exit` / `quit` | `exit` or `quit` | Exit the application | `exit` |

### Command Examples

#### 1. Add a Task

```
> add
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
Task added successfully!

TODO LIST
=========
[1] [ ] Buy groceries
    Milk, eggs, bread

>
```

#### 2. List Tasks

```
> list

TODO LIST
=========
[1] [ ] Buy groceries
    Milk, eggs, bread

[2] [ ] Call dentist
    Schedule appointment

[3] [ ] Finish report

>
```

#### 3. Mark Task Complete

```
> complete 1

TODO LIST
=========
[1] [✓] Buy groceries
    Milk, eggs, bread

[2] [ ] Call dentist
    Schedule appointment

[3] [ ] Finish report

>
```

#### 4. Update a Task

```
> update 2
Enter new title (press Enter to keep current):
Enter new description (press Enter to keep current): Appointment on Friday at 2 PM
Task updated successfully!

TODO LIST
=========
[1] [✓] Buy groceries
    Milk, eggs, bread

[2] [ ] Call dentist
    Appointment on Friday at 2 PM

[3] [ ] Finish report

>
```

#### 5. Delete a Task

```
> delete 1
Task deleted successfully!

TODO LIST
=========
[2] [ ] Call dentist
    Appointment on Friday at 2 PM

[3] [ ] Finish report

>
```

#### 6. Exit Application

```
> exit
Goodbye!
```

---

## Testing the Application

### Manual Test Scenarios

#### Test Scenario 1: Basic CRUD Operations

1. Start application
2. Add 3 tasks with different titles and descriptions
3. List all tasks → verify all 3 appear
4. Mark task 2 as complete → verify status changes to [✓]
5. Update task 1 title → verify title changes
6. Delete task 3 → verify it's removed
7. List tasks → verify only tasks 1 and 2 remain
8. Exit application

**Expected Result**: All operations complete without errors, task list displays correctly.

#### Test Scenario 2: Edge Cases

1. Start application with empty list
2. List tasks → verify friendly message "No tasks yet. Add one to get started!"
3. Add task with title only (no description) → verify task created
4. Try to complete task ID 99 (doesn't exist) → verify error message "Task ID 99 not found"
5. Try to enter invalid command "xyz" → verify error message "Unknown command. Type 'help' for available commands."
6. Add task, then toggle it complete, then incomplete → verify toggle behavior works

**Expected Result**: All edge cases handled gracefully, no crashes.

#### Test Scenario 3: Validation

1. Try to add task with empty title → verify rejection or re-prompt
2. Add task with very long title (300+ characters) → verify error or truncation
3. Try to complete task with non-numeric ID ("abc") → verify error message
4. Add 100 tasks → verify performance remains under 1 second for list display

**Expected Result**: All validation rules enforced, clear error messages.

---

## Troubleshooting

### Problem: "python3: command not found"

**Solution**: Python 3 is not installed or not in PATH.
```bash
# Check if python3 is installed
which python3

# If not found, install Python 3.13+
sudo apt install python3.13  # Ubuntu/Debian
brew install python@3.13     # macOS
```

### Problem: "ModuleNotFoundError" or Import Errors

**Solution**: Ensure you're running from project root and src/ directory exists.
```bash
# Verify current directory
pwd
# Should be: /path/to/hackathon-II

# Verify src/ exists
ls -la src/
```

### Problem: Application Exits Immediately

**Solution**: Check for syntax errors or exceptions in code.
```bash
# Run with verbose error output
python3 -u src/main.py
```

### Problem: Unicode Characters Not Displaying (✓ appears as ?)

**Solution**: Set terminal encoding to UTF-8.
```bash
# Check current encoding
locale

# Set UTF-8 encoding (add to ~/.bashrc or ~/.zshrc)
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

### Problem: Tasks Not Persisting After Exit

**Expected Behavior**: This is correct for Phase I! Tasks are stored in memory only and are lost when the application exits. Persistence will be added in Phase II.

---

## Development Workflow

### Running Tests (Optional for Phase I)

```bash
# If pytest tests are implemented
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Code Style Check

```bash
# Check PEP8 compliance (if tools installed)
flake8 src/
black --check src/
mypy src/
```

### Git Workflow

```bash
# View current branch
git branch

# View generated files
git status

# Commit changes (if needed)
git add .
git commit -m "Implement Phase I console todo app"

# Push to remote
git push origin 001-phase-i-console-todo
```

---

## Success Criteria Validation

### Validate Against Success Criteria

- **SC-001**: Add a new task and see it in list < 10 seconds → ✅
- **SC-002**: Complete all 5 operations within 2 minutes → ✅
- **SC-003**: Add 100 tasks, list displays < 1 second → ✅
- **SC-004**: Try invalid operations, get clear errors, no crashes → ✅
- **SC-005**: Perform 20 consecutive operations without crash → ✅
- **SC-006**: Task list shows ID, title, description, status clearly → ✅
- **SC-007**: Toggle task status without losing data → ✅

### Performance Benchmarking

```bash
# Time the list operation with 100 tasks
time python3 -c "
from src.todo import TodoManager
tm = TodoManager()
for i in range(100):
    tm.add_task(f'Task {i}', f'Description {i}')
tm.list_tasks()
"
```

Expected output: < 1 second total time

---

## Next Steps

### After Phase I Completion

1. **Create Demo Video** (≤ 90 seconds)
   - Show adding tasks
   - Show marking complete
   - Show updating and deleting
   - Highlight clean interface and error handling

2. **Proceed to Phase II** (File Persistence)
   - Run `/sp.specify` for Phase II feature
   - Add file-based storage (JSON)
   - Maintain backward compatibility with Phase I

3. **Submit Phase I**
   - Public GitHub repository
   - Demo video
   - README.md (this file or root README)
   - Complete spec/plan/task documentation

---

## Additional Resources

- **Feature Specification**: `specs/001-phase-i-console-todo/spec.md`
- **Implementation Plan**: `specs/001-phase-i-console-todo/plan.md`
- **Data Model**: `specs/001-phase-i-console-todo/data-model.md`
- **Research Notes**: `specs/001-phase-i-console-todo/research.md`
- **Constitution**: `.specify/memory/constitution.md`

---

## Support

For issues or questions:
1. Check existing documentation in `specs/001-phase-i-console-todo/`
2. Review constitution and workflow guidelines in `.specify/`
3. Consult hackathon organizers or project maintainers

---

**Quick Start Complete!** You're ready to run and test the Phase I Console Todo Application.
