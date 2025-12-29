# Technical Research: Phase I - In-Memory Console Todo Application

**Feature**: 001-phase-i-console-todo
**Date**: 2025-12-30
**Purpose**: Resolve technical decisions and validate approach for Phase I implementation

## Research Topics

### 1. Python 3.13 Features for Console Applications

**Decision**: Use Python 3.13 with standard library only

**Rationale**:
- Python 3.13 provides improved performance and better type checking support
- Standard library includes all necessary components: `dataclasses` for Task model, `typing` for type hints, `sys` for CLI I/O
- No external dependencies reduces complexity and aligns with Phase I constraints
- Simplifies deployment and testing in WSL 2 environment

**Alternatives Considered**:
- **Python 3.11/3.12**: Would work but 3.13 required by hackathon Phase I specification
- **External CLI frameworks (Click, Typer, Rich)**: Rejected - adds unnecessary complexity for Phase I; contradicts "standard library only" constraint
- **prompt_toolkit for advanced CLI**: Rejected - overkill for simple command loop; adds dependency

**Best Practices Applied**:
- Use `dataclasses` with `frozen=False` for mutable Task objects
- Use `typing.List` for task storage and type annotations
- Use `input()` for simple command-loop interface
- Keep CLI parsing minimal (string split and pattern matching)

---

### 2. In-Memory Data Storage Strategy

**Decision**: Use a Python list to store Task dataclass instances

**Rationale**:
- List provides O(n) access for display/iteration (acceptable for 100 tasks)
- Direct index-based access not needed since tasks use auto-incrementing IDs
- List append is O(1) amortized for adding new tasks
- Simple to implement find-by-ID with list comprehension
- No serialization needed (in-memory only for Phase I)

**Alternatives Considered**:
- **Dictionary with ID as key**: Slight performance benefit for lookup, but adds complexity for ID generation and management
- **Set**: Inappropriate - tasks need ordering and duplicate IDs impossible by design
- **Custom data structure**: Over-engineering for Phase I scope

**Implementation Details**:
- Initialize as empty list: `tasks: List[Task] = []`
- ID generation: Track next_id counter, increment after each add
- Find operations: Use `next((task for task in tasks if task.id == target_id), None)`
- Delete operations: Use `tasks.remove(task)` after finding
- Update operations: Modify task object in-place (dataclass with `frozen=False`)

**Best Practices**:
- Validate IDs before operations (check existence)
- Return clear error messages for invalid IDs
- Maintain ID counter separately to avoid reusing IDs after deletion

---

### 3. Task Model Design

**Decision**: Use `@dataclass` with mutable fields for Task entity

**Rationale**:
- Dataclasses provide clean syntax and automatic `__init__`, `__repr__`
- Mutable fields required for update operations (title, description, status can change)
- Type hints built-in for data validation
- Pythonic and aligns with modern Python best practices

**Task Entity Definition**:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool = False
```

**Alternatives Considered**:
- **NamedTuple**: Rejected - immutable, cannot update tasks
- **Plain class**: More verbose than dataclass, less pythonic
- **Dict**: No type safety, harder to maintain

**Field Decisions**:
- `id: int` - Auto-incrementing, never reused, managed by TodoManager
- `title: str` - Required, validated as non-empty before task creation
- `description: str` - Optional (can be empty string), defaults to ""
- `completed: bool` - Default False, toggle for mark complete/incomplete

**Best Practices**:
- Keep dataclass simple - no business logic methods
- Business logic in separate TodoManager class
- Use type hints for all fields
- Provide sensible defaults where appropriate

---

### 4. CLI Interface Design

**Decision**: Simple command-loop with command parser using string split

**Rationale**:
- Meets "simple text-based interface" requirement
- No external dependencies needed
- Easy to understand and maintain
- Sufficient for 5 core operations

**Command Format Decisions**:
- `add` - Prompt for title and description separately (multi-step input)
- `list` - No arguments, displays all tasks
- `complete <id>` - Single argument (task ID to toggle)
- `update <id>` - Prompts for new title and/or description (multi-step)
- `delete <id>` - Single argument (task ID to delete)
- `exit` / `quit` - Exit application gracefully
- `help` - Display available commands (bonus, not in spec but helpful)

**Alternatives Considered**:
- **Single-line commands with all args**: More complex to parse and error-prone for user input
- **Menu-driven interface**: Less flexible, more code to maintain
- **Natural language (Phase III feature)**: Out of scope for Phase I

**Best Practices**:
- Display prompt: `> ` (simple and clear)
- Show help on start and when invalid command entered
- Display updated task list after each operation (except exit)
- Graceful error handling with clear messages
- Case-insensitive command matching

---

### 5. Error Handling Strategy

**Decision**: Input validation with user-friendly error messages, no crashes

**Rationale**:
- FR-014 requires no crashes for any user input
- FR-013 requires clear error messages for invalid operations
- User experience prioritized per spec success criteria

**Error Categories and Handling**:
1. **Invalid Command**: Display "Unknown command. Type 'help' for available commands."
2. **Invalid ID**: Display "Task ID <id> not found."
3. **Non-numeric ID**: Display "Invalid ID. Please enter a number."
4. **Empty Title**: Prompt again or display "Title cannot be empty."
5. **Unexpected Errors**: Catch all exceptions, display generic error, log to stderr

**Best Practices**:
- Use try-except blocks around user input parsing
- Validate IDs before performing operations
- Provide helpful context in error messages
- Never use `sys.exit()` except for normal quit command
- Return to command prompt after any error

---

### 6. Code Organization

**Decision**: Two-file structure - main.py (UI/CLI) and todo.py (logic/model)

**Rationale**:
- Aligns with user input: "Structure: main.py for entry, todo.py for class/logic"
- Clean separation of concerns (UI vs. business logic)
- Testable - todo.py can be unit tested independently
- Extensible for future phases

**File Responsibilities**:
- **main.py**:
  - CLI command loop (interactive interface)
  - Command parsing and routing
  - User I/O (input prompts, output formatting)
  - Application entry point (`if __name__ == "__main__"`)

- **todo.py**:
  - Task dataclass definition
  - TodoManager class (CRUD operations)
  - ID generation logic
  - Business logic and validation

**Best Practices**:
- Keep main.py focused on UI/UX
- Keep todo.py free of I/O (pure business logic)
- Use type hints throughout
- Follow PEP8 style guide
- Maximum function length: ~20 lines for readability

---

### 7. Display Format

**Decision**: Simple text table format with status indicators

**Rationale**:
- Meets FR-004 requirement for clear status indicators
- No external dependencies (no Rich library)
- Human-readable without documentation (SC-006)

**Display Format**:
```
TODO LIST
=========
[1] [ ] Buy groceries
    Milk, eggs, bread

