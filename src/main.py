"""
Phase I - In-Memory Console Todo Application

Main entry point and interactive command-loop interface.
"""

from todo import Task, TodoManager, display_tasks


def show_help() -> None:
    """Display available commands to the user."""
    print("\nAvailable Commands:")
    print("  add              - Add a new task")
    print("  list             - Display all tasks")
    print("  complete <id>    - Toggle task completion status")
    print("  update <id>      - Update task title and/or description")
    print("  delete <id>      - Delete a task")
    print("  help             - Show this help message")
    print("  exit, quit       - Exit the application")
    print()


def handle_add_command(manager: TodoManager) -> None:
    """
    Handle the 'add' command to create a new task.

    Args:
        manager: TodoManager instance
    """
    try:
        # Prompt for title
        title = input("Enter task title: ").strip()

        # Validate title is non-empty
        if not title:
            print("Error: Title cannot be empty.")
            return

        # Prompt for optional description
        description = input("Enter task description (optional): ").strip()

        # Add task
        task = manager.add_task(title, description)
        print(f"Task added successfully! (ID: {task.id})")

        # Display updated task list
        display_tasks(manager.list_tasks())

    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")


def handle_list_command(manager: TodoManager) -> None:
    """
    Handle the 'list' command to display all tasks.

    Args:
        manager: TodoManager instance
    """
    tasks = manager.list_tasks()
    display_tasks(tasks)


def handle_complete_command(manager: TodoManager, args: list[str]) -> None:
    """
    Handle the 'complete' command to toggle task completion status.

    Args:
        manager: TodoManager instance
        args: Command arguments (should contain task ID)
    """
    # Validate arguments
    if len(args) != 1:
        print("Usage: complete <id>")
        return

    try:
        # Parse task ID
        task_id = int(args[0])

        # Toggle completion
        success = manager.toggle_complete(task_id)

        if success:
            print(f"Task {task_id} status toggled successfully!")
            display_tasks(manager.list_tasks())
        else:
            print(f"Error: Task ID {task_id} not found.")

    except ValueError:
        print("Error: Invalid ID. Please enter a number.")


def handle_update_command(manager: TodoManager, args: list[str]) -> None:
    """
    Handle the 'update' command to modify a task.

    Args:
        manager: TodoManager instance
        args: Command arguments (should contain task ID)
    """
    # Validate arguments
    if len(args) != 1:
        print("Usage: update <id>")
        return

    try:
        # Parse task ID
        task_id = int(args[0])

        # Check if task exists
        task = manager.find_task_by_id(task_id)
        if task is None:
            print(f"Error: Task ID {task_id} not found.")
            return

        # Prompt for new title
        print(f"Current title: {task.title}")
        new_title_input = input("Enter new title (press Enter to keep current): ").strip()
        new_title = new_title_input if new_title_input else None

        # Prompt for new description
        print(f"Current description: {task.description if task.description else '(empty)'}")
        new_desc_input = input("Enter new description (press Enter to keep current): ").strip()
        new_description = new_desc_input if new_desc_input else None

        # Update task
        if new_title is None and new_description is None:
            print("No changes made.")
            return

        success = manager.update_task(task_id, new_title, new_description)

        if success:
            print(f"Task {task_id} updated successfully!")
            display_tasks(manager.list_tasks())
        else:
            print(f"Error: Failed to update task {task_id}.")

    except ValueError as e:
        if "ID" in str(e) or "number" in str(e):
            print("Error: Invalid ID. Please enter a number.")
        else:
            print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")


def handle_delete_command(manager: TodoManager, args: list[str]) -> None:
    """
    Handle the 'delete' command to remove a task.

    Args:
        manager: TodoManager instance
        args: Command arguments (should contain task ID)
    """
    # Validate arguments
    if len(args) != 1:
        print("Usage: delete <id>")
        return

    try:
        # Parse task ID
        task_id = int(args[0])

        # Delete task
        success = manager.delete_task(task_id)

        if success:
            print(f"Task {task_id} deleted successfully!")
            display_tasks(manager.list_tasks())
        else:
            print(f"Error: Task ID {task_id} not found.")

    except ValueError:
        print("Error: Invalid ID. Please enter a number.")


def main() -> None:
    """Main application entry point with interactive command loop."""
    # Create TodoManager instance
    manager = TodoManager()

    # Welcome message
    print("\n" + "=" * 40)
    print("TODO LIST - Phase I")
    print("=" * 40)
    print("\nType 'help' for available commands.")

    # Main command loop
    while True:
        try:
            # Display prompt and read command
            user_input = input("\n> ").strip().lower()

            # Skip empty input
            if not user_input:
                continue

            # Parse command and arguments
            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            # Route to command handlers
            if command in ("exit", "quit"):
                print("\nGoodbye!")
                break

            elif command == "help":
                show_help()

            elif command == "add":
                handle_add_command(manager)

            elif command == "list":
                handle_list_command(manager)

            elif command == "complete":
                handle_complete_command(manager, args)

            elif command == "update":
                handle_update_command(manager, args)

            elif command == "delete":
                handle_delete_command(manager, args)

            else:
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Type 'help' for available commands.")


if __name__ == "__main__":
    main()
