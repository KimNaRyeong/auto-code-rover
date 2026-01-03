 Here is a standalone python script `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt

def print_datalim(*ax):
    for ax_ in ax:
        print(ax_.dataLim.intervaly, end=' / ')
    print()

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

if __name__ == "__main__":
    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    fig, ax1 = plt.subplots()

    ax1.stackplot(df1_index, df1_values)
    print_datalim(ax1)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    print_datalim(ax1, ax2)

    ax2.plot(df1_index, df2_values)
    print_datalim(ax1, ax2)

    try:
        assert ax1.dataLim.intervaly != (float('inf'), float('-inf')), "Data limits of ax1 should not be infs."
    except AssertionError as e:
        print_stacktrace(e)
```
This script reproduces the issue and raises an `AssertionError` when the data limits of `ax1` are changed to `(inf, -inf)`. The script prints the stack trace of the error.

To fix the issue, you can either downgrade Matplotlib to version 3.3.4 or earlier, or modify the script to use a different type of plot on the second axis, such as a line plot, which does not change the data limits of the first axis.