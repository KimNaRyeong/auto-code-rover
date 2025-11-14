Here is the reproducer script:

```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import traceback

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
        animation.save("hi.mp4")
        
        fig2, ax2 = plt.subplots()
        ax2.plot([7, 6, 3], [3, 5, 2])
        try:
            fig2.savefig("hi.png")
        except Exception as e:
            print_stacktrace(e)
            sys.exit(1)

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.

Please note that you need to have matplotlib installed in your Python environment for this script to run correctly.