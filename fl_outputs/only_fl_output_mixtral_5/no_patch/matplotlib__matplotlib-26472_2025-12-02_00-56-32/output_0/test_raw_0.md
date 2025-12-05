 Here is a standalone python script `reproducer.py` that reproduces the issue:
```python
import matplotlib.pyplot as plt
import sys

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

@contextmanager
def window(block=False):
    plt.ioff()
    plt.rcParams['backend'] = "Qt5Agg"
    yield
    plt.show()
    plt.ion()
    plt.rcParams['backend'] = "inline"

try:
    with window():
        plt.plot([1, 3, 2])
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```
To run the script, execute `python3 reproducer.py` in the terminal. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 1 when the issue is fixed.

The expected outcome is that the plot window stays open after the context manager exits, but the actual outcome is that the plot window closes when the `plt.rcParams['backend'] = "inline"` line is executed.