---

description: "Task list for Phase I Console Todo Application implementation"
---

# Tasks: Phase I - In-Memory Console Todo Application

**Input**: Design documents from `/specs/001-phase-i-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, research.md, quickstart.md

**Tests**: Not requested in specification - tasks focus on implementation only

**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root
- All Python files in `src/` directory
- Project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Python structure

- [X] T001 Create src/ directory for Python source code
- [X] T002 Create src/__init__.py as empty package initialization file
- [X] T003 [P] Create .gitignore with Python patterns (__pycache__/, *.pyc, .env, etc.)
- [X] T004 [P] Create README.md with project title, description, and quick start instructions
- [X] T005 [P] Create pyproject.toml for Python 3.13+ project configuration with UV

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Task model and TodoManager that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create Task dataclass in src/todo.py with fields: id (int), title (str), description (str=""), completed (bool=False)
- [X] T007 Create TodoManager class in src/todo.py with __init__ method initializing empty task list and next_id counter starting at 1
- [X] T008 Implement add_task(title: str, description: str="") -> Task method in TodoManager that validates title non-empty, creates Task with auto-incrementing ID, appends to list, increments next_id, and returns Task
- [X] T009 Implement list_tasks() -> list[Task] method in TodoManager that returns copy of tasks list
- [X] T010 Implement find_task_by_id(task_id: int) -> Task | None method in TodoManager that searches tasks list and returns matching Task or None

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 + 5 - Add/View Tasks + CLI Interface (Priority: P1) 🎯 MVP

**Goal**: Users can launch app, add tasks with title/description, view task list with status indicators, and interact via command loop

**Independent Test**: Launch app, add 3 tasks, verify they appear with IDs and [ ] status, verify empty list shows friendly message, verify CLI loop stays running until exit

**Note**: US1 (Add/View) and US5 (CLI Interface) are co-dependencies - implemented together as they form the MVP

### Implementation for US1 + US5

- [X] T011 [US1] Implement format_task(task: Task) -> str helper function in src/todo.py that returns formatted string: "[{id}] [{status}] {title}\n    {description}" where status is "[ ]" or "[✓]"
- [X] T012 [US1] Implement display_tasks(tasks: list[Task]) -> None function in src/todo.py that prints header "TODO LIST\n=========" then each formatted task, or "No tasks yet. Add one to get started!" if empty
- [X] T013 [US5] Create src/main.py with imports (from todo import Task, TodoManager) and TodoManager instance creation
- [X] T014 [US5] Implement show_help() -> None function in src/main.py that displays available commands: add, list, complete <id>, update <id>, delete <id>, exit/quit
- [X] T015 [US5] Implement handle_add_command(manager: TodoManager) -> None function in src/main.py that prompts for title, validates non-empty, prompts for optional description, calls manager.add_task(), and displays updated task list
- [X] T016 [US5] Implement handle_list_command(manager: TodoManager) -> None function in src/main.py that gets all tasks via manager.list_tasks() and calls display_tasks()
- [X] T017 [US5] Implement main() function in src/main.py with infinite while loop that displays prompt "> ", reads user input, parses command (split on whitespace), routes to command handlers, handles invalid commands with error message, and breaks loop on "exit" or "quit"
- [X] T018 [US5] Add if __name__ == "__main__": main() entry point at bottom of src/main.py
- [X] T019 [US5] Add graceful exit message "Goodbye!" when user exits application in main() function

**Checkpoint**: At this point, User Stories 1 and 5 are fully functional - MVP is complete and ready to test

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can toggle task completion status between incomplete and complete

**Independent Test**: Add task, mark it complete (verify [✓]), mark it incomplete (verify [ ]), try invalid ID (verify error message), verify no crashes

### Implementation for User Story 2

- [ ] T020 [US2] Implement toggle_complete(task_id: int) -> bool method in TodoManager (src/todo.py) that finds task by ID, returns False if not found, toggles task.completed boolean, and returns True if successful
- [ ] T021 [US2] Implement handle_complete_command(manager: TodoManager, args: list[str]) -> None function in src/main.py that validates args has exactly 1 element, validates arg is numeric, calls manager.toggle_complete(task_id), displays error "Task ID {id} not found" if task doesn't exist or "Invalid ID. Please enter a number." if not numeric, and displays updated task list if successful

**Checkpoint**: At this point, User Stories 1, 2, and 5 all work independently

---

## Phase 5: User Story 3 - Update Tasks (Priority: P3)

**Goal**: Users can update task title and/or description by ID

**Independent Test**: Add task, update description only, verify change; update both title and description, verify both change; try invalid ID, verify error message

### Implementation for User Story 3

- [ ] T022 [US3] Implement update_task(task_id: int, new_title: str | None = None, new_description: str | None = None) -> bool method in TodoManager (src/todo.py) that finds task by ID, returns False if not found, validates new_title is non-empty if provided, updates task.title if new_title provided, updates task.description if new_description provided, and returns True if successful
- [ ] T023 [US3] Implement handle_update_command(manager: TodoManager, args: list[str]) -> None function in src/main.py that validates args has exactly 1 element (task ID), validates ID is numeric, prompts "Enter new title (press Enter to keep current): ", prompts "Enter new description (press Enter to keep current): ", calls manager.update_task() with provided values (None for empty inputs), displays error "Task ID {id} not found" if task doesn't exist or "Invalid ID" if not numeric or "Title cannot be empty" if new title is empty, and displays updated task list if successful

**Checkpoint**: At this point, User Stories 1, 2, 3, and 5 all work independently

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can delete tasks by ID to keep list clean

**Independent Test**: Add 3 tasks, delete middle task, verify only 2 remain; delete last task, verify gone; add new task, verify ID not reused; try invalid ID, verify error

### Implementation for User Story 4

- [ ] T024 [US4] Implement delete_task(task_id: int) -> bool method in TodoManager (src/todo.py) that finds task by ID, returns False if not found, removes task from tasks list using tasks.remove(task), and returns True if successful (note: does NOT decrement next_id - IDs are never reused)
- [ ] T025 [US4] Implement handle_delete_command(manager: TodoManager, args: list[str]) -> None function in src/main.py that validates args has exactly 1 element, validates arg is numeric, calls manager.delete_task(task_id), displays error "Task ID {id} not found" if task doesn't exist or "Invalid ID. Please enter a number." if not numeric, and displays updated task list if successful

**Checkpoint**: All user stories (1-5) are now independently functional - feature complete

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T026 [P] Add type hints to all functions and methods in src/todo.py and src/main.py (verify compliance with Python 3.13 typing standards)
- [ ] T027 [P] Add docstrings to Task dataclass, TodoManager class, and all public functions in src/todo.py and src/main.py (follow Google style guide)
- [ ] T028 [P] Run PEP8 style check on all Python files (can use: python -m py_compile src/*.py)
- [ ] T029 Validate all edge cases from spec.md: empty title rejection, non-existent ID errors, empty list message, invalid command handling, non-numeric ID handling
- [ ] T030 [P] Update README.md with complete usage instructions, command reference, and example session (use content from quickstart.md)
- [ ] T031 Manual testing: Run through all acceptance scenarios from spec.md for all 5 user stories and verify success criteria SC-001 through SC-007
- [ ] T032 Performance validation: Add 100 tasks and verify list displays in <1 second per SC-003

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1+US5 (Phase 3): Can start after Foundational - No dependencies on other stories
  - US2 (Phase 4): Can start after Foundational - Independent of US1 implementation but logically builds on it
  - US3 (Phase 5): Can start after Foundational - Independent of US1/US2 but logically builds on them
  - US4 (Phase 6): Can start after Foundational - Independent of other stories
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 + 5 (P1)**: Can start after Foundational (Phase 2) - These are co-dependencies forming the MVP
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent implementation, logically extends US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent implementation, logically extends US1
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Completely independent

### Within Each User Story

**Foundation (Phase 2)**:
- T006 (Task dataclass) must complete before T007 (TodoManager)
- T007 (TodoManager init) must complete before T008-T010 (methods)
- T008, T009, T010 can run in parallel (different methods)

**User Story 1 + 5 (Phase 3)**:
- T011 (format function) independent
- T012 (display function) uses T011 output
- T013 (main.py setup) independent
- T014 (help function) independent
- T015 (add handler) uses T008 (add_task method) and T012 (display)
- T016 (list handler) uses T009 (list_tasks method) and T012 (display)
- T017 (main loop) uses T014-T016 (command handlers)
- T018 (entry point) uses T017 (main)
- T019 (exit message) modifies T017 (main)

**User Story 2 (Phase 4)**:
- T020 (toggle method) uses T010 (find_task)
- T021 (complete handler) uses T020 (toggle method) and T012 (display)

**User Story 3 (Phase 5)**:
- T022 (update method) uses T010 (find_task)
- T023 (update handler) uses T022 (update method) and T012 (display)

**User Story 4 (Phase 6)**:
- T024 (delete method) uses T010 (find_task)
- T025 (delete handler) uses T024 (delete method) and T012 (display)

**Polish (Phase 7)**:
- T026, T027, T028, T030 can run in parallel (different concerns)
- T029, T031, T032 are validation tasks (run after implementation complete)

### Parallel Opportunities

**Setup Phase (Phase 1)**:
- T003, T004, T005 can run in parallel (different files)

**Foundational Phase (Phase 2)**:
- T008, T009, T010 can run in parallel after T007 completes (different methods in same class)

**User Story 1 + 5 (Phase 3)**:
- T011, T012, T013, T014 can run in parallel (different functions/files)

**Polish Phase (Phase 7)**:
- T026, T027, T028, T030 can run in parallel (different concerns)

---

## Parallel Example: Foundational Phase

```bash
# After T007 completes (TodoManager __init__), launch all CRUD methods together:
Task T008: "Implement add_task method in src/todo.py"
Task T009: "Implement list_tasks method in src/todo.py"
Task T010: "Implement find_task_by_id method in src/todo.py"
```

---

## Parallel Example: User Story 1 + 5 Setup

```bash
# Before main loop, these can run in parallel:
Task T011: "Implement format_task function in src/todo.py"
Task T012: "Implement display_tasks function in src/todo.py"
Task T013: "Create src/main.py with imports and TodoManager instance"
Task T014: "Implement show_help function in src/main.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 5 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Stories 1 + 5 (Add/View + CLI)
4. **STOP and VALIDATE**: Test independently - can add tasks and view them in CLI
5. Deploy/demo if ready

