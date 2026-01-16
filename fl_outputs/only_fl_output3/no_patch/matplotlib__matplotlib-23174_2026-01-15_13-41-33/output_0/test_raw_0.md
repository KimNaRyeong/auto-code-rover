Below is the standalone Python file `reproducer.py` you have requested. Save this file in the root directory of your project. When you run it using `python3 reproducer.py`, it will attempt to reproduce the described issue. It will raise an `AssertionError` if the issue is present and print a stack trace of the issue. Otherwise, it exits with code 0 indicating the issue is fixed.

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

def main():
    try:
        # Reproducing the given issue
        delta = 0.025
        x = np.arange(-3.0, 3.0, delta)
        y = np.arange(-2.0, 2.0, delta)
        X, Y = np.meshgrid(x, y)
        Z1 = np.exp(-(X**2) - Y**2)
        Z2 = np.exp(-((X - 1) ** 2) - (Y - 1) ** 2)
        Z = (Z1 - Z2) * 2

        fig = plt.figure()
        figs = fig.subfigures(nrows=1, ncols=2)

        for f in figs:
            ax = f.subplots()
            CS = ax.contour(X, Y, Z)
            ax.clabel(CS, inline=True, fontsize=10)
            ax.set_title("Simplest default with labels")

        plt.show()
        # If no error occurs, we assume the issue is fixed
        print("No issue detected.")
    except Exception as e:
        print_stacktrace(e)
        assert False, "The script caught an error indicating the described issue is present."

if __name__ == "__main__":
    main()
```

Before running this script, ensure you have Matplotlib and NumPy installed in your Python environment as they are required for the script to execute. The script outlines the reproduction steps for the contour label issue on subfigures, raising an `AssertionError` if the problem persists or completing successfully if the issue is resolved.