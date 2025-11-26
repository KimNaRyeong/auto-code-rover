Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

def onselect(vmin, vmax):
    if vmin == vmax:
        raise AssertionError("onselect callback should be fired when span is removed")

fig, ax = plt.subplots()
ax.plot([10, 20], [10, 20])
ss = SpanSelector(ax, onselect, "horizontal", interactive=True)

plt.show()

try:
    input("Click and drag to select a span, then click and release immediately to remove the span.")
except AssertionError as e:
    print_stacktrace(e)
```
This script creates an interactive `SpanSelector` with the `onselect` callback. When you run the script, it will display a plot and wait for your input. Click and drag to select a span, then click and release immediately to remove the span. If the issue is present, the `onselect` callback should not be fired when the span is removed, and an `AssertionError` will be raised. The script will print a stack trace of the error and exit with a non-zero code. If the issue is fixed, the script will exit with code 0.