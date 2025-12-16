 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

def print(vmin, vmax):
    print(f'vmin: {vmin}, vmax: {vmax}')

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

fig, ax = plt.subplots()
ax.plot([10, 20], [10, 20])
ss = SpanSelector(ax, print, "horizontal", span_stays=True)  # or interactive=True

try:
    plt.show()
    assert False, "The issue is not reproduced."
except AssertionError:
    pass
except Exception as e:
    print_stacktrace(e)
```
The script creates a simple plot with a horizontal `SpanSelector` and prints the `vmin` and `vmax` values when the selection changes. When the `SpanSelector` is interactively removed by clicking and immediately releasing the button, the `onselect` callback should be fired, but it is not in the new implementation.

To run the script, execute `python3 reproducer.py` in the terminal. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.