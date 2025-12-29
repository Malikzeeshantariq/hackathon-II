# Data Model: Phase I - In-Memory Console Todo Application

**Feature**: 001-phase-i-console-todo
**Date**: 2025-12-30
**Purpose**: Define entity models, relationships, and validation rules

## Overview

The Phase I application uses a simple single-entity data model. All data resides in memory using Python's built-in list data structure. No database or file persistence is involved in Phase I.

## Entities

### Task

**Description**: Represents a single todo item with a title, description, completion status, and unique identifier.

**Source Requirement**: FR-001 (add tasks), FR-002 (unique IDs), FR-003 (display with status), Spec "Key Entities" section

**Attributes**:

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | int | Yes | Auto-assigned | > 0, unique, auto-incrementing | Unique identifier for the task |
| `title` | str | Yes | (none) | 1-200 characters, non-empty | Short description of the task |
| `description` | str | No | "" (empty string) | 0-1000 characters | Detailed information about the task |
| `completed` | bool | Yes | False | True or False | Completion status (incomplete or complete) |

**Python Implementation**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents a todo task with title, description, and completion status."""
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

**Validation Rules**:
- **ID Validation**:
  - Must be a positive integer (> 0)
  - Must be unique across all tasks
  - Auto-assigned by TodoManager, never manually set by user
  - Never reused even after task deletion

- **Title Validation**:
  - Cannot be empty string or whitespace only
  - Maximum length: 200 characters
  - Minimum length: 1 character (after trimming)
  - Should be trimmed of leading/trailing whitespace before storage

- **Description Validation**:
  - Can be empty string (optional field)
  - Maximum length: 1000 characters
  - Should be trimmed of leading/trailing whitespace before storage

- **Completed Validation**:
  - Must be boolean (True or False)
  - Cannot be null or undefined

**Invariants**:
- Once created, a task's ID never changes
- ID sequence is strictly incrementing (next ID = max existing ID + 1)
- Tasks are immutable except for title, description, and completed fields
- Deleted tasks do not leave "gaps" that get reused in ID sequence

---

## State Transitions

### Task Lifecycle States

```
[Created] ---> [Incomplete] ---> [Complete]
                    ^                |
                    |________________|
                         (toggle)
```

**State Definitions**:
1. **Created**: Task is instantiated with `completed=False`
2. **Incomplete**: Task exists with `completed=False` (default state)
3. **Complete**: Task exists with `completed=True`

**Transitions**:
- **Create** (User adds task): → Incomplete state
- **Toggle to Complete** (User marks complete): Incomplete → Complete
- **Toggle to Incomplete** (User marks incomplete): Complete → Incomplete
- **Update** (User modifies title/description): No state change, fields updated in-place
- **Delete** (User removes task): Task removed from storage, no longer exists

**Business Rules**:
- Tasks can transition between Incomplete and Complete unlimited times
- Updating title/description does not affect completion status
- Deleting a task is permanent (no "soft delete" in Phase I)
- Task state persists only for current session (lost on application exit)

---

## Relationships

**Phase I has no entity relationships** - only a single Task entity exists.

**Future Phases** (for reference):
- Phase II+: May introduce User entity (one-to-many: User has many Tasks)
- Phase III+: May introduce Category or Tag entities (many-to-many: Task has many Tags)

---

## Storage Model

### In-Memory Storage

**Container**: Python `list` containing `Task` instances

**Structure**:
```python
tasks: list[Task] = []
```

**Storage Operations**:

| Operation | Method | Complexity | Description |
|-----------|--------|------------|-------------|
| Create | `tasks.append(new_task)` | O(1) amortized | Add new task to end of list |
| Read All | `for task in tasks` | O(n) | Iterate all tasks for display |
| Read One | `next((t for t in tasks if t.id == id), None)` | O(n) | Find task by ID (linear search) |
| Update | `task.title = new_title` (in-place) | O(1) | Modify task fields directly |
| Delete | `tasks.remove(task)` | O(n) | Remove task from list |

**ID Management**:
- Maintain separate `next_id` counter (int) starting at 1
- Increment after each task creation
- Never decrement or reuse IDs

**Concurrency**: Not applicable (single-user, single-session, single-threaded)

**Capacity Limits**:
- Soft limit: 100 tasks (per SC-003 performance requirement)
- Hard limit: Python list capacity (~2^63 items, effectively unlimited)
- Memory: ~1KB per task (rough estimate), 100 tasks ≈ 100KB << 100MB constraint

---

## Data Validation

### Input Validation Matrix

| Field | Validation Rule | Error Message | When Validated |
|-------|----------------|---------------|----------------|
| title (create) | Non-empty after trim | "Title cannot be empty." | Before task creation |
| title (create) | Length 1-200 chars | "Title too long (max 200 characters)." | Before task creation |
| title (update) | Non-empty after trim | "Title cannot be empty." | Before update |
| title (update) | Length 1-200 chars | "Title too long (max 200 characters)." | Before update |
| description (create/update) | Length 0-1000 chars | "Description too long (max 1000 characters)." | Before creation/update |
| id (all operations) | Exists in task list | "Task ID {id} not found." | Before any ID-based operation |
| id (all operations) | Is numeric | "Invalid ID. Please enter a number." | During input parsing |
| command | In valid command list | "Unknown command. Type 'help' for available commands." | During command parsing |

### Edge Case Handling

| Edge Case | Behavior | Rationale |
|-----------|----------|-----------|
| Empty task list | Display "No tasks yet. Add one to get started!" | FR-012, user-friendly |
| Whitespace-only title | Reject as empty after trim | Prevent meaningless tasks |
| Empty description | Allow (description is optional) | FR-001, description is optional |
| Very long title (>200 chars) | Truncate or reject with error message | Prevent display issues, memory bounds |
| Very long description (>1000 chars) | Truncate or reject with error message | Prevent excessive memory usage |
| Invalid ID format (non-numeric) | Display clear error, re-prompt | FR-013, FR-014 (no crashes) |
| ID that doesn't exist | Display clear error, return to prompt | FR-013, FR-014 (no crashes) |
| Deleting last task | Leave empty list, show friendly message | Normal behavior, handle gracefully |
| 100th task added | Warn user approaching limit (optional) | Maintain performance per SC-003 |

---

## Display Format Specification

### Task List Display

**Format**:
```
TODO LIST
=========
[1] [ ] Buy groceries
    Milk, eggs, bread

[2] [✓] Call dentist
    Schedule appointment

[3] [ ] Finish report
    (no description)
```

**Format Rules**:
- **Header**: "TODO LIST" followed by separator line "========="
- **Task Line**: `[{id}] [{status}] {title}`
  - ID in brackets, left-aligned
  - Status indicator: `[ ]` for incomplete, `[✓]` for complete
  - Title on same line
- **Description Line** (if description non-empty):
  - Indented 4 spaces
  - Display description text
  - If description empty, can show "(no description)" or omit line
- **Blank line** between tasks
- **Empty List**: Display "No tasks yet. Add one to get started!" (no header)

**Status Indicators** (FR-004):
- Incomplete: `[ ]` (space between brackets)
- Complete: `[✓]` (checkmark symbol)

---

## Data Integrity

### Invariants (must always hold)

1. **ID Uniqueness**: No two tasks have the same ID
2. **ID Positivity**: All task IDs are > 0
3. **ID Sequence**: Next ID is always > maximum existing ID
4. **No Null IDs**: Every task has an ID (never None or null)
5. **Title Non-Empty**: No task has empty title (after validation)
6. **Boolean Completed**: Task.completed is always True or False (never None)

### Consistency Rules

- Tasks are added atomically (all fields set before adding to list)
- Updates are applied in-place (no task replacement)
- Deletes remove task completely (no orphaned references)
- ID counter increments monotonically (never decreases)

### Validation Checkpoints

| Checkpoint | When | What to Check |
|------------|------|---------------|
| Before Create | User submits add command | Title non-empty, within length limits |
| After Create | Task added to list | ID assigned, ID unique, invariants hold |
| Before Update | User submits update command | New title non-empty (if changing title), within limits |
| After Update | Task fields modified | Invariants still hold, no ID change |
| Before Delete | User submits delete command | Task ID exists |
| After Delete | Task removed from list | ID not reused, list consistent |

---

## Future Extensions (Phase II+)

**Phase II - File Persistence**:
- Add serialization methods to Task (to_dict, from_dict)
- Store tasks as JSON array in file
- No schema changes needed

**Phase III - Natural Language Interface**:
- May add `created_at` timestamp field
- May add `priority` field (low/medium/high)
- May add `tags` field (list of strings)

**Phase IV/V - Cloud Deployment**:
- May migrate to database (add database ID mapping)
- May add `user_id` foreign key for multi-user support
- May add `updated_at` timestamp for conflict resolution

---

## Summary

**Entity Count**: 1 (Task)
**Relationship Count**: 0 (single entity, no relationships)
**Storage**: In-memory Python list
**Validation Points**: 3 (create, update, delete)
**State Transitions**: 2 (incomplete ↔ complete)
**Maximum Capacity**: 100 tasks (soft limit per SC-003)

**Data Model Complexity**: Minimal - appropriate for Phase I MVP scope.
