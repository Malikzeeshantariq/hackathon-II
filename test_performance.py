"""
Performance test script - Add 100 tasks to test SC-003
Run this, then use 'list' command to verify <1 second display
"""

from src.todo import TodoManager, display_tasks
import time

def test_performance():
    """Add 100 tasks and measure list display time."""
    manager = TodoManager()

    # Add 100 tasks
    print("Adding 100 tasks...")
    for i in range(1, 101):
        manager.add_task(
            f"Task {i}",
            f"Description for task number {i}"
        )

    print(f"Added {len(manager.list_tasks())} tasks")

    # Measure display time
    print("\nTesting list display performance...")
    start_time = time.time()
    display_tasks(manager.list_tasks())
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"\n{'='*50}")
    print(f"Display time: {elapsed:.4f} seconds")
    print(f"Success Criteria (SC-003): < 1.0 second")
    print(f"Result: {'✅ PASS' if elapsed < 1.0 else '❌ FAIL'}")
    print(f"{'='*50}")

if __name__ == "__main__":
    test_performance()