[2] [✓] Call dentist
    Schedule appointment

[3] [ ] Finish report


No tasks yet. Add one to get started!  (for empty list)
```

**Format Decisions**:
- ID in brackets: `[1]`
- Status indicators: `[ ]` incomplete, `[✓]` complete
- Title on same line as ID and status
- Description indented on next line (if not empty)
- Blank line between tasks
- Header "TODO LIST" with separator

**Alternatives Considered**:
- **Table format with columns**: More complex to implement, harder to read with variable-length descriptions
- **JSON output**: Not user-friendly for console interaction
- **Rich library formatting**: Violates "no external dependencies" constraint

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Language | Python | 3.13+ | Hackathon requirement; modern features |
| Data Model | dataclasses | stdlib | Clean syntax, type hints, mutable |
| Storage | list | stdlib | Simple, sufficient for 100 tasks |
| CLI I/O | input/print | stdlib | Simple, no dependencies |
| Type Checking | typing | stdlib | PEP8 compliance, code quality |
| Testing | pytest | 8.x | Industry standard (optional for Phase I) |

---

## Performance Considerations

**Expected Performance**:
- **Add Task**: O(1) - append to list
- **List Tasks**: O(n) - iterate all tasks (n=100 → <1ms)
- **Find by ID**: O(n) - linear search (n=100 → <1ms)
- **Update Task**: O(n) find + O(1) update
- **Delete Task**: O(n) find + O(n) remove (worst case)

**Optimization Notes**:
- No optimization needed for 100 tasks (all operations <1ms)
- If scaling beyond 100 tasks in future: consider dict-based storage
- For Phase I: simplicity > performance

---

## Testing Strategy (Optional for Phase I)

**Approach**: Unit tests for todo.py, manual testing for main.py CLI

**Test Coverage**:
- Task creation with valid inputs
- ID auto-increment behavior
- ID non-reuse after deletion
- Find by ID (valid and invalid)
- Toggle completion status
- Update title and/or description
- Delete by ID
- Edge cases: empty list, invalid IDs, empty title

**Tools**: pytest (if testing is implemented)

---

## Migration Path to Phase II

**Phase II Requirements**: Add file-based persistence

**Planned Changes**:
- Add `storage.py` module with save/load functions
- Serialize tasks to JSON file
- Load tasks on startup
- Save tasks after each operation
- No changes to Task dataclass or TodoManager core logic

**Compatibility**: Current design supports easy extension without breaking changes

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| User enters very long title/description | Memory usage, display issues | Validate max length (title: 200 chars, description: 1000 chars) |
| Special characters in input | Display formatting breaks | Use UTF-8 encoding, test with special chars |
| ID counter overflow | Unlikely for Phase I | Use Python int (unbounded), document limitation |
| Performance degradation >100 tasks | Violates SC-003 | Document 100-task limit, warn user if exceeded |

---

## Open Questions (Resolved)

All technical unknowns from plan.md resolved:
- ✅ Python version: 3.13+
- ✅ Storage mechanism: In-memory list
- ✅ Data structure: Task dataclass
- ✅ CLI approach: Simple command loop with input()
- ✅ File organization: main.py + todo.py
- ✅ Display format: Text with status indicators
- ✅ Error handling: Validation with clear messages

**Research Complete** - Ready for Phase 1 (Data Model and Contracts)
