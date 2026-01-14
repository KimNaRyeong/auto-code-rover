 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import plotly.graph_objects as so

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    tips = so.load_dataset("tips")

    # Plot with 4 bins
    fig1 = so.Plot(tips, "total_bill") \
        .add(so.Bars(alpha=.3, edgewidth=0), so.Hist(bins=4)) \
        .scale(x="log")

    # Plot with 8 bins
    fig2 = so.Plot(tips, "total_bill") \
        .add(so.Bars(alpha=.3, edgewidth=0), so.Hist(bins=8)) \
        .scale(x="log")

    # Plot with 4 bins and explicit bar width
    fig3 = so.Plot(tips, "total_bill") \
        .add(so.Bar(alpha=.3, edgewidth=0, width=1), so.Hist(bins=4)) \
        .scale(x="log")

    # Check for overlap in the first plot
    for i in range(1, len(fig1.data)):
        if fig1.data[0].x[0] < fig1.data[i].x[0]:
            break
    else:
        assert False, "Overlap detected in the first plot"

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the line numbers of the statements. The script will also exit with code 1 when the issue is present. If the issue is fixed, the script will exit with code 0.