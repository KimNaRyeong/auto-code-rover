```python
# reproducer.py
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
        plt.plot([1,2,3], [2,4,3])
        
        def update(frame):
            return []
        
        animation = FuncAnimation(fig, update, frames=iter(range(10)), repeat=False, blit=True, interval=100)
        animation.save("hi.mp4")
        
        fig2, ax2 = plt.subplots()
        ax2.plot([7, 6, 3], [3, 5, 2])
        fig2.savefig("hi.png")
    except StopIteration as e:
        print_stacktrace(e)
        raise AssertionError("StopIteration issue occurred") from e

if __name__ == "__main__":
    reproduce_issue()
```

To execute this script, save it to the root directory of your project as `reproducer.py` and run it using the command `python3 reproducer.py`. This script will attempt to reproduce the reported issue where the `animation.save` and `fig.savefig` methods interfere with each other and raise a `StopIteration` exception under certain conditions. The script uses a `try...except` block to catch the `StopIteration` exception if it occurs, prints a stack trace with clear line numbers of the relevant statements, and exits by raising an `AssertionError`. If the exception is not raised (meaning the issue has been resolved or does not occur), the script will complete without printing anything or raising an error, thus exiting with code 0.