**This gives you a working MVP**: Users can launch the app, add tasks, view tasks, and exit cleanly.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 + US5 → Test independently → MVP complete! ✅
3. Add US2 (Mark Complete) → Test independently → Progress tracking enabled
4. Add US3 (Update) → Test independently → Task editing enabled
5. Add US4 (Delete) → Test independently → Full CRUD complete
6. Add Polish → Final validation → Production ready

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers (or parallel agent execution):

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 + US5 (Add/View + CLI) - **Priority 1**
   - Developer B: US2 (Mark Complete) - **Priority 2**
   - Developer C: US3 (Update) - **Priority 3**
   - Developer D: US4 (Delete) - **Priority 4**
3. Stories complete and integrate independently
4. All converge on Polish phase

---

## Notes

- **[P] tasks** = different files/methods, no dependencies on incomplete tasks
- **[Story] label** maps task to specific user story for traceability
- Each user story is independently completable and testable
- No tests included (not requested in specification)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **US1 and US5 are co-implemented** because the CLI interface (US5) is required to access add/view functionality (US1)
- All tasks include explicit file paths (src/todo.py or src/main.py)
- Type hints and docstrings added in Polish phase to maintain focus on functionality first

---

## Task Count Summary

- **Total Tasks**: 32
- **Setup**: 5 tasks
- **Foundational**: 5 tasks (blocking)
- **US1 + US5**: 9 tasks (MVP)
- **US2**: 2 tasks
- **US3**: 2 tasks
- **US4**: 2 tasks
- **Polish**: 7 tasks

**Parallel Opportunities**: 9 tasks can run in parallel across different phases

**MVP Scope**: 19 tasks (Setup + Foundational + US1 + US5) = Minimum viable product

**Feature Complete**: 28 tasks (all except final Polish validations)

---

## Success Validation Checklist

After completing all tasks, verify against spec.md success criteria:

- [ ] **SC-001**: Add a task and see it in list < 10 seconds
- [ ] **SC-002**: Complete all 5 operations within 2 minutes of first use
- [ ] **SC-003**: Add 100 tasks, list displays < 1 second
- [ ] **SC-004**: Try invalid IDs, invalid commands → clear errors, no crashes
- [ ] **SC-005**: Perform 20 consecutive operations without crash/freeze
- [ ] **SC-006**: Task list shows ID, title, description, status clearly
- [ ] **SC-007**: Toggle task status without losing any data

All success criteria must pass before Phase I submission.
