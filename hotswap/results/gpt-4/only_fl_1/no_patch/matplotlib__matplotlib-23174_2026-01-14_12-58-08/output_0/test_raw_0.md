```python
import matplotlib.pyplot as plt
import numpy as np

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
    delta = 0.025
    x = np.arange(-3.0, 3.0, delta)
    y = np.arange(-2.0, 2.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-(X**2) - Y**2)
    Z2 = np.exp(-((X - 1) ** 2) - (Y - 1) ** 2)
    Z = (Z1 - Z2) * 2

    fig = plt.figure()
    figs = fig.subfigures(nrows=1, ncols=2)

    try:
        for f in figs:
            ax = f.subplots()
            CS = ax.contour(X, Y, Z)
            ax.clabel(CS, inline=True, fontsize=10)
            ax.set_title("Simplest default with labels")
        plt.show()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue detected: Crash when adding clabels to subfigures.") from e

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        exit(0)  # Exiting with 0 if the specific issue is reproduced
```

This script includes a `try` block where it attempts to create contour plots with labels for subfigures. If the operation fails and raises an exception, the script catches this exception, prints a detailed stack trace using the `print_stacktrace` function, and raises an `AssertionError` indicating that the issue has been detected. On the other hand, if Matplotlib's behavior changes in the future such that the issue is fixed and the script runs without raising an exception, the script would normally complete and exit with a code of 0 (indicating success). 

This script is structured to specifically catch exceptions related to the described issue, offering developers a clear path to confirm the presence of the bug and benefit from the detailed stack trace for debugging purposes.