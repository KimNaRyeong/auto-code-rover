 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import plotly.express as so
import plotly.graph_objects as go

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

tips = so.data.tips()

try:
    fig = so.Plot(tips, "total_bill").add(so.Bars(alpha=.3, edgewidth=0), so.Hist(bins=4)).scale(x="log")
    assert fig.full_layout.width == 800
except AssertionError:
    print_stacktrace(e)
    raise

try:
    fig = so.Plot(tips, "total_bill").add(so.Bars(alpha=.3, edgewidth=0), so.Hist(bins=8)).scale(x="log")
    assert fig.full_layout.width == 800
except AssertionError:
    print_stacktrace(e)
    raise

try:
    fig = so.Plot(tips, "total_bill").add(so.Bar(alpha=.3, edgewidth=0, width=1), so.Hist(bins=4)).scale(x="log")
    assert fig.full_layout.width == 800
except AssertionError:
    print_stacktrace(e)
    raise
```
The script uses the `plotly.express` module to create the plots and the `plotly.graph_objects` module to access the layout properties of the figures. The `print_stacktrace` function is used to print the stack trace when an `AssertionError` is raised.

The script creates three figures using the same data and scales, but with different combinations of bars and histograms. It then checks the width of each figure and raises an `AssertionError` if it is not equal to 800. This is because the issue is related to the width computation of the figures, and the difference in width is expected to be small and imperceptible.

When executed using `python3 reproducer.py`, the script will print the stack trace and raise an `AssertionError` if the issue is present. If the issue is fixed, the script will exit with code 0 without raising any errors.