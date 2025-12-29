"""
Todo Application - Core Business Logic

This module contains the Task data model and TodoManager class that handles
all CRUD operations for tasks stored in memory.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """Represents a todo task with title, description, and completion status."""
    id: int
    title: str
    description: str = ""
    completed: bool = False


class TodoManager:
    """Manages todo tasks with CRUD operations using in-memory storage."""

    def __init__(self) -> None:
        """Initialize TodoManager with empty task list and ID counter."""
        self.tasks: list[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with title and optional description.

        Args:
            title: Task title (required, must be non-empty)
            description: Task description (optional, defaults to empty string)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is empty or whitespace only
        """
        # Validate title is non-empty
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        # Create task with auto-incrementing ID
        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip(),
            completed=False
        )

        # Add to list and increment ID counter
        self.tasks.append(task)
        self.next_id += 1

        return task

    def list_tasks(self) -> list[Task]:
        """
        Get all tasks.

        Returns:
            Copy of the tasks list
        """
        return self.tasks.copy()

    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find a task by its ID.

        Args:
            task_id: The ID of the task to find

        Returns:
            The Task object if found, None otherwise
        """
        return next((task for task in self.tasks if task.id == task_id), None)

    def toggle_complete(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if task was found and toggled, False otherwise
        """
        task = self.find_task_by_id(task_id)
        if task is None:
            return False

        task.completed = not task.completed
        return True

    def update_task(
        self,
        task_id: int,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None
    ) -> bool:
        """
        Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            new_title: New title (None to keep current)
            new_description: New description (None to keep current)

        Returns:
            True if task was found and updated, False otherwise

        Raises:
            ValueError: If new_title is provided but is empty
        """
        task = self.find_task_by_id(task_id)
        if task is None:
            return False

        # Validate new title if provided
        if new_title is not None:
            if not new_title or not new_title.strip():
                raise ValueError("Title cannot be empty")
            task.title = new_title.strip()

        # Update description if provided
        if new_description is not None:
            task.description = new_description.strip()

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was found and deleted, False otherwise

        Note:
            IDs are never reused - next_id counter is not decremented
        """
        task = self.find_task_by_id(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        return True


def format_task(task: Task) -> str:
    """
    Format a task for display.

    Args:
        task: The Task object to format

    Returns:
        Formatted string with ID, status indicator, title, and description
    """
    status = "[✓]" if task.completed else "[ ]"
    formatted = f"[{task.id}] {status} {task.title}"

    if task.description:
        formatted += f"\n    {task.description}"

    return formatted


def display_tasks(tasks: list[Task]) -> None:
    """
    Display all tasks with header or empty message.

    Args:
        tasks: List of Task objects to display
    """
    if not tasks:
        print("\nNo tasks yet. Add one to get started!")
        return

    print("\nTODO LIST")
    print("=" * 40)

    for task in tasks:
        print(format_task(task))
        print()  # Blank line between tasks
