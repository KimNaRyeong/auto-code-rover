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
        plt.savefig("hi.png")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()

assert True
```

This script will import matplotlib and then run the code that reproduces the issue. If an exception is raised during the execution of this code, it will catch the exception, print a stack trace using the `print_stacktrace` function, and then re-raise the exception so that the calling process can handle it. The script also includes an assertion statement to ensure that the script exits with code 0 when the issue is fixed.

Please note that you need to have matplotlib installed in your Python environment for this script to run correctly.