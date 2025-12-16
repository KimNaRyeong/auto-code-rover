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
    tips = so.datasets.load_tips()

    # Plot with 4 bins
    fig1 = so.Plot(tips, "total_bill").add(so.Bars(alpha=.3, edgewidth=0), so.Hist(bins=4)).scale(x="log")
    assert fig1.layout.xaxis.type == "log", "AssertionError: x-axis should be log scale"
    assert fig1.layout.yaxis.type == "linear", "AssertionError: y-axis should be linear"
    assert fig1.layout.showlegend == True, "AssertionError: Legend should be shown"
    assert len(fig1.data) == 3, "AssertionError: There should be 3 plots in the figure"
    assert fig1.data[0].x[0] > 0, "AssertionError: First bar should start from a positive value"
    assert fig1.data[0].x[-1] < fig1.layout.xaxis.range[1], "AssertionError: Last bar should end before the maximum value of the x-axis"
    assert fig1.data[1].x[0] > 0, "AssertionError: First histogram bar should start from a positive value"
    assert fig1.data[1].x[-1] < fig1.layout.xaxis.range[1], "AssertionError: Last histogram bar should end before the maximum value of the x-axis"
    assert fig1.data[2].x[0] > 0, "AssertionError: First histogram bar should start from a positive value"
    assert fig1.data[2].x[-1] < fig1.layout.xaxis.range[1], "AssertionError: Last histogram bar should end before the maximum value of the x-axis"

    # Plot with 8 bins
    fig2 = so.Plot(tips, "total_bill").add(so.Bars(alpha=.3, edgewidth=0), so.Hist(bins=8)).scale(x="log")
    assert fig2.layout.xaxis.type == "log", "AssertionError: x-axis should be log scale"
    assert fig2.layout.yaxis.type == "linear", "AssertionError: y-axis should be linear"
    assert fig2.layout.showlegend == True, "AssertionError: Legend should be shown"
    assert len(fig2.data) == 3, "AssertionError: There should be 3 plots in the figure"
    assert fig2.data[0].x[0] > 0, "AssertionError: First bar should start from a positive value"
    assert fig2.data[0].x[-1] < fig2.layout.xaxis.range[1], "AssertionError: Last bar should end before the maximum value of the x-axis"
    assert fig2.data[1].x[0] > 0, "AssertionError: First histogram bar should start from a positive value"
    assert fig2.data[1].x[-1] < fig2.layout.xaxis.range[1], "AssertionError: Last histogram bar should end before the maximum value of the x-axis"
    assert fig2.data[2].x[0] > 0, "AssertionError: First histogram bar should start from a positive value"
    assert fig2.data[2].x[-1] < fig2.layout.xaxis.range[1], "AssertionError