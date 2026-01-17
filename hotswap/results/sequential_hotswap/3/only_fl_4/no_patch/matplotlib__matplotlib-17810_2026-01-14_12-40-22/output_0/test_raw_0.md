```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    try:
        fig, ax = plt.subplots()
        plt.plot([1,2,3],[2,4,3])

        def update(frame):
            return []

        animation = FuncAnimation(fig, update, frames=iter(range(10)), repeat=False, blit=True, interval=100)
        # Save the animation
        animation.save("hi.mp4")

        # Create and save a different figure
        fig2, ax2 = plt.subplots()
        ax2.plot([7, 6, 3], [3, 5, 2])
        fig2.savefig("hi.png")
        
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.")

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to reproduce the issue described. It:

1. Creates a plot and an animation, then saves the animation to a file.
2. Creates a separate plot and saves it to a different file.
3. Uses a `try-except` block to catch any exceptions that arise during the process.
4. Makes use of a custom `print_stacktrace` function to print a detailed stack trace of any caught exception, ensuring the line numbers and code contexts are clear.
5. Raises an `AssertionError` if an exception is caught, indicating the presence of the issue.

When executed with `python3 reproducer.py`, it's expected to catch and output details of the `StopIteration` exception caused by the conflicting interactions between `animation.save` and `fig.savefig` as described.