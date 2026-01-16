```python
# reproducer.py
def main():
    import matplotlib.pyplot as plt
    import numpy as np

    try:
        x = np.array([[np.nan, np.nan], [np.nan, np.nan]])
        plt.contour(x)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present. Exiting normally.")
        exit(0)

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

if __name__ == "__main__":
    main()
```
When executed in a Python environment where Matplotlib 3.0.3 is installed (alongside the noted dependencies and in the described operating system), this script will try to generate a contour plot of an array composed entirely of `np.nan` values. If the issue is present, it will catch the `AssertionError` raised within Matplotlib's internals, print a detailed stack trace pointing to the source of the error, and exit with code 1. Conversely, if the issue has been resolved in the version of Matplotlib being used, the script will exit normally with code 0, indicating the absence of the problem.